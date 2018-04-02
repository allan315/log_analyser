import psycopg2
import argparse
import sys

""" 1. most popular article
create view view_count as
select replace(path, '/article/', '') as slug, count(*)
from log group by slug;"""

top_articles = """select articles.title, view_count.count from
articles inner join view_count on articles.slug = view_count.slug
order by view_count.count desc limit 3;"""

""" 2. most popular author
create view view_count as
select replace(path, '/article/', '') as slug, count(*)
from log group by slug;"""

top_authors = """select authors.name, t.count from
(select articles.author, articles.slug, view_count.count from articles
inner join view_count on articles.slug = view_count.slug)
as t inner join authors on authors.id = t.author
order by t.count desc limit 5;"""

""" 3. log errors
create view ok as select time::timestamp::date as date, status, count(*)
from log where status like '200%' group by date, status;

create view errors as select time::timestamp::date as date, status, count(*)
from log where status like '404%' group by date, status;"""

top_errors = """select to_char(date, 'Month DD, YYYY') as formated_date,
to_char(err, '9.9%') as error_rate
from (select ok.date, (errors.count * 100.0 / ok.count) as err
from ok inner join errors on ok.date = errors.date)
as t where err > 1 order by err desc limit 5;
"""

parser = argparse.ArgumentParser(add_help=True,
                                 description='***YOU NEED TO USE ONE OF THE OPTIONAL ARGUMENTS***',  # NOQA
                                 usage='%(prog)s options: [-h] [--errors] [--authors] [--articles]')  # NOQA

group = parser.add_mutually_exclusive_group()

group.add_argument('--errors', help='show which day error rate is greater than 1 percent',  # NOQA
                   action='store_true')
group.add_argument('--authors', help='show which show top five authors',
                   action='store_true')
group.add_argument('--articles', help='show which show top three articles',
                   action='store_true')
args = parser.parse_args()


def get_from_db(query):
    db = psycopg2.connect(dbname="news")
    c = db.cursor()
    c.execute(query)
    data = c.fetchall()
    db.close()
    return data

if __name__ == '__main__':
    if not (args.errors or args.authors or args.articles):
        parser.error('***YOU NEED TO USE ONE OF THE OPTIONAL ARGUMENTS***')
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
