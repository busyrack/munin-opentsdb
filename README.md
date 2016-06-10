# munin-opentsdb
Collect Munin metrics, convert and push them into OpenTSDB

## Usage
```
Munin collector to OpenTSDB

Usage: munin-collector.py (options)

Options:
    -T --opentsdb-host <opentsdb host>      OpenTSDB host name or IP
    -P --opentsdb-port <opentsdb port>      OpenTSDB port
    -M --munin-nodes <munin nodes>          List of Munin nodes separated by comma.
                                            Example: server1:4949,server2:4949
```

## Examples
```
nohup python munin-collector.py -T 192.168.0.10 -P 4242 -M server1:4949,server2:4949,server3:4949 &
```
