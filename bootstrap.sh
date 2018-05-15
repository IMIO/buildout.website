#!/bin/sh
# Usage:
#     ./bootstrap.sh  # use buildout.cfg
#     ./bootstrap.sh -c dev.cfg  # use dev.cfg
ln -s dev.cfg buildout.cfg
pip install -I --user -r requirements.txt
~/.local/bin/buildout "$@"
