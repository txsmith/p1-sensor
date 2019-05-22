#!/bin/bash
DIR="$(cd "$(dirname "$0")" && pwd)"
$DIR/retry.sh 3 "$DIR/read.sh"