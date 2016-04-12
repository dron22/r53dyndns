# -*- coding: utf-8 -*-

import pytest

import r53dyndns.r53dyndns as r53dyndns
from r53dyndns.r53dyndns import IpDetector


IP = '189.192.168.1'


@pytest.fixture(scope='function')
def mocks(monkeypatch):

    class JsonResponse:
        def json(self):
            return {'ip': IP}

    class PlainResponse:
        text = IP

    def get(url):
        plain_urls = [
            "http://ip.dnsexit.com/",
            "http://ip1.dynupdate.no-ip.com/",
            "http://ip2.dynupdate.no-ip.com/",
            "http://ipv4.icanhazip.com/",
        ]
        json_urls = [
            "http://jsonip.com/",
        ]
        if url in plain_urls:
            return PlainResponse()
        if url in json_urls:
            return JsonResponse()

    monkeypatch.setattr(
        r53dyndns.requests,
        'get',
        get
    )


@pytest.fixture(scope='function')
def ipdetector(monkeypatch):
    return IpDetector()


def test_detect(mocks, ipdetector):
    for i in range(10):
        ip = ipdetector.detect()
        assert ip == IP
