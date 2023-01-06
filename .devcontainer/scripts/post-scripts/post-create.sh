#!/bin/bash

RESET="\\033[0m"
RED="\\033[31;1m"
GREEN="\\033[32;1m"
YELLOW="\\033[33;1m"
BLUE="\\033[34;1m"
WHITE="\\033[37;1m"

say_green() {
    [ -z "${SILENT}" ] && printf "%b%s%b\\n" "${GREEN}" "$1" "${RESET}"
    return 0
}

say_red() {
    printf "%b%s%b\\n" "${RED}" "$1" "${RESET}"
}

say_yellow() {
    [ -z "${SILENT}" ] && printf "%b%s%b\\n" "${YELLOW}" "$1" "${RESET}"
    return 0
}

say_blue() {
    [ -z "${SILENT}" ] && printf "%b%s%b\\n" "${BLUE}" "$1" "${RESET}"
    return 0
}

say_white() {
    [ -z "${SILENT}" ] && printf "%b%s%b\\n" "${WHITE}" "$1" "${RESET}"
    return 0
}

say_blue "=== Adding awslocal command 🛎️ ==="
echo 'alias awslocal="AWS_ACCESS_KEY_ID=test
                      AWS_SECRET_ACCESS_KEY=test
                      AWS_DEFAULT_REGION=${DEFAULT_REGION:-$AWS_DEFAULT_REGION}
                      aws --endpoint-url=http://localstack:4566"' | tee -a ~/.bashrc ~/.zshrc 1>/dev/null

say_blue "=== Installing Pants 👖 ==="
chmod 754 /pants_install_bug/pants
cd /pants_install_bug/ && ./pants --version
echo "alias p=/pants_install_bug/pants" | tee -a ~/.bashrc ~/.zshrc 1>/dev/null

say_blue "=== Installing Python dependencies 📦️ ==="
./pants export :: || say_red 'Pants export failed. Please run ./pants generate-lockfiles && ./pants export ::'
echo 'export PATH=/pants_install_bug/dist/export/python/virtualenvs/default/$PYTHON_VERSION/bin:$PATH' | tee -a ~/.bashrc ~/.zshrc 1>/dev/null
chmod +x /pants_install_bug/.devcontainer/scripts/git.sh

say_blue "=== Activating git pre-commit hooks 🚀 ==="
chmod +x git_hooks/*
git config core.hooksPath "/pants_install_bug/git_hooks"

# Install Pulumi CLI
curl -fsSL https://get.pulumi.com | sh -s -- --version ${PULUMI_VERSION}
echo 'export PATH=$HOME/.pulumi/bin:$PATH' | tee -a ~/.bashrc ~/.zshrc 1>/dev/null
chmod +x /pants_install_bug/init-localstack.sh

say_blue "=== Adding autocompletion for Nefino CLI ✨ ==="
echo 'eval "$(_NEFINO_COMPLETE=bash_source nefino)"' | tee -a ~/.bashrc ~/.zshrc 1>/dev/null

# # serverless
# /pants_install_bug/django/docker-entrypoint.sh
