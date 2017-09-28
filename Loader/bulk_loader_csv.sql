COPY schema_snap.jobs ("title", "category", "status", "location") 
FROM :filename DELIMITER ',' CSV HEADER;
