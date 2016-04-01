# -*- coding: utf-8 -*-

import os
import sys
import time
import requests
import argparse
import boto.route53

# configs
TTL = 60
TMP_FILE = '/tmp/r53dyndns.tmp'


def get_myip():
    r = requests.get(r'http://jsonip.com')
    ip = r.json()['ip']
    return ip


def did_ip_change(ip):
    if os.path.isfile(TMP_FILE):
        with open(TMP_FILE) as f:
            content = f.read()
        old_ip = content.strip()
        if ip == old_ip:
            return False
    with open(TMP_FILE, 'w') as f:
        f.write(ip)
    return True


def wait_for_success(status):
    turning_pipe = ['|', '/', '-', '\\']
    idx = 0
    while status.status == 'PENDING':
        sys.stdout.write('%s\r' % turning_pipe[idx % 4]) 
        sys.stdout.flush()
        idx += 1
        status.update()
        time.sleep(0.1)
    print(status.status)


def get_zone(aws_r53_zone):
    conn = boto.route53.connection.Route53Connection()
    return conn.get_zone(aws_r53_zone)


def main():
    
    for i in ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY']:
        if not os.environ.get(i):
            print('Environment variable \'%s\' is required.' % i)
            exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument('-z', '--zone', metavar='<ZONE>', required=True)
    parser.add_argument('-d', '--dns', metavar='<DNS_NAME>', required=True)

    args = parser.parse_args()
    aws_r53_zone = args.zone
    dns_name = args.dns

    myip = get_myip()
    if did_ip_change(myip):
        zone = get_zone(aws_r53_zone)
        record = zone.get_a(dns_name)
        if record:
            status = zone.update_a(name=dns_name, value=myip, ttl=TTL)
            wait_for_success(status)
        else:
            status = zone.add_a(name=dns_name, value=myip, ttl=TTL)
            wait_for_success(status)
    else:
        print('IP did not change')


if __name__ == "__main__":
    main()
