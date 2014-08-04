#!/usr/bin/env python
#encoding=utf-8

'''
    About
    
    get_fortune - command line script to get quotes from quotegeek.com and 
        format as a fortune file.
        
    written by Ricardo Saar Gemignani
    special thanks to Google.com

    copyright 2008

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; version 2 of the License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    Usage
    
    $ get_fortune --help 
    
'''

__author__=u'Ricardo Saar Gemignani <ricardo@sthima.com.br>'
__version__=u'1.0'
__usage__ = "usage: %prog [options] quotegeek_url [quotegeek_url]"

from optparse import OptionParser
import formencode.validators as validators
import sys
import urllib
import re
from lxml import etree

import logging
log = logging.getLogger("get_fortune")

def startup_logging():
#    logging_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging_format = '%(levelname)s - %(message)s'
    logging_datefmt='%a, %d %b %Y %H:%M:%S'
    filename='/temp/myapp.log'
    logging_level = 50
    logging.basicConfig(level=logging_level, format=logging_format, datefmt=logging_datefmt)
    log.info('Logging level set to: %s'%logging.getLevelName(logging_level))
    
def update_verbosity(verbosity):
    lvl = 50-((verbosity<4 and verbosity or 4)*10)
    logging.root.setLevel(lvl)
    log.info('Logging level set to: %s'%logging.getLevelName(lvl))

def parse_options():
    usage = __usage__
    parser = OptionParser(usage)
    parser.set_defaults(verbosity=1, show_about=False)
    parser.add_option("-v", action="count", dest="verbosity", help="Verbosity counter.")
    parser.add_option("-a", dest="append", help="Text to be appended to every quote.")
    parser.add_option("", "--about", action="store_true", dest="show_about", help="Shows about page.")
    (options, args) = parser.parse_args()

    return options, args, parser

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
    f = urllib.urlopen(url)
    try:
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

    try:
        
        startup_logging()
        
        options, args, parser = parse_options()
        
        update_verbosity(options.verbosity)

        if options.show_about is True:
            print __doc__
            return

        if len(args) != 1:
            print parser.format_help()
            log.fatal("I need at least one quotegeek url!")
        
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

    except (KeyboardInterrupt, SystemExit):
        print >>sys.stderr, "Processo interrompido pelo usuário!"
        exit(None)
        
if __name__ == "__main__":
    main()
    

