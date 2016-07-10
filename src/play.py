#!/usr/bin/env python

from pprint import pprint
import random

def show(obj):
    '''Show the dump of the properties of the object.'''
    pprint(vars(obj))

from tlsarchiverfront import *
from tlsarchiverfront.services import *

print(stats.get_stats())
