export TERM="vt100"

devel=$3

ntpdate -u 0.centos.pool.ntp.org
cd /usr/local/bin/
rm -rf *
wget http://aims1.llnl.gov/esgf/dist/devel/$1/$2/esgf-installer/esg-bootstrap
if [ ! -z $devel ] ; then
    wget http://aims1.llnl.gov/esgf/dist/devel/$1/$2/esgf-installer/esg-bootstrap
    bash esg-bootstrap --devel
else
    wget http://aims1.llnl.gov/esgf/dist/$1/$2/esgf-installer/esg-bootstrap
    bash esg-bootstrap
fi

cp /tmp/esg-autoinstall-full.conf ../etc/esg-autoinstall.conf
./esg-autoinstall 2>&1 > install-log-$1.$2.log

