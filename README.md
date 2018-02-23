```
sudo -i
apt-get install lm-sensors 
sensors-detect
mv system_health_check.py /usr/bin/
mv system_health_check.service /etc/systemd/system/
systemctl daemon-reload 
systemctl enable system_health_check.service
systemctl start system_health_check.service
```
