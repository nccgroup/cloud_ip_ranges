#!/usr/bin/python3

from argparse import ArgumentParser
import requests
from netaddr import IPNetwork, IPAddress
import json
from lxml import html
import coloredlogs, logging


def match_aws(target_ip):
    try:
        logger.info('Checking for AWS')
        aws_url = 'https://ip-ranges.amazonaws.com/ip-ranges.json'
        aws_ips = json.loads(requests.get(aws_url, allow_redirects=True).content)

        for item in aws_ips["prefixes"]:
            if IPAddress(target_ip) in IPNetwork(str(item["ip_prefix"])):
                logger.info('Match for AWS range "{}", region "{}" and service "{}"'.format(item['ip_prefix'],
                                                                                            item['region'],
                                                                                            item['service']))

    except Exception as e:
        logger.error('Error: {}'.format(e))


def match_azure(target_ip):
    try:
        logger.info('Checking for Azure')
        azure_url = 'https://www.microsoft.com/en-us/download/confirmation.aspx?id=56519'
        page = requests.get(azure_url)
        tree = html.fromstring(page.content)
        download_url = \
            tree.xpath("//a[contains(@class, 'failoverLink') and "
                       "contains(@href,'download.microsoft.com/download/')]/@href")[0]

        azure_ips = json.loads(requests.get(download_url, allow_redirects=True).content)

        for item in azure_ips["values"]:
            for prefix in item["properties"]['addressPrefixes']:
                if IPAddress(target_ip) in IPNetwork(str(prefix)):
                    logger.info('Match for Azure range "{}", region "{}" and service "{}"'.format(prefix,
                                                                                                  item["properties"][
                                                                                                      "region"],
                                                                                                  item["properties"][
                                                                                                      "systemService"]))

    except Exception as e:
        logger.error('Error: {}'.format(e))


def match_gcp(target_ip):
    try:
        logger.info('Checking for GCP')
        gcp_url = 'https://www.gstatic.com/ipranges/cloud.json'
        gcp_ips = json.loads(requests.get(gcp_url, allow_redirects=True).content)

        for item in gcp_ips["prefixes"]:
            if IPAddress(target_ip) in IPNetwork(str(item.get("ipv4Prefix", item.get("ipv6Prefix")))):
                # return [target_ip, str(item["ipv4Prefix"]), str(item["scope"]), 'GCP', str(item["service"])]
                logger.info('Match for GCP range "{}", region "{}" and service "{}"'.format(
                    item.get("ipv4Prefix", item.get("ipv6Prefix")),
                    item['scope'],
                    item['service']))

    except Exception as e:
        logger.error('Error: {}'.format(e))


def match_oci(target_ip):
    try:
        logger.info('Checking for OCI')
        oci_url = 'https://docs.cloud.oracle.com/en-us/iaas/tools/public_ip_ranges.json'
        oci_ips = json.loads(requests.get(oci_url, allow_redirects=True).content)

        for region in oci_ips["regions"]:
            for cidr_item in region['cidrs']:
                if IPAddress(target_ip) in IPNetwork(str(cidr_item["cidr"])):
                    # return [target_ip, str(cidr_item["cidr"]), str(region['region']), 'OCI', str(cidr_item["tags"][-1])]
                    logger.info('Match for OCI range "{}", region "{}" and service "{}"'.format(cidr_item['cidr'],
                                                                                                region['region'],
                                                                                                cidr_item["tags"][-1]))

    except Exception as e:
        logger.error('Error: {}'.format(e))


logger = logging.getLogger(__name__)
coloredlogs.install(level='info')

if __name__ == "__main__":
    logger.info('Starting')

    parser = ArgumentParser(add_help=True)

    parser.add_argument('ip',
                        help="The IP to evaluate, e.g.: 8.8.8.8")

    args = parser.parse_args()

    match_aws(args.ip)
    match_azure(args.ip)
    match_gcp(args.ip)
    match_oci(args.ip)

    logger.info('Done')
