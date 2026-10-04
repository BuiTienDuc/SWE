#!/usr/bin/env bash
cd -- "$(dirname -- "$0")" || exit 2
python3 evaluate.py --patch baseline
python3 evaluate.py --patch regression
python3 evaluate.py --patch partial
python3 evaluate.py --patch partial --expanded
python3 evaluate.py --patch fixed --expanded
