# Ревизии материалов практики

Горохов Георгий, 4П1.23

После переноса истории в личный репозиторий SHA изменились. В датированных журналах сохранены исходные номера, чтобы можно было сверить артефакты прежних запусков. В таблице указан соответствующий коммит с тем же деревом файлов. Итоговые запуски личного репозитория перечислены в [отчёте](final-report.md).

| SHA в журнале | SHA в личном репозитории | Изменение |
|---|---|---|
| `4959b8f` | [a5ecde6](https://github.com/windowambassador/support-ticket-service/commit/a5ecde6fd0c040317005067b6c875e27f60cc932) | docs: define project scope and requirements |
| `0554e34` | [0b18caf](https://github.com/windowambassador/support-ticket-service/commit/0b18caf2390da57a1dd32ee3956dd4c55dc5ffa4) | docs: add user stories and prioritized backlog |
| `1a95bf8` | [245a224](https://github.com/windowambassador/support-ticket-service/commit/245a2245dca80215eb1470c77288428cc61f633a) | docs: design architecture and data model |
| `f60ba26` | [0a264f0](https://github.com/windowambassador/support-ticket-service/commit/0a264f0d8c94c5f3806778657baca13105c413dc) | docs: specify API contract and test plan |
| `1e528ee` | [2eabcb1](https://github.com/windowambassador/support-ticket-service/commit/2eabcb176fad22dc166519ecf930d0412901ca4a) | build: initialize Java and Kotlin application |
| `7ab7833` | [3484d0c](https://github.com/windowambassador/support-ticket-service/commit/3484d0cc870c5ce276d6cd8c2cf91497c1e089e2) | feat: add PostgreSQL schema and Flyway migrations |
| `9134482` | [8aeda46](https://github.com/windowambassador/support-ticket-service/commit/8aeda46733f26487470af9edb22f66d643ba6952) | feat: add category listing, ticket creation and retrieval |
| `ae8aa20` | [76af924](https://github.com/windowambassador/support-ticket-service/commit/76af92404b4660594166224c818a66d455064225) | feat: enforce request validation and uniform API errors |
| `7c89753` | [bdc82f0](https://github.com/windowambassador/support-ticket-service/commit/bdc82f0c3ae831b25c2967897dfcf5a11700e6b8) | feat: enforce request validation and uniform API errors |
| `ee399f9` | [8243286](https://github.com/windowambassador/support-ticket-service/commit/82432865604a8b4dd47827f2b59b0b427acf44b4) | feat: add ticket details editing with state protection |
| `68153f7` | [cb9f7a9](https://github.com/windowambassador/support-ticket-service/commit/cb9f7a929840551ba994b150f3df3b900a112ddc) | feat: add ticket status transitions and atomic history |
| `7bbeca4` | [61ecc88](https://github.com/windowambassador/support-ticket-service/commit/61ecc88a6bf118b4e069385f88899ee2111c3ec0) | feat: add ticket filtering and pagination |
| `a2247b4` | [dab26b8](https://github.com/windowambassador/support-ticket-service/commit/dab26b82684846ba9c542b3e3729fcb816fa82e5) | feat: add Kotlin summary report calculation |
| `3073ad7` | [60ad4fd](https://github.com/windowambassador/support-ticket-service/commit/60ad4fdc47b8f6db8b5c7e665d2f5918c12c6103) | feat: expose Kotlin summary report API |
| `c12d082` | [00e380b](https://github.com/windowambassador/support-ticket-service/commit/00e380ba71a9c2b2b824f9a529302702d0a01265) | test: cover report boundaries and fix historical date mapping |
| `4c75cd0` | [abc0fd1](https://github.com/windowambassador/support-ticket-service/commit/abc0fd16c7433abe76857284f200216305bafb66) | test: complete unit coverage of ticket business rules |
| `21e5aff` | [35d2613](https://github.com/windowambassador/support-ticket-service/commit/35d261331dfd240eaeb9ab4665f81cc258e28618) | test: verify integration coverage and OpenAPI responses |
| `7d971eb` | [ee3a221](https://github.com/windowambassador/support-ticket-service/commit/ee3a2215e48320bdde3777a3cbb1725a78e0942d) | test: add end-to-end ticket lifecycle scenarios |
| `9678878` | [8e992b8](https://github.com/windowambassador/support-ticket-service/commit/8e992b86078f819b650e9734a01bc86d19d7a5c5) | test: make defect regression checks reproducible |
| `9bd912c` | [f88a075](https://github.com/windowambassador/support-ticket-service/commit/f88a0750c36093e7464472a6c9183bb7dc36780c) | test: add Java and Kotlin coverage reports |
| `3203c8d` | [4e8c77d](https://github.com/windowambassador/support-ticket-service/commit/4e8c77d2c2c66aff63687cf38892db14984c74db) | feat: add Swagger UI and verified API demo collection |
| `25b1c40` | [a89e110](https://github.com/windowambassador/support-ticket-service/commit/a89e110a0fc91c59a603664841dfd53cf87f719a) | feat: add Docker Compose runtime with persistent PostgreSQL |
| `71e6c6c` | [e4fac82](https://github.com/windowambassador/support-ticket-service/commit/e4fac8270b38ef40a6cf16c3d46fae96bf1f213e) | feat: add verified PostgreSQL backup and restore |
| `2cea55b` | [94d644c](https://github.com/windowambassador/support-ticket-service/commit/94d644cae236b789fb4a260f251211ee715fe2b2) | docs: add verified runtime failure diagnostics |
| `eff4b3c` | [957039e](https://github.com/windowambassador/support-ticket-service/commit/957039e9ea4054640e8c8374cfb812bcae31cd31) | ci: add pull request checks and build artifacts |
| `883007f` | [8c4b4de](https://github.com/windowambassador/support-ticket-service/commit/8c4b4de004bcf77571f15db89d693e1e46815f70) | docs: record successful GitHub Actions verification |
| `1605f98` | [9cc2bec](https://github.com/windowambassador/support-ticket-service/commit/9cc2bec67624b15d75fd15eada2dae4eb481f875) | ci: prepare image publishing and local staging runner |
| `399fa4d` | [b028b1d](https://github.com/windowambassador/support-ticket-service/commit/b028b1dbef5d76e22eac870c0485137d618217c4) | Merge pull request #1: prepare image publishing and local staging runner |
