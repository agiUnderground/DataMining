import hug
from hug.redirect import *
from snap.models import *
from io import StringIO
import csv

hug.API(__name__).http.output_format = hug.output_format.text


@hug.get('/jobs/{location}')
def open_job_positions(location: hug.types.text):

    # with ORM we can simply get data like this:
    jobs = Jobs.select().where(Jobs.location == location)

    # with row sql - SQL INJ PSBL!!!
    '''
    request = "select * from schema_snap.jobs where" \
              " schema_snap.jobs.location='{}';".format(str(location))
    jobs = database.execute_sql(request)
    '''
    resp = StringIO()
    writer = csv.writer(resp)

    with database.transaction():
        if not jobs.exists():
            return not_found()
        for elem in jobs.naive():
            elem = [elem.title, elem.category, elem.status, elem.location]
            writer.writerow(elem)

    sresp = resp.getvalue().strip('\r\n')
    return sresp
