.. image:: https://img.shields.io/pypi/v/dwave-cloud-client.svg
    :target: https://pypi.python.org/pypi/dwave-cloud-client

.. image:: https://travis-ci.org/dwavesystems/dwave-cloud-client.svg?branch=master
    :target: https://travis-ci.org/dwavesystems/dwave-cloud-client
    :alt: Travis Status

.. image:: https://coveralls.io/repos/github/dwavesystems/dwave-cloud-client/badge.svg?branch=master
    :target: https://coveralls.io/github/dwavesystems/dwave-cloud-client?branch=master
    :alt: Coverage Report

.. image:: https://readthedocs.org/projects/dwave-cloud-client/badge/?version=latest
    :target: http://dwave-cloud-client.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. index-start-marker

D-Wave Cloud Client
===================

A minimal implementation of the REST interface used to communicate with
D-Wave Sampler API (SAPI) servers.

SAPI is an application layer built to provide resource discovery, permissions,
and scheduling for quantum annealing resources at D-Wave Systems.
This package aims to provide a minimal Python interface to that layer that
still captures some reasonable practices for interacting with SAPI.


Example
-------

.. code-block:: python

    import random
    from dwave.cloud import Client

    # Connect using the default or environment connection information
    with Client.from_config() as client:

        # Load the default solver
        solver = client.get_solver()

        # Build a random Ising model on +1, -1. Build it to exactly fit the graph the solver provides
        linear = {index: random.choice([-1, 1]) for index in solver.nodes}
        quad = {key: random.choice([-1, 1]) for key in solver.undirected_edges}

        # Send the problem for sampling, include a solver specific parameter 'num_reads'
        computation = solver.sample_ising(linear, quad, num_reads=100)

        # Print out the first sample (out of a hundred)
        print(computation.samples[0])

.. index-end-marker


Installation
------------

.. installation-start-marker

Compatible with Python 2 and 3:

.. code-block:: bash

    pip install dwave-cloud-client

To install from source (available on GitHub in `dwavesystems/dwave-cloud-client`_ repo):

.. code-block:: bash

    pip install -r requirements.txt
    python setup.py install

.. _`dwavesystems/dwave-cloud-client`: https://github.com/dwavesystems/dwave-cloud-client

.. installation-end-marker


License
-------

Released under the Apache License 2.0. See LICENSE file.


Contribution
------------

See CONTRIBUTING.rst file.
