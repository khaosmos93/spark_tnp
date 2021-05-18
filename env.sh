LCG_RELEASE=LCG_97apython3
LCG_ARCH=x86_64-centos7-gcc8
source /cvmfs/sft.cern.ch/lcg/views/${LCG_RELEASE}/${LCG_ARCH}-opt/setup.sh

if [[ "$HOSTNAME" == *"ithdp"* ]]; then
  # edge node
  echo "Sourcing hadoop edge node environment..."
  source hadoop-setconf.sh analytix
  echo "Done!"
elif [[ "$HOSTNAME" == *"lxplus"* ]]; then
  # lxplus
  echo "Sourcing lxplus environment..."
  source /cvmfs/sft.cern.ch/lcg/etc/hadoop-confext/hadoop-swan-setconf.sh analytix
  echo "Done!"
else
  echo "ERROR setting up environment! Environment can only be lxplus or the CERN hadoop edge nodes. See README for more details"
fi
