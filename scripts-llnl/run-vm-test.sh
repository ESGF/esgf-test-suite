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
scp auto-keypair.exp $target:/tmp
scp pcmdi8.key cert.cer.txt cachain.pe $target:/tmp
scp node_tests.py $target:/tmp

ssh $target "bash /tmp/auto-test.sh"


datestr=`date | sed s/\ /_/g`

logdir="log-$datestr"

mkdir $logdir

pushd $logdir

scp $target:/usr/local/bin/install-log-2.5.17-full .
scp $target:/usr/local/bin/keypair-inst.log .
scp $target:/usr/local/bin/publish-test.log .
scp $target:/usr/local/bin/http-test.log .

popd





