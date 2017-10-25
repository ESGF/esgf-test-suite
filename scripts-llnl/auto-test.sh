export TERM="vt100"
ntpdate -u 0.centos.pool.ntp.org
cd /usr/local/bin/
rm -rf *
wget http://aims1.llnl.gov/esgf/dist/esgf-installer/2.5/esg-bootstrap
bash esg-bootstrap
cp /tmp/esg-autoinstall-full.conf ../etc/esg-autoinstall.conf
./esg-autoinstall 2>&1 | tee install-log-2.5.17-full
expect /tmp/auto-keypair.exp 2>&1 | tee keypair-inst.log
esg-node restart
source /usr/local/conda/bin/activate esgf-pub
export UVCDAT_ANONYMOUS_LOG=no
esgtest_publish 2>&1 | tee publish-test.log
python /tmp/node_tests.py 2>&1 | tee http-tests.log
esg-node status 2>&1 | tee node-status.log  