#!/bin/bash

if [[ -f package.json ]]; then
  npm install
fi

pulumi "$@"