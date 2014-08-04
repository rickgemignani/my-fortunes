#coding=utf-8

short_name =       "get_fortune"
package_name =     "get_fortune"
name =             "get_fortune"
version =          "1.0"
description =      "command line script"
long_description = ""
author =           "Ricardo Saar Gemignani"
author_email =     "ricardo@sthima.com.br"
maintainer =       ""
maintainer_email=  ""
copyright =        "Ricardo Saar Gemignani 2008"
url =              "http://www.sthima.com.br/"
download_url =     "http://www.sthima.com.br/"
license =          "GPL"
#dev_status =       "Development Status :: 1 - Planning"
#dev_status =       "Development Status :: 2 - Pre-Alpha"
dev_status =       "Development Status :: 3 - Alpha"
#dev_status =       "Development Status :: 4 - Beta"
#dev_status =       "Development Status :: 5 - Production/Stable"
#dev_status =       "Development Status :: 6 - Mature"
#dev_status =       "Development Status :: 7 - Inactive"

zip_safe = False
keywords = []

install_requires = [
        "FormEncode>= 1.2",
]

classifiers = [
    dev_status,
    'Operating System :: OS Independent',
    'Programming Language :: Python',
]

test_suite='nose.collector'

entry_points = """
[console_scripts]
%(short_name)s = %(package_name)s.command:main
"""%vars()

data_dirs=[]

data_files = []
