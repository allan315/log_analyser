import psycopg2
import argparse
import sys

# This script will query database for some statistics (described below)
# and prints the results to standard output. It should be used from command line.
# Currently script has 3 queries which can be accessed through arguments e.g.
# python loganalyser.py --authors


# Top articles query (needs to have "view_count" view). It connects articles and logs
# using modified path in log table which is connected to slug to get view count.

top_articles = """select articles.title, view_count.count from
articles inner join view_count on articles.slug = view_count.slug
order by view_count.count desc limit 3;"""

# Top authors query (needs to have "view_count" view). This query can be divided to
# two steps 1. we connect view_count with articles, 2. we connect this result
# with authors table to get author name and view count


top_authors = """select authors.name, t.count from
(select articles.author, articles.slug, view_count.count from articles
inner join view_count on articles.slug = view_count.slug)
as t inner join authors on authors.id = t.author
order by t.count desc limit 5;"""

# Log errors query (needs to have "ok" and "errors" view). This query uses two views and
# calculates error rate (percentage). Error rate higher than 1 will be shown.

top_errors = """select to_char(date, 'Month DD, YYYY') as formated_date,
to_char(err, '9.9%') as error_rate
from (select ok.date, (errors.count * 100.0 / ok.count) as err
from ok inner join errors on ok.date = errors.date)
as t where err > 1 order by err desc limit 5;
"""


# I'm using argparse to define and take arguments from command line

parser = argparse.ArgumentParser(add_help=True,
                                 description='***YOU NEED TO USE ONE OF THE OPTIONAL ARGUMENTS***',  # NOQA
                                 usage='%(prog)s options: [-h] [--errors] [--authors] [--articles]')  # NOQA

# add_mutually_exclusive_group() will define that only one argument is taken

group = parser.add_mutually_exclusive_group()

group.add_argument('--errors', help='show which day error rate is greater than 1 percent',  # NOQA
                   action='store_true')
group.add_argument('--authors', help='show which show top five authors',
                   action='store_true')
group.add_argument('--articles', help='show which show top three articles',
                   action='store_true')
args = parser.parse_args()

# Connect to DB, execute queries and return data

def get_from_db(query):
    db = psycopg2.connect(dbname="news")
    c = db.cursor()
    c.execute(query)
    data = c.fetchall()
    db.close()
    return data

if __name__ == '__main__':

    # Check for no arguments and print error if any
    
    if not (args.errors or args.authors or args.articles):
        parser.error('***YOU NEED TO USE ONE OF THE OPTIONAL ARGUMENTS***')

    # Check what argument was given with "if" statements and execute the appropriate SQL query

    if args.errors:
        data = get_from_db(top_errors)
        sys.stdout.write("Date - Time\n")
        for date, err in data:
            sys.stdout.write("{} - {}\n".format(date, err))

    if args.authors:
        data = get_from_db(top_authors)
        sys.stdout.write("Author - View count\n")
        for author, views in data:
            sys.stdout.write("{} - {} views\n".format(author, views))

    if args.articles:
        data = get_from_db(top_articles)
        sys.stdout.write("Article - View count\n")
        for article, views in data:
            sys.stdout.write("{} - {} views\n".format(article, views))
