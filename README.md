# JsonToGraphite
Graphite Setup and Json converter + instructions

### Installing Grafana/Graphite:
```
$ wget https://s3-us-west-2.amazonaws.com/grafana-releases/release/grafana-4.X.X-X.x86_64.rpm
$ yum install grafana-4.X.X-X.x86_64.rpm
```

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
