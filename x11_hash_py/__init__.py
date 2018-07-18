# -*- coding: utf-8 -*-

from __future__ import absolute_import

from . import op
from .blake import blake
from .bmw import bmw
from .groestl import groestl
from .skein import skein
from .jh import jh
from .keccak import Keccak512
from .luffa import luffa5
from .cubehash import cubehash
from .shavite import shavite
from .simd import simd
from .echo import echo

def getPoWHash(x):
    assert type(x) == bytes
    res = blake(x)
    res = bmw(res)
    res = groestl(res)
    res = skein(res)
    res = jh(res)
    res = Keccak512(res).digest()
    res = luffa5(res)
    res = cubehash(res)
    res = shavite(res)
    res = simd(res)
    res = echo(res)
    return res[:32]
