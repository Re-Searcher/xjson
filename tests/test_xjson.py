""" file:   test.xjson.py
    author: Jess Robertson
            CSIRO Earth Science and Resource Engineering
    date:   Tuesday 2 May, 2015

    description: Tests for.xjson class
"""

from __future__ import print_function, division

from xjson import XJson

import unittest
import requests
import json


class TestXJson(unittest.TestCase):

    "Tests for XJson class"

    def setUp(self):
        # Make a request to the wfs
        ept = ('http://www.ga.gov.au/thredds/wcs/national_grids/'
               'radmap10_unfiltered_pctk.nc')
        payload = {
            'service': 'wcs',
            'request': 'getcapabilities'
        }
        self.response = requests.get(ept, payload)
        self.response.raise_for_status()
        self.xjson = XJson.from_xml(self.response.content)

    def test_str_method(self):
        """ Check that string methods work ok
        """
        str(self.xjson)
        str(self.xjson.body)
        str(self.xjson.context)

    def test_repr_method(self):
        """ Check that string methods work ok
        """
        repr(self.xjson)
        repr(self.xjson.body)
        repr(self.xjson.context)

    def test_str_roundtrip(self):
        """ Check that we can roundtrip xjson ojects
        """
        reloaded = json.loads(str(self.xjson))
        self.assertEqual(
            set(reloaded.keys()),
            set(list(self.xjson.body.keys()) + ['@context']))

    def test_theres_something_to_use(self):
        """ Check that we've got a response to play with
        """
        self.assertIsNotNone(self.response.content)

    def test_xjson_length(self):
        """ Check that the.xjson conversion results in the right number of
            items.
        """
        bh_elems = self.xjson['.//nvcl:scannedBorehole']
        self.assertTrue(len(list(self.xjson.yaml())) > 10)
        self.assertTrue(len(bh_elems) > 0)

    def test_xjson_queries(self):
        """ Check that queries can run multiple times and get the same results
        """
        elems = self.xjson['.//nvcl:scannedBorehole']
        self.assertTrue(len(elems) > 0)
        elems2 = self.xjson['.//nvcl:scannedBorehole']
        self.assertEqual(len(elems2), len(elems)) 
