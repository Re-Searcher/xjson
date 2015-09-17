""" file: decorator.py (pysiss.xjson)
    author: Jess Robertson
            CSIRO Earth Science and Resource Engineering
    email:  jesse.robertson@csiro.au
    date:   Wednesday May 1, 2013

    description: Some basic metaclasses etc for defining pysiss classes
"""

from __future__ import print_function, division

from .xjson import XJson, XJSON_NAMESPACE

from uuid import uuid5 as uuid
from uuid import NAMESPACE_DNS
import types


def with_xjson(tag, subelements=None):
    """ A decorator to store xjson about an object

        This decorator generates a UUID for a class at initialization,
        and defines the class __eq__ method to use this UUID.

        This decorator generates a.xjson record for a class at
        initialization, and defines a set of methods for serializing and
        deserializing that.xjson

        The optional subelements parameter allows classes to define an initial
        structure for their.xjson tree. Subelements should be a dictionary 
        defining keyword arguments which can be passed to `XJson.add_subelement` 

        Parameters:
            tag - the tag for the.xjson tree
            subelements - a list of dictionaries, defining subelements of the
               .xjson instance.
    """
    def _md_wrapper(cls):
        """ Wrapper to add.xjson
        """
        # Generate a new identity if required, & construct.xjson attributes
        cls.uuid = uuid(NAMESPACE_DNS, tag)
        if not hasattr(cls, 'ident') or cls.ident is None:
            cls.ident = str(cls.uuid)
        cls.xjson = XJson(tag=XJSON_NAMESPACE + tag,
                                ident=cls.ident)

        # Add subelements if required
        if subelements:
            for subelement in subelements:
                cls.xjson.add_subelement(**subelement)

        # Add equality test to match instances if their uuids match
        setattr(cls, '__eq__', lambda self, other: self.uuid == other.uuid)
        cls.__eq__.__doc__ = \
            """ Equality test

                Class instances are equal if their UUIDs match
            """

        return cls  
    return _md_wrapper
