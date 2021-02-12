#!/bin/bash
echo "Setting up environment"
source env-lxplus.sh
echo "Setup complete"
echo "Will run:"
echo "$@"
eval "$@"
