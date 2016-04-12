# -*- coding: utf-8 -*-

import sys
import time
import random
import requests
import boto.route53


class IpDetector:

    def __init__(self):
        self.urls = [
            ("http://ip.dnsexit.com/", 'plain'),
            ("http://ip1.dynupdate.no-ip.com/", "plain"),
            ("http://ip2.dynupdate.no-ip.com/", "plain"),
            ("http://ipv4.icanhazip.com/", 'plain'),
            ("http://jsonip.com/", 'jsonip'),
        ]

    def detect(self):
        random.shuffle(self.urls)
        for url, parser_name in self.urls:
            parser = getattr(self, 'parser_' + parser_name)
            try:
                r = requests.get(url)
            except Exception as e:
                print(e)
                continue
            ip = parser(r)
            break
        return ip

    def parser_plain(self, response):
        return response.text.strip()

    def parser_jsonip(self, response):
        return response.json()['ip'].strip()


class R53Updater:

    def __init__(self, zone):
        self.zone = self.get_zone(zone)

    def get_zone(self, aws_r53_zone):
        conn = boto.route53.connection.Route53Connection()
        return conn.get_zone(aws_r53_zone)

    def update_dyndns(self, dns, ip, ttl):
        record = self.zone.get_a(dns)
        print('Set "%s" to ip: %s' % (dns, ip))
        if record:
            status = self.zone.update_a(name=dns, value=ip, ttl=ttl)
            self.wait_for_success(status)
        else:
            status = self.zone.add_a(name=dns, value=ip, ttl=ttl)
            self.wait_for_success(status)

    def did_ip_change(self, dns, ip):
        record = self.zone.get_a(dns)
        if record and ip in record.resource_records:
            return False
        return True

    def wait_for_success(self, status):
        turning_pipe = ['|', '/', '-', '\\']
        idx = 0
        while status.status == 'PENDING':
            sys.stdout.write('%s\r' % turning_pipe[idx % 4])
            sys.stdout.flush()
            idx += 1
            status.update()
            time.sleep(0.1)
        if status.status == 'INSYNC':
            print('Completed successfully')
        else:
            print('Error: %s' % status.status)


def get_ip():
    ip_detector = IpDetector()
    return ip_detector.detect()


def update(zone, dns, ttl):
    ip = get_ip()
    updater = R53Updater(zone)
    if updater.did_ip_change(dns=dns, ip=ip):
        updater.update_dyndns(dns=dns, ip=ip, ttl=ttl)
    else:
        print('IP did not change')
