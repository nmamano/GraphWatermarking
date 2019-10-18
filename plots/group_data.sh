#!/bin/bash
networks=( random_power_law youtube flickr )
for network in "${networks[@]}"
do
    grep "" "${network}"_0*_? > "${network}_data"
done
cat *_data >> data