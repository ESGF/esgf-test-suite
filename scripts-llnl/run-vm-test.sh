major=$1
minor=$2

devel=$3

vminst=/export_backup/ames4/vmware/esgf-dev1_on_grim/esgf-dev1_on_grim.vmx

snap=preinstall

target=root@esgf-dev1

vmrun revertToSnapshot $vminst $snap
vmrun start $vminst nogui
vmrun unpause $vminst

sleep 60

# deploy the conf
# scp the key
# fetch and run the bootstrap

scp esg-autoinstall-full.conf $target:/tmp
scp auto-test.sh $target:/tmp
scp auto-deploy.sh $target:/tmp
scp auto-keypair.sh $target:/tmp
scp auto-keypair.exp $target:/tmp
scp pcmdi8.key cert.cer.txt cachain.pem $target:/tmp
scp node_tests.py $target:/tmp

ssh $target "bash /tmp/auto-deploy.sh $major $minor $devel"


ssh $target "bash /tmp/auto-keypair.sh"
ssh $target "esg-node restart"

ssh $target "bash auto-test.sh"

datestr=`date | sed s/\ /_/g`

logdir="log-$datestr"

mkdir $logdir

pushd $logdir

scp $target:/usr/local/bin/install-log-$major.$minor-$devel-full .
scp $target:/tmp/keypair-inst.log .
scp $target:/tmp/publish-test.log .
scp $target:/tmp/http-tests.log .
scp $target:/tmp/node-status.log .

popd





