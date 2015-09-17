""" file:   __init__.py (xjson.metadata)
    author: Jess Robertson
            CSIRO Minerals Resources Flagship
    date:   Wednesday 27 August, 2014

    description: Functions to deal with metadata
"""

from .registry import MetadataRegistry
from .metadata import Metadata, yamlify, xml_to_metadata
from .namespaces import NamespaceMap
from .vocabulary import unmarshal, unmarshal_all
from .decorator import with_metadata, XJSON_NAMESPACE
from ._version import __version__

__all__ = ['MetadataRegistry', 'Metadata', 'NamespaceMap',
           'unmarshal', 'unmarshal_all', 'yamlify', 'XJSON_NAMESPACE',
           'with_metadata', 'xml_to_metadata', '__version__']