CREATE SCHEMA schema_snap AUTHORIZATION snap_user
	CREATE TABLE jobs (title text, category text, status text, location text)
	GRANT ALL ON jobs TO snap_user
