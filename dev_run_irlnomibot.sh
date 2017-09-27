#!/bin/sh -e

cd `dirname $0`

. activate.sh

python3 setup.py develop

mimicbot irlnomibot 30 post
