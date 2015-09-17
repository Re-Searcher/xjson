""" file: xjson_namespace.py (xjson.metadata)
    author: Jess Robertson
            CSIRO Mineral Resources Flagship
    date: Monday May 2, 2015

    description: Defines a namespace for xjson metadata
"""

from ._version import __version__

# Namespace for xjson objects in XML
XJSON_NAMESPACE = \
	'{{http://geoanalytics.csiro.au/xjson/{0}}}'.format(__version__)
