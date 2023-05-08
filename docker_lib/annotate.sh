#!/bin/bash
. ~/.bashrc
set -e

# Pressing database
if [[ ! -f "/opt/conda/envs/lab/db/hmm/all_phrogs.hmm.h3f" ]]; then
    conda activate lab
    echo 'Pressing PHROGs'
    hmmpress /opt/conda/envs/lab/db/hmm/all_phrogs.hmm
fi

python /lab/bin/coordinator.py
