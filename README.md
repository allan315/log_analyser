# Udacity nano degree log analyzer project

This is a command line tool written in Python which analyzes a news database to show some of the statistics of a webpage

### Prerequisites

Setup Vagrant and Virtualbox

<ul><li>Download and install Virtualbox:<br>
https://www.virtualbox.org/wiki/Download_Old_Builds_5_1</li>

<li>Download and install Vagrant:<br>
https://www.vagrantup.com/downloads.html</li>

<li>Download and extract VM configuration:<br>
https://d17h27t6h515a5.cloudfront.net/topher/2017/August/59822701_fsnd-virtual-machine/fsnd-virtual-machine.zip 

'cd' to /vagrant directory and run command 'vagrant up' to install the VM.
Then run 'vagrant ssh' to login to the virtual machine.</li>

<li>Download the database file and extract it to /vagrant directory:<br>
https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip </li></ul>

Load the data to database using 'psql -d news -f newsdata.sql' command

<ul>In VM connect to database (if not already connected to):<br>
use 'psql -d news' command in your VM</ul>

When connected to database create views which are needed for error rate calculation:<br> 
<ul>Copy paste this:<br>
<li>create view errs as select time::timestamp::date as date, count(*) from log where status like '404%' group by date;</li>
<li>create view total as select time::timestamp::date as date, count(*) from log group by date;</li></ul>

Download and put the loganalyser.py in the same directory as the newsdata.sql<br>

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

Will produce:<br>
<br>
Article - View count<br>
Candidate is jerk, alleges rival - 338647 views<br>
Bears love berries, alleges bear - 253801 views<br>
Bad things gone, say good people - 170098 views<br>
