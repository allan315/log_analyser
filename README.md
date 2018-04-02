# Udacity nano degree log analyzer project
This is a command line tool written in Python which analyzes a news database to show some of the statistics of a webpage
## 
In order to use this code database should have these views:
1. create view view_count as select replace(path, '/article/', '') as slug, count(*) from log group by slug;
2. create view ok as select time::timestamp::date as date, status, count(*) from log where status like '200%' group by date, status;
3. create view errors as select time::timestamp::date as date, status, count(*) from log where status like '404%' group by date, status;

Run the script file from command line: 

pyhton loganalyser.py options: [-h] [--errors] [--authors] [--articles]

*YOU NEED TO USE ONE OF THE OPTIONAL ARGUMENTS*

optional arguments:
  -h, --help  show this help message and exit
  --errors    show which day error rate is greater than 1 percent
  --authors   show which show top five authors
  --articles  show which show top three articles

For example: 

pyhton loganalyser.py --authors

Will produce:

Author - View count
Rudolf von Treppenwitz - 338647 views
Ursula La Multa - 253801 views
Anonymous Contributor - 170098 views
Ursula La Multa - 84906 views
Rudolf von Treppenwitz - 84810 views
