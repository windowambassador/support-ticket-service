# Локальный стенд и GitHub Actions runner

**Автор:** Горохов Георгий, 4П1.23

## Назначение

Стенд предназначен для BL-26 и последующей проверки отката BL-27. Он использует отдельный дистрибутив Ubuntu 24.04 LTS в виртуальной среде WSL 2. У дистрибутива свой диск, пользователи и Docker Engine; ядро и ресурсы виртуальной машины управляются WSL 2. Docker Desktop для этого стенда не используется.

20.11.2026 runner `gorokhov-staging` подключён к [репозиторию Горохова](https://github.com/windowambassador/support-ticket-service). GitHub показывает статус online и метки self-hosted, Linux, X64 и gorokhov-staging. Служба включена в systemd. Проверены запуск штатным PowerShell-скриптом, Docker Engine 29.9.3, Compose 5.7.1 и запуск контейнера от пользователя runner. В GitHub Actions настроен секрет STAGING_DB_PASSWORD. Первый запуск доставки из этого репозитория предстоит выполнить после слияния workflow в main.

## Конфигурация

| Параметр | Значение |
|---|---|
| Дистрибутив WSL | gorokhov-support-staging |
| Образ ОС | Ubuntu 24.04.5 LTS, amd64 |
| Каталог виртуального диска Windows | C:\Users\Admin\Documents\PracticeVMs\gorokhov-staging\disk |
| Пользователь runner | runner |
| Каталог runner | /opt/actions-runner |
| Каталог приложения | /srv/support-service |
| Метка задания доставки | gorokhov-staging |
| Исходная версия runner | 2.338.2 |

Образ Ubuntu загружается с releases.ubuntu.com; его SHA-256 сверяется с SHA256SUMS. Архив runner сверяется с SHA-256 официального release: baebf204307bac6193480852732f0aba2ae97b6c5597c244f4d5558390147c40. Runner может автоматически обновляться после регистрации; фактическая версия проверяется отдельно.

[install-host.sh](../scripts/staging/install-host.sh) устанавливает Docker из официального apt-репозитория, Compose, служебные утилиты и runner. Скрипт рассчитан на выделенную Ubuntu 24.04 x86_64 и запускается от root. Пользователь runner входит в группу docker; эта группа даёт административный доступ к Docker внутри стенда. Проверки PR остаются на GitHub-hosted runner, локальный runner предназначен для доверенной доставки из main.

[wsl.conf](../scripts/staging/wsl.conf) включает systemd, отключает автоматическое подключение дисков Windows и запуск Windows-программ из Linux. Файл устанавливается как /etc/wsl.conf только внутри этого дистрибутива. Изменение вступает в силу после остановки и запуска данного дистрибутива; глобальный wsl --shutdown не нужен.

## Подготовка и регистрация

1. Скачать официальный WSL-образ Ubuntu 24.04 и проверить SHA-256.
2. Импортировать образ под именем gorokhov-support-staging с --version 2 в указанный каталог disk.
3. Передать install-host.sh внутрь дистрибутива и выполнить его от root.
4. Установить wsl.conf и перезапустить только gorokhov-support-staging.
5. В настройках отдельного репозитория открыть Actions → Runners → New self-hosted runner, выбрать Linux x64 и получить временный регистрационный токен.
6. От пользователя runner выполнить config.sh с URL отдельного репозитория, именем gorokhov-staging и меткой gorokhov-staging. Токен не записывать в документацию, файлы проекта или историю shell.
7. Установить и запустить службу через svc.sh install runner и svc.sh start. Проверить online и busy=false в GitHub.

Токены и служебные credentials хранятся только внутри установленного runner. Виртуальный диск находится вне репозитория и не удаляется задачей Gradle clean.

## Проверка и остановка

Для запуска подготовленного стенда из корня проекта выполнить [start-local-staging.ps1](../scripts/staging/start-local-staging.ps1). Скрипт оставляет скрытый процесс WSL активным, запускает Docker и службу runner. Повторный вызов не создаёт второй удерживающий процесс.

```powershell
./scripts/staging/start-local-staging.ps1
```

Из PowerShell можно проверить дистрибутив и открыть Linux:

```powershell
wsl --list --verbose
wsl -d gorokhov-support-staging --cd /home/runner
```

В Linux:

```bash
docker version
docker compose version
systemctl is-active docker
/opt/actions-runner/bin/Runner.Listener --version
```

Служба runner запускается при старте дистрибутива. Это не означает автоматический запуск дистрибутива после включения Windows. На время работы стенда процесс WSL должен оставаться активным. Остановка выполняется только после завершения заданий runner:

```powershell
wsl --terminate gorokhov-support-staging
```

Команда останавливает этот стенд; она не удаляет виртуальный диск. Не использовать wsl --unregister для обычной остановки: эта команда удаляет дистрибутив и его данные.

## Граница текущего этапа

Подготовка окружения не заменяет BL-26. Задание доставки после publish реализовано в следующем изменении: конкретный image@sha256, Compose без сборки, health и API, запись SHA, digest и ID контейнера. Порядок запуска и результаты находятся в [описании доставки](staging-deployment.md). До коммита, слияния и проверки реального задания BL-26 остаётся незавершённым. Откат к предыдущему образу относится к BL-27.

## Выполненные проверки

12.11.2026 импортирован отдельный дистрибутив gorokhov-support-staging, Ubuntu 24.04.5 LTS с systemd. SHA-256 установочного образа bb415d824822c4b878125729af451a5d18fb13d1cf5cbed9a7393ad64ac6039e совпал с официальным SHA256SUMS.

Docker Engine запущен внутри дистрибутива. Пользователь runner успешно выполнил docker run --rm hello-world; контейнер завершился с кодом 0 и удалён штатным параметром --rm. Это проверка окружения, не развёртывание приложения через pipeline. Журнал: build/vm-hello-world.log.

Копия проекта прошла spotlessCheck, checkTextConventions, unitTest и bootJar с повторным выполнением задач. Подтверждены 129 успешных модульных тестов без ошибок и пропусков, точка входа ru.gorokhov.support.SupportApplication. Workflow прошёл actionlint; синтаксис install-host.sh и start-local-staging.ps1 проверен. Материалы: build/copy-local-check.log и build/copy-local-verification.json.

Runner зарегистрирован 12.11.2026 в VasilevYuV/support-ticket-service-test: имя gorokhov-staging, ID 2, метки self-hosted, Linux, X64 и gorokhov-staging. GitHub API подтвердил status=online и busy=false. Служба actions.runner.VasilevYuV-support-ticket-service-test.gorokhov-staging.service установлена от пользователя runner, включена и активна.

Фактические версии: Docker Engine 29.9.3, Compose 5.7.1, Actions runner 2.338.2, ядро 5.15.167.4-microsoft-standard-WSL2. После применения wsl.conf проверены systemd, работа Docker и отсутствие автомонтирования /mnt/c. В Linux работает один удерживающий процесс sleep infinity; Windows запускает для него launcher и дочерний wsl.exe. Docker Desktop остаётся остановленным.

Материалы проверки: build/vm-install-host.log, vm-runner-registration.log, vm-runner-status.json и local-staging-verification.json. Credentials runner находятся внутри виртуального диска, в Git не добавляются. В новом репозитории опубликованы main и feature-c/pull-request-ci. PR #1 прошёл CI и слит; первая публикация в GHCR успешна. Этот запуск выполнялся на GitHub-hosted runner. Локальный runner пока не выполнял доставку через pipeline.

## Источники

- [Ubuntu в WSL 2](https://documentation.ubuntu.com/wsl/latest/guides/install-ubuntu-wsl2/).
- [Команды WSL](https://learn.microsoft.com/en-us/windows/wsl/basic-commands).
- [Docker Engine для Ubuntu](https://docs.docker.com/engine/install/ubuntu/).
- [Регистрация runner](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/add-runners).
- [Служба runner](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/configure-the-application).
