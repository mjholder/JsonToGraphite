# JsonToGraphite
Graphite Setup and Json converter + instructions

### Installing Grafana/Graphite:
```
# wget https://s3-us-west-2.amazonaws.com/grafana-releases/release/grafana-4.X.X-X.x86_64.rpm
# yum install grafana-4.X.X-X.x86_64.rpm
```
Next copy the example configuration files
```
# cd /opt/graphite/conf
# cp aggregation-rules.conf.example aggregation-rules.conf
# cp blacklist.conf.example blacklist.conf
# cp carbon.conf.example carbon.conf
# cp carbon.amqp.conf.example carbon.amqp.conf
# cp relay-rules.conf.example relay-rules.conf
# cp rewrite-rules.conf.example rewrite-rules.conf
# cp storage-schemas.conf.example storage-schemas.conf
# cp storage-aggregation.conf.example storage-aggregation.conf
# cp whitelist.conf.example whitelist.conf
```
### Installing the Graphite Webapp
```
# cd /tmp
# git clone https://github.com/graphite-project/graphite-web.git
# cd /tmp/graphite-web
```
To check if you installed all the dependencies use
```
# python check-dependencies.py
```
If no "REQUIRED" dependency messages print then run
```
# sudo python setup.py install
```
Next copy the local_settings file
```
# cd /opt/graphite/webapp/graphite
# cp local_settings.py.example local_settings.py
```
Modify this file if you want to change any of the Webapp settings
