#!/usr/bin/env bash
mkdir .deploy || true
export DAPP_SLUG=`dapp slug $CI_COMMIT_REF_NAME`
if [ $NAMESPACE == "production" ]; then export NODESELECTOR=production; fi;
for f in .kube/*.yaml
do
 envsubst < $f > ".deploy/$(basename $f)"
done
