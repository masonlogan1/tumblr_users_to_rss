import csv
import re

DEFAULT_PATTERN = 'https://www.tumblr.com/[A-Za-z--]*'
IGNORED_URL_TYPES = ('reblog', 'live', 'blog', 'dashboard', 'explore', 'inbox',
                     'new', 'reblog', 'settings', '')


def get_from_file(filename: str, url_pattern: str = DEFAULT_PATTERN,
                  ignored_urls: str = IGNORED_URL_TYPES) -> list:
    """Opens the file, finds all tumblr urls, filters out ones we don't want,
    and returns all of them as a list"""
    with open(filename, 'r') as reader:
        # generates all found strings in the file
        gen_urls = (re.findall(url_pattern, line) for line in
                    reader.readlines())
        # unpacks gen_urls into a list of strings; turns into set for uniqueness
        urls = set(sum([url for url in gen_urls
                        if url is not None
                        and url != ''
                        and url not in ignored_urls],
                       []))
    return list(urls)


def get_rss_urls(urls) -> list:
    return [f"""https://{url.split('/')[-1]}.tumblr.com/rss""" for url in urls]


def parse_rss_urls_from_document(filename):
    return get_rss_urls(get_from_file(filename=filename))


def create_csv_from_urls(urls, destination):
    with open(destination, 'w+') as writer:
        csv_writer = csv.writer(writer)
        for url in urls:
            csv_writer.writerow([url])


def create_csv_from_file(file_in, destination):
    """Takes a file, strips the tumblr blog urls, produces a csv with the
    blog urls as rows to the destination"""
    create_csv_from_urls(parse_rss_urls_from_document(file_in), destination)
