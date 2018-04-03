# Udacity nano degree log analyzer project

This is a command line tool written in Python which analyzes a news database to show some of the statistics of a webpage

### Prerequisites

Setup Vagrant and Virtualbox

- Download and install Virtualbox:
https://www.virtualbox.org/wiki/Download_Old_Builds_5_1

- Download and install Vagrant:
https://www.vagrantup.com/downloads.html

- Download and extract VM configuration
https://d17h27t6h515a5.cloudfront.net/topher/2017/August/59822701_fsnd-virtual-machine/fsnd-virtual-machine.zip 

'cd' to /vagrant directory and run command 'vagrant up' to install the VM.
Then run 'vagrant ssh' to login to the virtual machine.

- Download the database file and extract it to /vagrant directory:
https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip 

Load the data to database using 'psql -d news -f newsdata.sql' command

- In VM connect to database (if not already connected to)
use 'psql -d news' command in your VM

- When connected to database create views which are needed for error rate calculation. 
Copy paste this:
create view errs as select time::timestamp::date as date, count(*) from log where status like '404%' group by date;
create view total as select time::timestamp::date as date, count(*) from log group by date;

- Download and put the loganalyser.py in the same directory as the newsdata.sql

### Running the code

Run the script file from command line: 

pyhton loganalyser.py options: [-h] [--errors] [--authors] [--articles]

*YOU NEED TO USE ONE OF THE OPTIONAL ARGUMENTS*

optional arguments:
  -h, --help  show this help message and exit
  --errors    show which day error rate is greater than 1 percent
  --authors   show which show top five authors
  --articles  show which show top three articles

For example: 

python loganalyser.py --articles

Will produce:

Article - View count
Candidate is jerk, alleges rival - 338647 views
Bears love berries, alleges bear - 253801 views
Bad things gone, say good people - 170098 views
