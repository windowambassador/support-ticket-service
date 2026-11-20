import argparse
import fcntl
import json
import os
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from verify_api import verify_api


def docker(*args, capture=False):
    result = subprocess.run(["docker", *args], check=True, text=True, capture_output=capture)
    return result.stdout.strip() if capture else None


def write_json(path, value):
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def validate(args):
    if not re.fullmatch(r"[a-z0-9][a-z0-9.:-]*/[a-z0-9._/-]+@sha256:[a-f0-9]{64}", args.image):
        raise ValueError("Требуется полный адрес образа с digest sha256.")
    if not re.fullmatch(r"[a-f0-9]{40}", args.commit):
        raise ValueError("Требуется полный SHA коммита.")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}", args.deployment_id):
        raise ValueError("Недопустимый идентификатор доставки.")
    password = os.environ.get("STAGING_DB_PASSWORD", "")
    if not re.fullmatch(r"[A-Za-z0-9_-]{32,128}", password):
        raise ValueError("STAGING_DB_PASSWORD должен содержать 32-128 букв, цифр, дефисов или подчёркиваний.")
    project = os.environ.get("STAGING_PROJECT", "support-staging")
    if not re.fullmatch(r"[a-z0-9][a-z0-9_-]{0,49}", project):
        raise ValueError("Недопустимое имя Compose-проекта.")
    port = int(os.environ.get("STAGING_PORT", "18080"))
    timeout = int(os.environ.get("STAGING_WAIT_TIMEOUT", "180"))
    if not 1024 <= port <= 65535 or not 10 <= timeout <= 600:
        raise ValueError("Порт или тайм-аут вне допустимого диапазона.")
    return password, project, port, timeout


def deploy(args):
    password, project, port, timeout = validate(args)
    root = Path(os.environ.get("STAGING_ROOT", "/srv/support-service")).resolve(strict=True)
    source = Path(__file__).resolve().parents[2]
    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with (root / ".deployment.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        database_env = root / ".env"
        credentials = "DB_NAME=support_service\nDB_USERNAME=support_service\nDB_PASSWORD=" + password + "\n"
        if database_env.exists() and database_env.read_text(encoding="utf-8") != credentials:
            raise ValueError("Настройки существующей БД отличаются; автоматическая смена пароля запрещена.")
        release = root / "releases" / args.deployment_id
        if release.exists():
            raise ValueError("Этот идентификатор доставки уже использован.")

        print("Загрузка образа по digest.", flush=True)
        docker("pull", args.image)
        image = json.loads(docker("image", "inspect", args.image, capture=True))[0]
        labels = image.get("Config", {}).get("Labels") or {}
        expected_source = os.environ.get("EXPECTED_IMAGE_SOURCE", "https://github.com/windowambassador/support-ticket-service")
        if labels.get("org.opencontainers.image.revision") != args.commit:
            raise ValueError("Revision образа не совпадает с SHA коммита.")
        if labels.get("org.opencontainers.image.source") != expected_source:
            raise ValueError("Источник образа не совпадает с репозиторием.")
        if args.image not in image.get("RepoDigests", []):
            raise ValueError("Docker не подтвердил запрошенный digest.")

        release.mkdir(parents=True, mode=0o750)
        for name in ("compose.yaml", "compose.staging.yaml"):
            shutil.copyfile(source / name, release / name)
        if not database_env.exists():
            descriptor = os.open(database_env, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(descriptor, "w", encoding="utf-8") as file:
                file.write(credentials)
        os.chmod(database_env, 0o600)
        (release / "release.env").write_text(
            f"APP_IMAGE={args.image}\nAPP_PORT={port}\n", encoding="utf-8"
        )
        compose = ["compose", "--project-directory", str(release), "--project-name", project,
                   "--env-file", str(database_env), "--env-file", str(release / "release.env"),
                   "-f", str(release / "compose.yaml"), "-f", str(release / "compose.staging.yaml")]
        # Переменные окружения имеют приоритет над .env; задаются проверенные значения.
        os.environ.update(DB_NAME="support_service", DB_USERNAME="support_service", DB_PASSWORD=password,
                          APP_IMAGE=args.image, APP_PORT=str(port))
        docker(*compose, "config", "--quiet")
        docker(*compose, "pull", "postgres")
        print("Запуск Compose и ожидание health checks.", flush=True)
        docker(*compose, "up", "--detach", "--no-build", "--wait", "--wait-timeout", str(timeout))
        container_id = docker(*compose, "ps", "--quiet", "app", capture=True)
        container = json.loads(docker("inspect", container_id, capture=True))[0]
        if container["Image"] != image["Id"] or container["State"].get("Health", {}).get("Status") != "healthy":
            raise ValueError("Работающий контейнер не соответствует проверенному образу или health check.")
        checks = verify_api(f"http://127.0.0.1:{port}")
        result = {"status": "success", "deploymentId": args.deployment_id, "commit": args.commit,
                  "image": args.image, "imageId": image["Id"], "containerId": container_id,
                  "project": project, "port": port, "runUrl": args.run_url, "checks": checks,
                  "completedAt": datetime.now(timezone.utc).isoformat(), "releaseDirectory": str(release)}
        current = root / "current.json"
        if current.exists():
            previous = json.loads(current.read_text(encoding="utf-8"))
            write_json(root / "previous.json", previous)
        write_json(release / "deployment.json", result)
        write_json(current, result)
        write_json(output, result)
        print("Доставка проверена: health, API, SHA и ID образа совпали.", flush=True)


def main():
    parser = argparse.ArgumentParser(description="Доставка проверенного образа на локальный стенд.")
    parser.add_argument("--image", required=True)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--deployment-id", required=True)
    parser.add_argument("--run-url", default="")
    parser.add_argument("--output", default="build/ci/deployment.json")
    args = parser.parse_args()
    try:
        deploy(args)
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        output = Path(args.output).resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        message = "Ошибка команды Docker/Compose." if isinstance(error, subprocess.CalledProcessError) else str(error)
        write_json(output, {"status": "failure", "deploymentId": args.deployment_id,
                            "commit": args.commit, "message": message})
        print("Доставка не подтверждена: " + message, flush=True)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
