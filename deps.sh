#!/bin/bash
sudo apt install gnuplot tmux

mkdir ttyd
wget -O ttyd/ttyd https://github.com/tsl0922/ttyd/releases/download/1.7.7/ttyd.x86_64
chmod +x ttyd/ttyd

#install afl++
rm -rf ./AFLplusplus
git clone https://github.com/AFLplusplus/AFLplusplus
cd ./AFLplusplus
make distrib
sudo make install