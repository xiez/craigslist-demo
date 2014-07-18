#!/bin/env python

import re
import urllib2

from bs4 import BeautifulSoup

# job_kw = 'software'
sale_kw = 'software'
location = 'chicago'

sale_search_url_fmt = 'http://%s.craigslist.org/search/sss?query=%s&sort=rel'
job_search_url_fmt = 'http://%s.craigslist.org/search/jjj?query=%s&sort=rel'

reply_link_base_fmt = 'http://%s.craigslist.org/reply'

def build_reply_link(res_link):
    """

    Arguments:
    - `res_link`:

    Returns:
        A reply link to query contact info.
    """
    reply_link_base = reply_link_base_fmt % location
    return reply_link_base + res_link.split('.')[0]

def get_email_from_reply_link(reply_link):
    """Extract email from reply page.

    Arguments:
    - `res_link`:

    Returns:
        email or None.
    """
    req = urllib2.Request(reply_link)
    res = urllib2.urlopen(req)
    the_page = res.read()
    emails = re.findall(r'[\w\.-]+@[\w\.-]+', the_page)
    if len(set(emails)) > 0:
        return set(emails).pop()  # ignore rest emails
    else:
        return None

def main():
    """Main logic of the program.
    """
    sale_search_url = sale_search_url_fmt % (location, sale_kw)
    req = urllib2.Request(sale_search_url)
    res = urllib2.urlopen(req)
    the_page = res.read()
    parsed_html = BeautifulSoup(the_page)
    for span in parsed_html.findAll('span', attrs={'class': 'pl'}):
        res_link = span.find('a')['href']
        reply_link = build_reply_link(res_link)
        email = get_email_from_reply_link(reply_link)
        print email

if __name__ == "__main__":
    main()
