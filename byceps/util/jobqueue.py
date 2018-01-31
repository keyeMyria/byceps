"""
byceps.util.jobqueue
~~~~~~~~~~~~~~~~~~~~

An asynchronously processed job queue based on Redis_ and RQ_.

.. _Redis: http://redis.io/
.. _RQ:    http://python-rq.org/

:Copyright: 2006-2018 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

from contextlib import contextmanager

from flask import current_app
from rq import Connection, Queue

from byceps.redis import redis


@contextmanager
def connection():
    with Connection(redis.client):
        yield


def get_queue():
    async = current_app.config['JOBS_ASYNC']
    return Queue(async=async)


def enqueue(*args, **kwargs):
    """Add the function call to the queue as a job."""
    with connection():
        queue = get_queue()
        queue.enqueue(*args, **kwargs)
