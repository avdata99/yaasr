
sudo supervisorctl stop yaasr-fm1023-universidad-cordoba
sudo supervisorctl stop yaasr-radio-bio-bio-santiago-chile
sudo supervisorctl stop yaasr-radio-universidad-cordoba-argentina

rm -f /home/cluster311/yaasr/*.aac

sudo supervisorctl start yaasr-fm1023-universidad-cordoba
sudo supervisorctl start yaasr-radio-bio-bio-santiago-chile
sudo supervisorctl start yaasr-radio-universidad-cordoba-argentina

tail -f /var/log/yaasr-*.log
