
# R53DynDNS

![build status](https://travis-ci.org/dron22/r53dyndns.svg?branch=master)

Simple Dynamic DNS with AWS Route53

If you need a simple DynDNS solution and you are already on AWS, why not use
their Route53 service to set it up yourself. R53DynDNS provides you with a
simple solution to set up you own DNS.


### Install

        sudo pip install r53dyndns


### Usage

        r53dyndns -z <ZONE> -d <DNS>

        e.g.

        r53dyndns -z domain.com -d sub.domain.com


### Authentication

R53DynDNS uses the python boto module as an interface to AWS which need two
environment variables for authentication

        AWS_ACCESS_KEY_ID
        AWS_SECRET_ACCESS_KEY


### Limitations

AWS Route53 service has a minimum ttl of 60 seconds. This might be a problem
in Production, but for a lot of solutions it is not.
