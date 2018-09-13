export TERM="vt100"
source /usr/local/conda/bin/activate esgf-pub
export UVCDAT_ANONYMOUS_LOG=no
esgtest_publish 2>&1 > publish-test.log
python /tmp/node_tests.py 2>&1 > http-tests.log
esg-node status 2>&1 > node-status.log  