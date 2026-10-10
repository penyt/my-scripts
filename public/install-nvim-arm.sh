#!/bin/bash

# curl -fsSL https://sh.penyt.com/install-nvim-arm.sh | bash

curl -LO https://github.com/neovim/neovim/releases/latest/download/nvim-linux-arm64.tar.gz
sudo rm -rf /opt/nvim-linux-arm64
sudo tar -C /opt -xzf nvim-linux-arm64.tar.gz

echo
echo 'Put this in ~/.bashrc or ~/.zshrc:'
echo 'export PATH="$PATH:/opt/nvim-linux-arm64/bin"'
rm nvim-linux-arm64.tar.gz
