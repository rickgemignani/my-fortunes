#!/usr/bin/env python
#encoding=utf-8

'''

'''

__author__=u'Ricardo Saar Gemignani <ricardo@sthima.com.br>'
__version__=u'1.0'

from optparse import OptionParser
import formencode.validators as validators
import sys
import urllib
import re
from lxml import etree

import logging
log = logging.getLogger("getQG")

def startup_logging(options):
    logging_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging_datefmt='%a, %d %b %Y %H:%M:%S'
    filename='/temp/myapp.log'
    logging_level = 50-((options.verbosity<4 and options.verbosity or 4)*10)
    logging.basicConfig(level=logging_level, format=logging_format, datefmt=logging_datefmt)
    log.info('Logging level set to: %s'%logging.getLevelName(logging_level))

def parse_options():
    usage = "usage: %prog [options] quotegeek_url"
    parser = OptionParser(usage)
    parser.set_defaults(verbosity=1)
    parser.add_option("-v", "--verbose", action="count", dest="verbosity")
#    parser.add_option("-l", "--logfile", dest="logging_file")
    parser.add_option("-a", "--appendtoquote", dest="append")
    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("I need a quotegeek url!")

    return options, args

def validate_url(url):
    u = validators.URL(add_http=True, check_exists=True)
    return u.to_python(url)
    
def get_quotes(root):
    quotes_and_categories = [(i, i.get('class')) for i in root.iterdescendants(tag='span') if i.get('class') == 'quotestandard' or i.get('class') == 'categorycrumb' ]
    quotes = []
    for qc in quotes_and_categories:
        if qc[1] == 'quotestandard':
            quotes.append(qc[0].text)
        elif qc[1] == 'categorycrumb':
            if len(quotes) == 0: continue;
            q = quotes.pop()
            html=etree.tostring(qc[0])
            cat = re.sub(r'<[^>]*?>', '', html)
            cat = cat.replace('&gt;','>')
            cat = cat.replace('\n','')
            quotes.append(q+"\n"+" -- "+cat)
        
    return quotes

def parse(url):
    try:
        f = urllib.urlopen(url)
        html = f.read()
        
        root = etree.HTML(html)
        
        return get_quotes(root)
    finally:
        f.close()
    
def parse_all_pages(url):
    count = 0
    quote_list = []
    tmp_quote_list = parse(url)
    while len(tmp_quote_list)>0 and count < 10:
        quote_list.extend(tmp_quote_list)
        log.debug('Parsing Page %s'%(count+1))
        count += 1
        tmp_quote_list = parse('%s&pageid=%s'%(url,count))
    return quote_list
    
def main():
    (options, args) = parse_options()
    startup_logging(options)
    for url in args:
        try:
            url = validate_url(url)
        except validators.Invalid, err:
            log.error('Invalid URL (%s) - %s'%(url, err))
            continue
    
        log.debug('Parsing URL: %s'%url)
        quotes = parse_all_pages(url)
        if len(quotes) > 0:
            print '%'
        else:
            log.info('Looks like there are no quotes in this url (%s).'%url)
        for quote in quotes:
            if quote is None: continue;
            print quote.encode("utf-8")
            if options.append is not None:
                print ' -- %s'%options.append
            print '%'

if __name__ == "__main__":
    main()
    

