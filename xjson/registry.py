""" file:   registry.py (pysiss.xjson)
    author: Jess Robertson
            CSIRO Minerals Resources Flagship
    date:   Wednesday 27 August, 2014

    description: Functions to deal with.xjson objects

    XJson descriptions can be shared by many different objects, so it makes
    sense to seperate these out into a seperate registry.
"""

from __future__ import print_function, division

from .singleton import singleton

import logging

LOGGER = logging.getLogger('pysiss')


class XJsonRegistry(dict, metaclass=singleton):

    """ A registry to store.xjson instances

        Since GeoSciML allows.xjson reuse, we need to have a central
        repository of.xjson which stores the actual etrees, and objects can
        refer to keys within this repository.
    """

    registered_ids = set()

    def register(self, xjson, replace_existing=False, verbose=False):
        """ Register a.xjson item in the registry
        """
        # Check to see whether the item already exists
        if not replace_existing:
            if xjson.ident in self.registered_ids and verbose:
                LOGGER.warn(('XJson ID {0} already exists, skipping'
                             ' registration').format(xjson.ident))
            return

        # If it doesn't already exist
        self[xjson.ident] = xjson

    def deregister(self, ident):
        """ Deregister the given xjson item given by the key
        """
        del self[ident]
