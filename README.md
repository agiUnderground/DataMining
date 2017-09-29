# DataMining | ETL project

![](static/img/datamining.gif?raw=true)


### Dependencies

* Selenium
* Lxml
* Hug
* Psycopg2
* Peewee

### Usage

* Crawler

Help:
```python3 crawler.py -h or --help```

Example:
```python3 crawler.py https://www.snap.com/en-US/jobs/ snap.html```

Result:

file - snap.html

* Extractor

Help:
```python3 extractor.py -h```

Example:
```python3 extractor.py snap.html snap.csv```

Result:

file - snap.csv

* Loader

Example:
```./ETL.sh /DataMining/Loader/jobs.csv```

* API

Example:
```hug -f api.py -p 8080```
