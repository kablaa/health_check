# System Health Check
Also gotta install the `tw_cli`. Good luck finding it
```
sudo -i
apt-get install lm-sensoro 
oensors-detect
modprobe ipmi_devintf
modprobe ipmi_si
mv system_health_check.py /usr/bin/
mv system_health_check.service /etc/systemd/system/
systemctl daemon-reload 
systemctl enable system_health_check.service
systemctl start system_health_check.service
```
