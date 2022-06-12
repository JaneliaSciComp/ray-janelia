#!/bin/bash
#
# ./ray-launch.sh -n 20 -e ray-python -p "/path/to/job.py --options"
#
DIR=$(cd "$(dirname "$0")"; pwd)

while getopts "n:e:d::m::o::p::b::h" option;do
    case "${option}" in
    n) n=${OPTARG}
        slots=$n
    ;;
    e) e=${OPTARG}
        conda_env=$e
    ;;
    d) d=${OPTARG}
        nodes=$d
    ;;
    m) m=${OPTARG}
        object_store_mem=$m
    ;;
    o) o=${OPTARG}
        output_file=$o
    ;;
    p) p=${OPTARG}
        python_command=$p
    ;;
    b) b=${OPTARG}
        bsub_opts=$b
    ;;
    h) echo "Usage: $0 -n slots -e conda-env-name [-d num-nodes] [-m object-store-bytes] [-o output-file] [-p python-command] [-b bsub-options]"
        exit 1
    ;;
    esac
done

if [ -z "$slots" ]; then
    echo "Use -n to provide the number of slots you want for your cluster."
    exit 1
fi

if [ -z "$conda_env" ]; then
    echo "Use -e to provide the name of a conda environment with ray installed."
    exit 1
fi

ptile=4
if [ -n "$nodes" ]; then
    ptile=$(( slots / nodes ))
    echo "Using tiling of $ptile slots per node"
else
    echo "Using default tiling of 4 slots per node"
fi

if [ -z "$object_store_mem" ]; then
    echo "Using default object store mem of 4GB. Make sure your cluster has more than 4GB of memory."
    object_store_mem=4000000000
fi

if [ -z "$output_file" ]; then
    output_file="std%J.out"
fi

command_str=""
if [ -n "$python_command" ]; then
    command_str="-c python $python_command"
fi

bsub -o $output_file -e $output_file -n $slots -R "span[ptile=$ptile]" $bsub_opts \
    bash -i $DIR/ray-janelia.sh -n $conda_env -m $object_store_mem "$command_str"
