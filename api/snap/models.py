import peewee
import datetime
import os
import logging
from peewee import *
from playhouse.postgres_ext import *
from playhouse.pool import PooledPostgresqlExtDatabase

POSTGRES_USER = os.environ['POSTGRES_USER']
POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']
POSTGRES_DB_NAME = os.environ['POSTGRES_DB_NAME']
POSTGRES_HOST = os.environ['POSTGRES_HOST']


database = PooledPostgresqlExtDatabase(POSTGRES_DB_NAME,
                                       user=POSTGRES_USER,
                                       password=POSTGRES_PASSWORD,
                                       host=POSTGRES_HOST,
                                       server_side_cursors=True,
                                       max_connections=2000,
                                       stale_timeout=300)  # 5 min

logger = logging.getLogger('snap.models')


class Jobs(peewee.Model):
    title = peewee.CharField()
    category = peewee.CharField()
    status = peewee.CharField()
    location = peewee.CharField()

    class Meta:
        database = database
        primary_key = False
        schema = 'schema_snap'

if __name__ == "__main__":

    # Connect to our database.
    database.connect()
    # Create schemas
    try:
        database.create_tables([Jobs], safe=True)
    except peewee.OperationalError as e:
        logger.warn('Creating db scheme. Failed to create table Jobs'
                    ' or it already exist.')
