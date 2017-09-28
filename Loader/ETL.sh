#/bin/bash

PGPASSWORD=snap_user psql -U snap_user -h localhost -d test -a -f run_insert.sql
PGPASSWORD=snap_user psql -U snap_user -h localhost -d test -a -v filename="'$1'" -f bulk_loader_csv.sql
