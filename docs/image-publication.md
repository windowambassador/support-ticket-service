# Публикация контейнерного образа

**Автор:** Горохов Георгий, 4П1.23

## 1. Назначение

BL-25 дополняет [workflow CI](../.github/workflows/ci.yml) публикацией в GitHub Container Registry. Адрес образа: ghcr.io/vasilevyuv/support-ticket-service-test:<полный-SHA-коммита>. Тег latest не создаётся. Развёртывание на стенд остаётся BL-26.

Для связи образа с репозиторием при сборке устанавливаются OCI-метки org.opencontainers.image.source и org.opencontainers.image.revision. Путь registry переводится в нижний регистр, поскольку имя владельца GitHub содержит прописные буквы.

Публикация использует GITHUB_TOKEN текущего запуска с packages:write. Дополнительный PAT или repository secret для этого не требуется. При первой публикации пакет по умолчанию закрытый; публичный репозиторий сам по себе не делает пакет публичным. Права пакета и загрузка из другого окружения проверяются отдельно. Основание: [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry).

## 2. События и зависимости

| Событие | verify | image | publish |
|---|---|---|---|
| pull_request | Форматирование, сборка, тесты и отчёты | Сборка и метаданные | Пропущено |
| push в main, в том числе после слияния PR | Те же проверки | Сборка, метаданные и архив образа | После успеха image |
| workflow_dispatch на main, без контрольного отказа | Те же проверки | Сборка и архив | После успеха image |
| workflow_dispatch в другой ветке, без контрольного отказа | Те же проверки | Только сборка и метаданные | Пропущено |
| workflow_dispatch на main с verify_publication_gate=true | Временный падающий JUnit-тест | Должно быть skipped | Должно быть skipped |

Цепочка зависимостей: verify → image → publish. У publish нет always() или continue-on-error. Условие публикации не исключает verify_publication_gate: в контрольном запуске публикацию должен остановить именно провал теста, а не отдельный запрет по входному параметру. Если контрольный режим выбран не на main, запуск отклоняется до создания теста и не засчитывается как проверка блокировки.

Новый запуск PR отменяет предыдущий для того же PR. Уже выполняющийся запуск main не прерывается новым коммитом. Права verify и image остаются contents:read, packages:write выдан только publish. Docker credentials сохраняются во временной папке runner, токен передаётся через stdin, завершение сеанса registry выполняется через always().

Workflow реагирует на любой push в main. Для ограничения изменения main слияниями PR нужно отдельно настроить правила ветки; один YAML-файл не запрещает прямой push.

## 3. Передача и публикация образа

В image образ собирается один раз под локальным тегом support-service:ci-<SHA>. Для main выполняется docker save с gzip, а архив и image.json передаются в артефакте container-image-<SHA>. Он хранится один день и не создаётся для PR. Архив уже сжат, повторное сжатие upload-artifact отключено.

Задание publish выполняет следующие действия:

1. Скачивает артефакт текущего запуска через actions/download-artifact v8.0.2, закреплённый SHA.
2. Выполняет docker load и сверяет ID с image.json, затем проверяет OCI-метку revision по GITHUB_SHA.
3. Входит в ghcr.io с GITHUB_TOKEN и присваивает уже загруженному образу тег полного SHA.
4. Выполняет docker push, получает RepoDigests и формирует release.json.
5. Загружает образ из registry по digest и повторно сверяет его ID.
6. Сохраняет release.json и published-image.json в артефакте release-<SHA> на 14 дней.

Повторной сборки в publish нет. В output publish.image передаётся ссылка ghcr.io/vasilevyuv/support-ticket-service-test@sha256:..., которую можно использовать для развёртывания конкретного содержимого. Формат release.json:

```json
{
  "tag": "ghcr.io/vasilevyuv/support-ticket-service-test:<commit-sha>",
  "image": "ghcr.io/vasilevyuv/support-ticket-service-test@sha256:<registry-digest>",
  "imageId": "sha256:<image-id>",
  "commit": "<commit-sha>"
}
```

SHA-тег обозначает версию исходников, digest фиксирует содержимое образа. Повторный обычный ручной запуск на том же коммите может пересобрать и обновить этот тег; для стенда и отката нужно сохранять ссылку по digest. ID локального Docker-образа и digest registry не следует считать одним значением.

Если push прошёл, а последующая проверка или сохранение артефакта завершились ошибкой, образ уже может присутствовать в registry. Такой запуск не считается успешной публикацией всего pipeline; причину нужно проверить в логах и registry. Публикация образа не подтверждает его работу на стенде.

## 4. Проверка после коммита и слияния

Сначала отправить изменения в PR и дождаться успеха verify/image. Publish на PR должен быть skipped. После слияния в main автоматически начнётся запуск push; он должен завершить все три задания успешно.

Скачать release-<SHA>, сверить commit с SHA основной ветки, tag с полным SHA и image с digest опубликованного пакета. В логах проверить загрузку по digest и сравнение ID. Сохранить URL запуска, tag, digest, ID и артефакт release.json. Не использовать для этого служебный merge-SHA старого PR-запуска вместо SHA фактического коммита main.

Для проверки блокировки открыть Actions → CI → Run workflow, выбрать main и включить verify_publication_gate. В рабочей копии runner будет создан PublicationGateProbeTest с явным AssertionFailedError. Этот класс отсутствует в src репозитория, не требует изменения истории и не попадает в образ: image получает отдельный checkout, а при отказе verify вообще не запускается.

Ожидаемый результат контрольного запуска:

- verify завершается failure именно на JUnit-тесте, а не на checkout, оформлении или недоступном Docker;
- в test-reports-<SHA> есть XML с отказом PublicationGateProbeTest;
- image и publish имеют skipped;
- новые container-image-<SHA> и release-<SHA> в этом запуске отсутствуют;
- digest ранее опубликованного SHA-тега не изменился.

После этого повторить ручной запуск на main без контрольного режима и подтвердить возвращение нормальных проверок. Падающий класс создаётся только в отдельной рабочей копии контрольного запуска; постоянно падающий тест в проект не добавляется. Это эксплуатационная проверка, а не найденный дефект бизнес-логики.

До включения задания deploy в main проверяется только блокировка публикации. OPS-07 и AC-12.3 полностью закрываются после добавления и проверки блокировки доставки в BL-26.

## 5. Локальная подготовка BL-25 от 11.11.2026

Подготовлено 11.11.2026 поверх коммита 883007fec36f8f0f6c063bb68b057f10ca793cf1. Этот коммит с результатами BL-24 отправлен в [PR #1](https://github.com/VasilevYuV/support-ticket-service/pull/1), оба задания повторного [CI #2](https://github.com/VasilevYuV/support-ticket-service/actions/runs/43092583552) прошли успешно. CI #2 проверяет прежний workflow без публикации; на тот момент новые настройки BL-25 ещё не были закоммичены.

| Локальная проверка | Результат |
|---|---|
| actionlint 1.7.12 | Workflow прошёл проверку |
| actions/download-artifact | v8.0.2, SHA 9000827ccba6bdab643e8b6fd33ac0654aef8333 и параметры сверены с GitHub |
| Команды image/save/load из YAML | Выполнены без изменения в отдельной копии; после удаления проверочного тега архив восстановил тот же ID и revision |
| Неверный ожидаемый ID | Загрузка выполнена, проверка ID остановила шаг с кодом 1 до входа в registry |
| Контрольный JUnit-тест | Форматирование прошло; выбранный тест дал ровно один ожидаемый отказ, ошибок инфраструктуры нет |

Проверочный образ имеет ID sha256:9c21049fd9f5f194e409c7a67211e092c0ac36c01be557ba19fe703bbfd06026. При локальной проверке использованы Git Bash, Docker Desktop 28.4.0 и Temurin 25.0.5 в Linux-контейнере; для команды python3 в Git Bash использован локальный Python. Проверочный контейнер удалён после копирования JUnit XML. Основные исходники и тесты приложения не менялись.

Материалы: build/bl25-image-transfer.log, bl25-image-mismatch.log, bl25-gate-probe.log, bl25-gate-test-results, bl25-actionlint.log и bl25-verification.json. Архив образа находится в build/bl25-check/build/ci/image.tar.gz. Эти локальные файлы игнорируются Git и удаляются clean.

На момент этой локальной подготовки реальная публикация в GHCR, загрузка через download-artifact и отрицательный запуск на GitHub ещё не выполнялись. Они требуют коммита BL-25, успешного CI и слияния PR. Локальный отказ JUnit проверяет подготовку контрольного теста, но не доказывает статус skipped заданий GitHub Actions. BL-25 остаётся подготовленным, OPS-07 и AC-12.3 не объявляются завершёнными.

## 6. Отдельная копия и публикация в новом репозитории

12.11.2026 в приватный [support-ticket-service-test](https://github.com/VasilevYuV/support-ticket-service-test) отправлены main и feature-c/pull-request-ci. Автор Горохов Георгий, 4П1.23, пакет ru.gorokhov.support и прежняя история сохранены. Исторические ссылки выше относятся к прежним запускам в исходном репозитории.

[PR #1](https://github.com/VasilevYuV/support-ticket-service-test/pull/1) прошёл [CI](https://github.com/VasilevYuV/support-ticket-service-test/actions/runs/43271317629): verify и image успешны, publish skipped. После слияния создан коммит 399fa4dc37dc3ab33093e113fa870d29fbbf0c36. [Запуск main](https://github.com/VasilevYuV/support-ticket-service-test/actions/runs/43272882544) завершился успешно во всех трёх заданиях.

Скачаны артефакты тестов и публикации. В JUnit XML подтверждены 507 выполнений без failures, errors и skipped. В release.json проверены:

- tag: ghcr.io/vasilevyuv/support-ticket-service-test:399fa4dc37dc3ab33093e113fa870d29fbbf0c36;
- image: ghcr.io/vasilevyuv/support-ticket-service-test@sha256:662c4a7c0240807372d16c79ed0153ff08e03c44dd879ddb5947decf07bcc316;
- imageId: sha256:cf7f8bf719c8a0518facd12e003bc5bb3c5d6479b9a983c957eda868a7e94887;
- commit: 399fa4dc37dc3ab33093e113fa870d29fbbf0c36.

Publish загрузил опубликованный образ обратно по digest и сравнил ID с переданным артефактом сборки. Материалы: build/bl26-publication-verification.json и скачанные ZIP в build. Публикация подтверждена; контрольный отказ в новом репозитории пока не выполнен. Его проверка вместе с блокировкой доставки описана в [BL-26](staging-deployment.md). BL-25, OPS-07 и AC-12.3 полностью завершёнными пока не объявляются.
