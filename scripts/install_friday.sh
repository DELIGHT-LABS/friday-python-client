#!/usr/bin/env bash

COMMIT_HASH="5b4e25495ac4ae87b67fe646ced2c8bf5820ee40"
if [ ! -d "friday/.git" ]; then
  git clone https://github.com/hdac-io/friday.git
fi

cd friday
git fetch origin
git reset --hard $COMMIT_HASH
