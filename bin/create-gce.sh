if [ "$#" -ne "1" ]; then
    echo "wrong arguments: Usage $0 <num-nodes>"
    exit 1
fi
./net/gce.sh create -n $1 -c 1 -d pd-ssd --custom-machine-type "--custom-cpu 16 --custom-memory 32GB --min-cpu-platform Intel%20Skylake" --dedicated
