#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import datetime

import praw
import markdown2
from docopt import docopt
from jinja2 import Environment, PackageLoader

USAGE = """r2k.py

Compiles requested number of top posts from specified subreddit
into a Kindle-formatted MOBI book.

Usage:
    r2k.py <subreddit> [--posts=<n>] [--period=<t>]

Options:
    --posts=<n>         The number of posts to include in the generated book.
                        [default: 5]
    --period=<t>        Pick the top posts from "hour", "day", "week", "month"
                        or "year".
                        [default: all]
"""


def from_cli():
    args = docopt(USAGE)

    max_posts = int(args['--posts'])
    period = args['--period']
    subreddit = args['<subreddit>']

    r = praw.Reddit('reddit-selftext-to-kindle converter')
    sub = r.get_subreddit(subreddit)

    posts = {
        'all': sub.get_top_from_all,
        'year': sub.get_top_from_year,
        'month': sub.get_top_from_month,
        'week': sub.get_top_from_week,
        'day': sub.get_top_from_day,
        'hour': sub.get_top_from_hour
    }[period](limit=max_posts)

    env = Environment(loader=PackageLoader('r2klib', 'templates'))
    thread_template = env.get_template('thread.jinja')

    with open('{0}.html'.format(subreddit), 'wb') as fout:
        fout.write(thread_template.render(
            now=datetime.datetime.today(),
            post_count=max_posts,
            period=period,
            subreddit=subreddit,
            title=subreddit,
            posts=posts,
            markdown=markdown2.markdown
        ).encode('utf-8'))


if __name__ == '__main__':
    sys.exit(from_cli())