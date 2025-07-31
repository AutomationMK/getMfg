#!/bin/bash

if [[ ! -d $(pwd)/venv ]]; then
  python -m venv venv
fi

source $(pwd)/venv/bin/activate
pip install -r $(pwd)/requirements.txt
playwright install chromium
deactivate

CMD=~/bin/run_getMfg

pathadd() {
  if [ -d "$1" ] && [[ ":$PATH:" != *":$1:"* ]]; then
    PATH="${PATH:+"$PATH:"}$1"
  fi
}

if [[ ! -d ~/bin ]]; then
  mkdir ~/bin
  pathadd ~/bin
  echo "export PATH='$PATH'" >> ~/.bashrc
  source ~/.bashrc
fi

if [[ ! -f $CMD ]]; then
  ln -s $(pwd)/run.sh $CMD
  chmod +x $CMD
fi

read -p "Press Enter to close the window..."
