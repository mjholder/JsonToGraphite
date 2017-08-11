# JsonToGraphite
Graphite Setup and Json converter + instructions

### Dependencies
Note: This was created on a Centos 7.3 system and most of the commands will require root privilages/sudo

* Python-cffi
```
   # yum install python-cffi
```
* Pip
```
   # yum install python-pip
```
* Django 
``` 
   # pip install django
```
* Django-Tagging
```
   # pip install django-tagging
```
* Pyparsing
```
   # pip install pyparsing
```
* Cairo
```
   # yum install cairo-devel
```
* Pycairo
```
   # yum install pycairo-devel
```
* Cairo-cffi
```
   # yum install cairocffi
```
* Scandir
```
   # yum install python-scandir
```

### Installing Grafana/Graphite:
Install Grafana
```
# wget https://s3-us-west-2.amazonaws.com/grafana-releases/release/grafana-4.X.X-X.x86_64.rpm
# yum install grafana-4.X.X-X.x86_64.rpm
```
Install Graphite
```
# yum groupinstall "Development Tools"
# yum install python-devel
# yum install git
# pip install twisted
# cd /tmp
# git clone https://github.com/graphite-project/carbon.git
# cd /tmp/carbon
# python setup.py install
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
Install Whisper
```
# cd /tmp
# git clone https://github.com/graphite-project/whisper.git
# cd /tmp/whisper
# python setup.py install
```
Next you need to start the carbon-cache script. This script starts the connection between carbon's whisper database and the JsonToGraphite script.
```
# cd /opt/graphite/bin
# ./carbon-cache.py start
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
# python setup.py install
```
Next copy the local_settings file. Modify this file if you want to change any of the Webapp settings
```
# cd /opt/graphite/webapp/graphite
# cp local_settings.py.example local_settings.py
```
Be sure to uncomment DEBUG=True in local_settings.py, otherwise certain parts of the graphite web page won't appear and you will get 404 errors in the log.

To run the Webapp use the following commands
```
# export PYTHONPATH=$PYTHONPATH:/webapp
# PYTHONPATH=/opt/graphite/webapp django-admin.py migrate --settings=graphite.settings --run-syncdb
# cd /opt/graphite
# PYTHONPATH=/whisper ./bin/run-graphite-devel-server.py --libs=/webapp/ /opt/graphite/
```
By default the Webapp will run on port 8080, this can be changed by adding "--port=(port number)". I.e. running on port 8585
```
# PYTHONPATH=/whisper ./bin/run-graite-devel-server.py --libs=/webapp/ /opt/graphite/ --port=8585
```
### Installing and using JsonToCarbon
To install, go to the directory where setup.py is located and run
```
# python setup.py bdist_rpm
```
And to install the rpm run
```
# yum install dist/JsonToCarbon-x.x_x.noarch.rpm
```
Before running JsonToCarbon make sure carbon-cache is running and the json file you want to import to Graphite is in the same directory you are in. To run JsonToCarbon use
```
JsonToCarbon -f filename
```
Use the argument -h for help
### Using Grafana
Start Grafana with
```
# service grafana-server start
```
If you want Grafana to start on boot run
```
# systemctl enable grafana-server.service
```
Next to access Grafana, on a browser go to whatever ip and port you chose in grafana.ini earlier, or the default is 0.0.0.0:3000.

Login or create an account

Then when creating a data source, select graphite as the type, the source should be whatever you have the graphite running on (default being 0.0.0.0:8080), and make sure the access type is proxy.

When saving the datasource it will automatically check if the datasource works.

And that's it!

More info on how to use Grafana/Graphite can be found here
> http://docs.grafana.org/features/datasources/graphite/

and 

> http://docs.grafana.org/guides/getting_started/
