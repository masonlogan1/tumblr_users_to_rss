import csv
import re

DEFAULT_PATTERN = 'https://www.tumblr.com/[A-Za-z--]*'
NONUSER_TYPES = ('reblog', 'live', 'blog', 'dashboard', 'explore', 'inbox',
                     'new', 'reblog', 'settings', 'about', 'policy')


def users_from_file(datafile, url_pattern: str = DEFAULT_PATTERN,
                  ignored_users: str = NONUSER_TYPES):
    """Opens the file, finds all potential user urls, filters out ones we
    know are not actually users, and returns all of them as a list"""
    # generates all tumblr urls in the file
    gen_urls = (re.findall(url_pattern, line.decode()) for line in datafile.readlines())
    # unpacks gen_urls into a list of strings; turns into set for uniqueness
    urls = set(sum([url for url in gen_urls if url is not None], []))
    # separates the username and filters out things we know are not usernames
    return (user for user in (url.split('/')[-1] for url in urls)
            if user not in ignored_users
            and user != '')


def get_rss_urls(users):
    return (f"""https://{user}.tumblr.com/rss""" for user in sorted(users))


def parse_rss_urls_from_document(datafile):
    return get_rss_urls(users_from_file(datafile=datafile))


def create_csv_from_urls(urls, writer):
    csv_writer = csv.writer(writer)
    for url in urls:
        csv_writer.writerow([url])


def create_csv_from_file(file_in, destination):
    """Takes a file, strips the tumblr blog urls, produces a csv with the
    blog urls as rows to the destination"""
    create_csv_from_urls(parse_rss_urls_from_document(file_in), destination)
