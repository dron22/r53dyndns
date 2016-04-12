# -*- coding: utf-8 -*-

import pytest
from mock import Mock

import r53dyndns.r53dyndns as r53dyndns
from r53dyndns.r53dyndns import R53Updater

ZONE = 'r53zone.com'
DNS = 'test.r53zone.com'
IPS = ['188.192.168.1', '217.192.168.1', '217.192.168.1']


@pytest.fixture(scope='function')
def boto_status():
    status_mock = Mock()
    status_mock.get_status.side_effect = ['PENDING', 'INSYNC']

    def update():
        status_mock.status = status_mock.get_status()

    status_mock.update.side_effect = update
    status_mock.status = 'PENDING'
    return status_mock


@pytest.fixture(scope='function')
def boto_zone(boto_status):
    class Record:
        def __init__(self, value, ttl):
            self.resource_records = [value]

    class Zone:
        def __init__(self, name):
            self.name = name
            self.records = {}

        def update_a(self, name, value, ttl):
            self.records[name] = Record(value=value, ttl=ttl)
            return boto_status

        def add_a(self, name, value, ttl):
            self.records[name] = Record(value=value, ttl=ttl)
            return boto_status

        def get_a(self, name):
            return self.records.get(name)

    return Zone(ZONE)


@pytest.fixture(scope='function')
def boto_connection(boto_zone):
    connection_mock = Mock()
    func = lambda x: boto_zone if x == 'r53zone.com' else exit(1)
    connection_mock.get_zone.side_effect = func
    return connection_mock


@pytest.fixture(scope='function')
def r53updater(monkeypatch, boto_connection):
    get_ip_mock = Mock(side_effect=IPS)
    monkeypatch.setattr(
        r53dyndns,
        'get_ip',
        get_ip_mock
    )
    monkeypatch.setattr(
        r53dyndns.boto.route53.connection,
        'Route53Connection',
        Mock(return_value=boto_connection)
    )
    return R53Updater(ZONE)


def test_r53updater(r53updater, boto_zone):

    r53dyndns.update(ZONE, DNS)
    assert len(boto_zone.records[DNS].resource_records) == 1
    assert boto_zone.records[DNS].resource_records[0] == IPS[0]

    r53dyndns.update(ZONE, DNS)
    assert len(boto_zone.records[DNS].resource_records) == 1
    assert boto_zone.records[DNS].resource_records[0] == IPS[1]

    r53dyndns.update(ZONE, DNS)
    assert len(boto_zone.records[DNS].resource_records) == 1
    assert boto_zone.records[DNS].resource_records[0] == IPS[1]
