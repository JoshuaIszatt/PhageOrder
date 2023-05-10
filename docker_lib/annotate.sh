#!/bin/bash
. ~/.bashrc
set -e
SECONDS=0

# Pressing database
if [[ ! -f "/opt/conda/envs/lab/db/hmm/all_phrogs.hmm.h3f" ]]; then
    conda activate lab
    echo 'Pressing PHROGs'
    hmmpress /opt/conda/envs/lab/db/hmm/all_phrogs.hmm
fi

python /lab/bin/coordinator.py
chmod -R 777 /lab/output/*

if (($SECONDS > 3600)); then
    let "hours=SECONDS/3600"
    let "minutes=(SECONDS%3600)/60"
    let "seconds=(SECONDS%3600)%60"
    echo " " >>/lab/output/docker_log.tsv
    echo "[hours:$hours,minutes:$minutes,seconds:$seconds]" >>/lab/output/docker_log.tsv
elif (($SECONDS > 60)); then
    let "minutes=(SECONDS%3600)/60"
    let "seconds=(SECONDS%3600)%60"
    echo " " >>/lab/output/docker_log.tsv
    echo "[minutes:$minutes,seconds:$seconds]" >>/lab/output/docker_log.tsv
else
    echo " " >>/lab/output/docker_log.tsv
    echo "[seconds:$SECONDS]" >>/lab/output/docker_log.tsv
fi
