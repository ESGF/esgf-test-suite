export TERM="vt100"
ntpdate -u 0.centos.pool.ntp.org
cd /usr/local/bin/
rm -rf *
wget http://aims1.llnl.gov/esgf/dist/devel/esgf-installer/$1/esg-bootstrap
bash esg-bootstrap --devel
cp /tmp/esg-autoinstall-full.conf ../etc/esg-autoinstall.conf
./esg-autoinstall 2>&1 > install-log-$1.$2.log

