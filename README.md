# Cloud IP Ranges

## Description

Most cloud providers publish up to date lists of their IP address ranges. This tools identifies if an IP belongs to a provider's ranges by fetching and parsing the latest lists.

Supports:

- [x] AWS ([source](https://ip-ranges.amazonaws.com/ip-ranges.json)) 
- [x] Azure ([source](https://www.microsoft.com/en-us/download/confirmation.aspx?id=56519))
- [x] Google Cloud Platform ([source](https://www.gstatic.com/ipranges/cloud.json))
- [ ] Alibaba Cloud (currently doesn't publish lists)
- [x] Oracle Cloud Infrastructure ([source](https://docs.cloud.oracle.com/en-us/iaas/tools/public_ip_ranges.json))
- [ ] IBM Cloud (currently doesn't publish lists)
- [x] DigitalOcean ([source](http://digitalocean.com/geo/google.csv))

This tool is inspired by [Nimbusland](https://gist.github.com/TweekFawkes/ff83fe294f82f6d73c3ad14697e43ad5) by [Bryce Kunz](http://www.brycekunz.com/).

## Usage

Setup a virtual environment and install dependencies:

```shell script
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ pip -r requirements.txt
```

Run the tool:

```shell script
$ python cloud_ip_ranges.py -h

usage: cloud_ip_ranges.py [-h] [-q] ip

positional arguments:
  ip           The IP to evaluate, e.g.: 8.8.8.8

optional arguments:
  -h, --help   show this help message and exit
  -q, --quiet  Suppress logging output

$ python cloud_ip_ranges.py 52.4.0.0

2020-09-18 17:38:42 host __main__[21549] INFO Starting
2020-09-18 17:38:42 host __main__[21549] INFO Checking for AWS
2020-09-18 17:38:43 host __main__[21549] INFO Match for AWS range "52.4.0.0/14", region "us-east-1" and service "AMAZON"
2020-09-18 17:38:43 host __main__[21549] INFO Match for AWS range "52.4.0.0/14", region "us-east-1" and service "EC2"
2020-09-18 17:38:43 host __main__[21549] INFO Checking for Azure
2020-09-18 17:38:44 host __main__[21549] INFO Checking for GCP
2020-09-18 17:38:44 host __main__[21549] INFO Checking for OCI
2020-09-18 17:38:44 host __main__[21549] INFO Done
```
