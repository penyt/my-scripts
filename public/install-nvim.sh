#!/bin/bash

curl -LO https://github.com/neovim/neovim/releases/latest/download/nvim-linux-x86_64.tar.gz
sudo rm -rf /opt/nvim-linux-x86_64
sudo tar -C /opt -xzf nvim-linux-x86_64.tar.gz

echo
echo 'Put this in ~/.bashrc or ~/.zshrc:'
echo 'export PATH="$PATH:/opt/nvim-linux-x86_64/bin"'
rm nvim-linux-x86_64.tar.gz
