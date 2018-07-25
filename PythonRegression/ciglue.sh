#!/bin/bash

set -x

DOCKER_REGISTRY=dyrellc/iri-network-tests
ERROR=0

git clone --depth 1 --branch yaml_configuration https://github.com/karimodm/iri-network-tests.git iri-network-tests
cd iri-network-tests
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

cd ..
for machine_dir in tests/features/machine?; do
  python iri-network-tests/create_cluster.py -u $DOCKER_REGISTRY -d -c $machine_dir/config.yml -o $machine_dir/output.yml
  if [ $? -ne 0 ]; then
    ERROR=1
    python <<EOF
import yaml
for (key,value) in yaml.load(open('$machine_dir/output.yml'))['nodes'].iteritems():
  if value['status'] == 'Error':
    print value['log']
EOF
  fi
done
REVISION_HASH=$(grep -F 'revision_hash:' $machine_dir/output.yml | cut -d' ' -f2)
deactivate

if [ $ERROR -eq 0 ]; then
  echo "Starting tests..."
  for machine_dir in tests/features/machine?;do
    for feature in $machine_dir/*.feature; do
      echo $feature
      aloe $feature --nologcapture -v
    done
  done
fi

timeout 10 iri-network-tests/teardown_cluster.sh -r $REVISION_HASH
exit $ERROR
