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
Next you need to start the carbon-cache script. This script starts the connection between carbon's whisper database and the JsonToGraphite script.
```
# cd /opt/graphite/bin
# service carbon-cache.py start
```
By default Grafana uses port 3000 and the carbon-cache uses port 2004. 

To change the port used by Grafana, edit in /etc/grafana/grafana.ini the http_port variable under the [server] section. 

To change the carbon-cache port, edit in /opt/graphite/conf/carbon.conf the PICKLE_RECEIVER_PORT number.
### Installing and running the Graphite Webapp
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
Next copy the local_settings file. Modify this file if you want to change any of the Webapp settings
```
# cd /opt/graphite/webapp/graphite
# cp local_settings.py.example local_settings.py
```
To run the Webapp use the following commands
```
# cd /opt/graphite
# PYTHONPATH=/whisper ./bin/run-graite-devel-server.py --libs=/webapp/ /opt/graphite/
```
By default the Webapp will run on port 8080, this can be changed by adding "--port=(port number)". I.e. running on port 8585
```
#  PYTHONPATH=/whisper ./bin/run-graite-devel-server.py --libs=/webapp/ /opt/graphite/ --port=8585
```
