$ErrorActionPreference = 'Stop'
$distribution = 'gorokhov-support-staging'

$keeper = Get-CimInstance Win32_Process -Filter "Name = 'wsl.exe'" |
    Where-Object {
        $_.CommandLine -like "*$distribution*" -and
        $_.CommandLine -match 'sleep\s+infinity'
    }

if (-not $keeper) {
    Start-Process -FilePath 'wsl.exe' -WindowStyle Hidden -ArgumentList @(
        '--distribution', $distribution, '--user', 'runner', '--cd', '/',
        '--exec', 'sleep', 'infinity'
    ) | Out-Null
}

& wsl.exe --distribution $distribution --user root --cd / --exec systemctl start docker
if ($LASTEXITCODE -ne 0) { throw 'Не удалось запустить Docker Engine стенда.' }

& wsl.exe --distribution $distribution --user root --cd /opt/actions-runner --exec ./svc.sh start
if ($LASTEXITCODE -ne 0) { throw 'Не удалось запустить службу runner. Проверьте регистрацию.' }

& wsl.exe --distribution $distribution --user runner --cd / --exec docker info --format '{{.ServerVersion}}'
if ($LASTEXITCODE -ne 0) { throw 'Docker Engine недоступен пользователю runner.' }

Write-Output 'Стенд запущен. Состояние runner проверяется в Settings > Actions > Runners.'
