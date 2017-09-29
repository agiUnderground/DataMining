import hug
import sys
import pytest
from api import *
from falcon import HTTP_400, HTTP_404, HTTP_200
from hug.redirect import *
import logging

logger = logging.getLogger('peewee')
logger.setLevel(logging.ERROR)
logger.addHandler(logging.StreamHandler())


def test_jobs_endpoint():

    response = hug.test.get(api, 'jobs/Seattle')

    assert response.status == HTTP_200
    assert response.data is not None

    response = hug.test.get(api, 'jobs/London')

    assert response.status == HTTP_200
    assert response.data is not None


def test_jobs_inval():

    response = hug.test.get(api, 'jobs/doNotExists')

    assert response.status == HTTP_404

    response = hug.test.get(api, 'jobs/\'235gq35g45g54"f341g535g')
    assert response.status == HTTP_404
