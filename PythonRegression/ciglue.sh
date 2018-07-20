#!/bin/bash

set -x

git clone --depth 1 --branch yaml_config https://github.com/karimodm/iri-network-tests.git iri-network-tests
cd iri-network-tests
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

cd ..
for machine_dir in tests/features/machine?; do
  python iri-network-tests/create_cluster.py -d -c $machine_dir/cluster.yml -o $machine_dir/output.yml
done
REVISION_HASH=$(grep -F 'revision_hash:' $machine_dir/output.yml | cut -d' ' -f2)
deactivate

###
RUN ALOE TESTS HERE
###

iri-network-tests/teardown_cluster.sh -r $REVISION_HASH
