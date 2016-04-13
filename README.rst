
R53DynDNS
============

Simple Dynamic DNS with AWS Route53

.. image:: https://travis-ci.org/dron22/r53dyndns.svg?branch=master
    :alt: travis-status


QuickStart
---------------

1. Install

.. sourcecode:: bash

    $ pip install r53dyndns

2. Set environment variables

.. sourcecode:: bash

    export AWS_ACCESS_KEY_ID="<AWS_KEY>"
    export AWS_SECRET_ACCESS_KEY="<AWS_SECRET_KEY>"

3. Run script
 
.. sourcecode:: bash

    $ r53dyndns -z <ZONE> -d <DNS> [-t <TTL>]

    $ r53dyndns -z domain.com -d sub.domain.com -t 30

 
AWS Route53 pricing (as of Apr. 13th 2016)
--------------------

AWS Pricing is cheap and there won't be significant costs.

* Hosted Zones

    $0.50 per hosted zone / month for the first 25 hosted zones
    
    $0.10 per hosted zone / month for additional hosted zones

* Standard Queries

    $0.400 per million queries – first 1 Billion queries / month  
    
    $0.200 per million queries – over 1 Billion queries / month


License
---------

`MIT <https://opensource.org/licenses/mit-license.html>`_

