""" file:  xjson.py (pysiss xjson)
    author: Jess Robertson
            CSIRO Minerals Resources Flagship
    date:   Wednesday 27 August, 2014

    description: Functions to deal with gsml:geologicFeature data

    Geologic features can be shared by many different objects, so it makes
    sense to seperate these out into a seperate registry.
"""

from __future__ import print_function, division

from .registry import XJsonRegistry
from .xjson_namespace import XJSON_NAMESPACE
from .json_target import JSONLDTarget
from .json_context import JSONLDContext

import json
from lxml.etree import XML, XMLParser
import io
import uuid


def qname_str(qname):
    """ Represent a QName in a namespace:localname string
    """
    if qname.namespace not in (None, 'None', 'none'):
        result = '{0}:{1}'.format(qname.namespace, qname.localname)
    else:
        result = '{0}'.format(qname.localname)
    return result

def get_children(self):
    """ Return the children nodes from the xjson tree

        Returns:
            an iterator over the children, or None if there are no
            children
    """
    child_keys = [k for k in self.keys()
                  if not any(k.startswith(c) for c in ('@', '#'))]
    if child_keys:
        return ((k, self[k]) for k in child_keys)
    else:
        return None

def yamlify(xjson, indent_width=2):
    """ Convert a xjson tree to 'yaml' format

        Parameterts:
            xjson - a XJson instance
            intent_width - width of a single indent step in characters
    """
    def _emit_yaml(key, body, indent):
        """ Function to emit YAML for one element at a time
        """
        # Sort out indentation
        spaces = ' ' * indent_width * indent
        new_item = '\n' + spaces + ' ' * indent_width

        # Build line for current element
        result = '\n' + spaces + key + ':'
        if isinstance(body, dict):
            # Add data and attributes
            if '#data' in body.keys():
                result += ' {0}'.format(body['#data'])
                result += '\n'
            if '#attributes' in body.keys():
                for item in body['#attributes'].items():
                    result += new_item + '@{0}: {1}'.format(*item)

            # Add lines for children recursively
            children = get_children(body)
            if children:
                for tag, child in children:
                    result += _emit_yaml(tag, child, indent + 1)

        elif isinstance(body, str):
            result += ' ' + body

        elif body is None:
            result += ' None'

        else:
            result += ' [' + new_item \
                + new_item.join(str(b) for b in body) \
                + new_item + ']'

        # Return result
        return result

    return '\n'.join([_emit_yaml(*it, indent=0) for it in xjson.body.items()])


class XJson(object):

    """ Class to store xjson record

        Can be initialized with an dict instance, or using the 'from_xml'
        class method.

        Queries (XPath, or ElementPath) are passed through to the underlying
        element, with a few nicities to deal with XML namespaces.

        Parameters:
            body - a dict containing the JSON-LD body
            context - a XJsonContext containing the JSON-LD context
    """

    registry = XJsonRegistry()

    def __init__(self, body, ident=None, context=None):
        super(XJson, self).__init__()
        self.ident = self.uuid = \
            uuid.uuid5(uuid.NAMESPACE_DNS,
                       XJSON_NAMESPACE + 'xjson')
        if isinstance(body, str):
            json.loads(body)
        else:
            self.body = body
        if context is not None:
            if isinstance(context, str):
                self.context = JSONLDContext(mapping=json.loads(context))
            else:
                self.context = context
        else:
            self.context = JSONLDContext()

    def __str__(self):
        """ String representation
        """
        template = '{{\n{0},\n{1}\n}}'
        cstr = '\n'.join('    ' + l for l in str(self.context).splitlines())
        bstr = json.dumps(self.body, indent=4)
        bstr = '\n'.join(bstr.splitlines()[1:-1])
        return template.format(cstr, bstr)

    def __repr__(self):
        """ String representation
        """
        template = 'XJson(ident={0}, body={1}, context={2}'
        return template.format(self.ident, self.body, self.context)

    def __getitem__(self, query):
        """ Getitem executes a jsonpath query
        """
        pass
        # return self.query(query)

    @classmethod
    def from_xml(cls, xml, namespace_handling=None):
        """ Read some XML containing a xjson record

            Parameters:
                xml - either a handle to an open xml file, or a string of XML
                namespace_handling - how to handle XML namespaces. Optional,
                defaults to 'shorten'.

            Returns:
                the new XJson instance containing the record
        """
        if namespace_handling is None:
            namespace_handling = 'shorten'

        # Initialize tree and XML namespaces
        if not isinstance(xml, io.IOBase):
            try:
                xml = io.BytesIO(xml.encode('utf-8'))
            except AttributeError:
                # We already have a bytestring so don't bother encoding it
                xml = io.BytesIO(xml)

        # Parse xjson using JSON mapping
        parser = XMLParser(
            target=JSONLDTarget(namespace_handling=namespace_handling))
        body, context = XML(xml.read(), parser)
        return cls(body=body, context=context)

    def register(self):
        """ Register this xjson instance with the XJson registry
        """
        # Register yourself with the registry if required
        self.registry.register(self)

    def yaml(self, indent_width=2):
        """ Return a YAML-like representation of the tags

            Parameters:
                indent_width - the number of spaces in each indent level.
                    Optional, defaults to 2.

            Returns:
                a string reprentation of the xjson tree
        """
        return yamlify(self, indent_width=indent_width)
