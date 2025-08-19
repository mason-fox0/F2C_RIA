#!/bin/bash
rm -r __pycache__
rm -r ../build
rm -r ../*egg-info
python -m pip install ../.
python sobolSample.py
