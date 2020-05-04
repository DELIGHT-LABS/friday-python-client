#!/usr/bin/env bash

if [ ! -d "friday/.git" ]; then
  git clone https://github.com/hdac-io/friday.git
fi

cd friday
git fetch origin
git reset --hard origin/master
