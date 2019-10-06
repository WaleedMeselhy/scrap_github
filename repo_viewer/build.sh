#!/usr/bin/env bash

set -e

if [ "x$cloudprovider" = "xaws" ] ; then
  echo Building for AWS
  build_args="--build-arg cloudprovider=$cloudprovider --build-arg CUSTOMER_SITE=$CUSTOMER_SITE --build-arg CYTHONIZE=$CYTHONIZE"
else
  build_args="--build-arg CUSTOMER_SITE=$CUSTOMER_SITE --build-arg CYTHONIZE=$CYTHONIZE"
fi

cd "$(dirname "$0")"
cp -rf ../../core .
cp ../../../setup.py .


if [ "x$localdev" = "xtrue" ]; then
    docker build $build_args -t balance_viewer_v2 .
else
    docker build $build_args -t __system_docker_registry_address__/balance_viewer_v2 .
    docker push __system_docker_registry_address__/balance_viewer_v2
fi

rm -rf ./core