import fcntl
import json
import os
from pathlib import Path

from deploy import docker, write_json
from verify_api import verify_api


def rollback(root):
    with (root / ".deployment.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        current = json.loads((root / "current.json").read_text())
        previous = json.loads((root / "previous.json").read_text())
        release = (root / "releases" / previous["deploymentId"]).resolve(strict=True)
        if release.parent != (root / "releases").resolve() or current["project"] != previous["project"]:
            raise ValueError("Каталог или проект предыдущего релиза не совпадает.")
        for key in ("APP_IMAGE", "APP_PORT", "DB_PASSWORD", "DB_USERNAME", "DB_NAME"):
            os.environ.pop(key, None)
        compose = [
            "compose", "--project-name", previous["project"],
            "--env-file", str(root / ".env"), "--env-file", str(release / "release.env"),
            "-f", str(release / "compose.yaml"), "-f", str(release / "compose.staging.yaml"),
        ]
        if docker("image", "inspect", "--format", "{{.Id}}", previous["image"], capture=True) != previous["imageId"]:
            raise ValueError("Предыдущий образ отсутствует в локальном хранилище.")
        docker(*compose, "up", "-d", "--no-build", "--pull", "never", "--wait", "--wait-timeout", "180")
        container = docker(*compose, "ps", "-q", "app", capture=True)
        if docker("inspect", "--format", "{{.Image}}", container, capture=True) != previous["imageId"]:
            raise ValueError("После отката запущен другой образ.")
        checks = verify_api(f"http://127.0.0.1:{previous['port']}")
        result = dict(previous, containerId=container, checks=checks)
        write_json(root / "rollback.json", {"from": current, "to": result})
        write_json(root / "current.json", result)
        write_json(root / "previous.json", current)
        print("Откат проверен:", result["image"])


if __name__ == "__main__":
    rollback(Path(os.environ.get("STAGING_ROOT", "/srv/support-service")).resolve(strict=True))
