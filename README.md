
# R53DynDNS

![build status](https://travis-ci.org/dron22/r53dyndns.svg?branch=master)

Simple Dynamic DNS with AWS Route53

If you need a simple DynDNS solution and you are already on AWS, why not use
their Route53 service to set it up yourself? R53DynDNS provides you with a
simple solution to set up you own DNS.


### Install

    pip install r53dyndns


### Usage

    r53dyndns -z <ZONE> -d <DNS> [-t <TTL>]

    r53dyndns -z domain.com -d sub.domain.com -t 30


### Authentication

R53DynDNS uses the python boto module as an interface to AWS which need two
environment variables for authentication

    AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY


### AWS Route53 pricing

> as of Apr. 13th

* Hosted Zones

    $0.50 per hosted zone / month for the first 25 hosted zones  
    $0.10 per hosted zone / month for additional hosted zones

* Standard Queries

    $0.400 per million queries – first 1 Billion queries / month  
    $0.200 per million queries – over 1 Billion queries / month

