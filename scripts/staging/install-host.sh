#!/usr/bin/env bash
set -euo pipefail

if [[ $(id -u) != 0 ]]; then
    echo "Запустите подготовку от root." >&2
    exit 1
fi
source /etc/os-release
if [[ "$ID" != ubuntu || "$VERSION_ID" != 24.04 ]]; then
    echo "Требуется Ubuntu 24.04 LTS." >&2
    exit 1
fi
if [[ $(uname -m) != x86_64 ]]; then
    echo "Требуется архитектура x86_64." >&2
    exit 1
fi

export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y ca-certificates curl git jq python3 tar gzip unzip
install -m 0755 -d /etc/apt/keyrings
curl --fail --silent --show-error --location https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
chmod 0644 /etc/apt/keyrings/docker.asc
cat > /etc/apt/sources.list.d/docker.sources <<'DOCKER'
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: noble
Components: stable
Architectures: amd64
Signed-By: /etc/apt/keyrings/docker.asc
DOCKER
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
systemctl enable --now docker

if ! id runner >/dev/null 2>&1; then
    useradd --create-home --shell /bin/bash runner
fi
usermod --append --groups docker runner
install -d -o runner -g runner -m 0750 /opt/actions-runner /srv/support-service

runner_version=2.338.2
runner_sha256=baebf204307bac6193480852732f0aba2ae97b6c5597c244f4d5558390147c40
if [[ ! -f /opt/actions-runner/config.sh ]]; then
    archive=$(mktemp /tmp/actions-runner.XXXXXX.tar.gz)
    trap 'rm -f -- "$archive"' EXIT
    curl --fail --silent --show-error --location --retry 3 \
        "https://github.com/actions/runner/releases/download/v${runner_version}/actions-runner-linux-x64-${runner_version}.tar.gz" \
        --output "$archive"
    printf '%s  %s\n' "$runner_sha256" "$archive" | sha256sum --check
    tar --extract --gzip --file "$archive" --directory /opt/actions-runner
    chown -R runner:runner /opt/actions-runner
fi
/opt/actions-runner/bin/installdependencies.sh
runuser -u runner -- docker version
runuser -u runner -- docker compose version
runuser -u runner -- /opt/actions-runner/bin/Runner.Listener --version
