#!/bin/bash
networks=( random_power_law youtube flickr )
probs=( 0 0.01 0.001 0.0001 0.00001 0.000001 0.0000001 )
iters=( 0 1 2 3 4 5 6 7 8 9 )
exp_folder="../experiments"
mkdir "${exp_folder}"
for prob in "${probs[@]}"
do
    for i in "${iters[@]}"
    do
        echo "random_power_law ${prob} ${i}"
        python3.3 security_experiment.py random_power_law 64 "${prob}" "${exp_folder}/"random_power_law"_${prob}_${i}" sub
        echo "youtube ${prob} ${i}"
        python3.3 security_experiment.py youtube 255 "${prob}" "${exp_folder}/"youtube"_${prob}_${i}" sub
        echo "flickr ${prob} ${i}"
        python3.3 security_experiment.py flickr 300 "${prob}" "${exp_folder}/"flickr"_${prob}_${i}" sub
    done
done
