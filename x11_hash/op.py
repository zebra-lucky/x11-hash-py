# -*- coding: utf-8 -*-

from builtins import int
from struct import unpack, pack


M32 = 2**32 - 1     # Mask 32-bit
S32 = 2**31         # Sign Mask 32-bit
R32 = 2**32         # Mask for logical right shift 32-bit
M64 = 2**64 - 1     # Mask 64-bit
S64 = 2**63         # Sign Mask 64-bit
R64 = 2**64         # Mask for logical right shift 64-bit


def to32s(u): return -((~u & M32) + 1) if u & S32 else u & M32
def to32u(s): return s & M32
def to64s(u): return -((~u & M64) + 1) if u & S64 else u & M64
def to64u(s): return s & M64
def rshift32b(val, n): return (val % R32) >> n  # logical right shift 32-bit
def rshift64b(val, n): return (val % R64) >> n  # logical right shift 64-bit
def rotl32(x, c): return ((x << c) | rshift32b(x, 32 - c)) & M32


def buffer_insert(buf, offset, data, data_len=None):
    if data_len is None:
        data_len = len(data)
    for i in range(data_len):
        buf[i+offset] = data[i]


def buffer_insert_2d(buf, offset, offset2, data, data_len, data_len2):
    for i in range(data_len):
        for j in range(data_len2):
            buf[i+offset][j+offset2] = data[i][j]


def buffer_xor_insert(buf, offset, data, doffset, data_len=None):
    if data_len is None:
        data_len = len(data)
    for i in range(data_len):
        buf[i+offset] ^= data[i+doffset]


def buffer_insert_u64(buf, offset, data, data_len=None):
    if data_len is None:
        data_len = len(data)
    for i in range(data_len):
        buf[i+offset] = data[i].clone()


def bytes_to_i32_list(buf):
    i32l = []
    buf_len = len(buf)
    for i in range(buf_len//4):
        i32v = unpack('>I', buf[i*4:i*4+4])[0]
        i32l.append(i32v)
    return i32l


def bytes_from_i32_list(l):
    res = b''
    for i32v in l:
        res += pack('>I', i32v)
    return res


def bytes_to_u64_list(buf, buf_len):
    buf64 = []
    for i in range(buf_len//8):
        hi = unpack('>I', buf[i*8:i*8+4])[0]
        lo = unpack('>I', buf[i*8+4:i*8+8])[0]
        u64v = u64(hi, lo)
        buf64.append(u64v)
    return buf64


def bytes_to_u64_list_le(buf, buf_len):
    buf64 = []
    for i in range(buf_len//8):
        lo = unpack('<I', buf[i*8:i*8+4])[0]
        hi = unpack('<I', buf[i*8+4:i*8+8])[0]
        u64v = u64(hi, lo)
        buf64.append(u64v)
    return buf64


def swap32(val):
    return (
        ((val & 0xFF) << 24) |
        ((val & 0xFF00) << 8) |
        (rshift32b(val, 8) & 0xFF00) |
        (rshift32b(val, 24) & 0xFF))


def swap32_list(l): return list(map(swap32, l))
def t32(x): return x & M32


def xor_table(d, s1, s2, tlen):
    for i in range(tlen):
        d[i] = s1[i] ^ s2[i]


class u64(object):

    def __init__(self, hi, lo):
        self.hi = hi & M32
        self.lo = lo & M32

    def __repr__(self):
        #return 'u64(%d)' % self.x
        return 'u64 { hi: %s, lo: %s }' % (self.hi, self.lo)

    def set(self, x):
        self.hi = x.hi
        self.lo = x.lo

    def add(self, x):
        lowest = (self.lo & 0XFFFF) + (x.lo & 0XFFFF)
        lowMid = rshift32b(self.lo, 16) + rshift32b(x.lo, 16) + rshift32b(lowest, 16)
        highMid = (self.hi & 0XFFFF) + (x.hi & 0XFFFF) + rshift32b(lowMid, 16)
        highest = rshift32b(self.hi, 16) + rshift32b(x.hi, 16) + rshift32b(highMid, 16)
        self.lo = (lowMid << 16) | (lowest & 0XFFFF)
        self.hi = (highest << 16) | (highMid & 0XFFFF)
        self.hi &= M32
        self.lo &= M32
        return self

    def add_one(self):  # set self
        if self.lo == -1 or self.lo == 0xFFFFFFFF:
            self.lo = 0
            self.hi += 1
        else:
            self.lo += 1
        self.hi &= M32
        self.lo &= M32

    def plus(self, x):
        c = u64(0, 0)
        lowest = (self.lo & 0XFFFF) + (x.lo & 0XFFFF)
        lowMid = rshift32b(self.lo, 16) + rshift32b(x.lo, 16) + rshift32b(lowest, 16)
        highMid = (self.hi & 0XFFFF) + (x.hi & 0XFFFF) + rshift32b(lowMid, 16)
        highest = rshift32b(self.hi, 16) + rshift32b(x.hi, 16) + rshift32b(highMid, 16)
        c.lo = (lowMid << 16) | (lowest & 0XFFFF)
        c.hi = (highest << 16) | (highMid & 0XFFFF)
        c.hi &= M32
        c.lo &= M32
        return c

    def bit_not(self):
        return u64(~self.hi, ~self.lo)

    def one(self):
        return u64(0x0, 0x1)

    def zero(self):
        return u64(0x0, 0x0)

    def neg(self):
        return self.bit_not().plus(self.one())

    def minus(self, x):
        return self.plus(x.neg())

    def is_zero(self):
        return self.lo == 0 and self.hi == 0

    def multiply(self, x):
        if self.is_zero():
            return self

        a48 = rshift32b(self.hi, 16)
        a32 = self.hi & 0xFFFF
        a16 = rshift32b(self.lo, 16)
        a00 = self.lo & 0xFFFF

        b48 = rshift32b(x.hi, 16)
        b32 = x.hi & 0xFFFF
        b16 = rshift32b(x.lo, 16)
        b00 = x.lo & 0xFFFF

        c48 = 0
        c32 = 0
        c16 = 0
        c00 = 0
        c00 += a00 * b00
        c16 += rshift32b(c00, 16)
        c00 &= 0xFFFF
        c16 += a16 * b00
        c32 += rshift32b(c16, 16)
        c16 &= 0xFFFF
        c16 += a00 * b16
        c32 += rshift32b(c16, 16)
        c16 &= 0xFFFF
        c32 += a32 * b00
        c48 += rshift32b(c32, 16)
        c32 &= 0xFFFF
        c32 += a16 * b16
        c48 += rshift32b(c32, 16)
        c32 &= 0xFFFF
        c32 += a00 * b32
        c48 += rshift32b(c32, 16)
        c32 &= 0xFFFF
        c48 += a48 * b00 + a32 * b16 + a16 * b32 + a00 * b48
        c48 &= 0xFFFF
        return u64((c48 << 16) | c32, (c16 << 16) | c00)

    def shift_left(self, bits):
        bits = bits % 64
        c = u64(0, 0)
        if bits == 0:
            return self.clone()
        elif bits > 31:
            c.lo = 0
            c.hi = self.lo << (bits - 32)
        else:
            toMoveUp = rshift32b(self.lo, 32 - bits)
            c.lo = self.lo << bits
            c.hi = (self.hi << bits) | toMoveUp
        c.hi &= M32
        c.lo &= M32
        return c

    def set_shift_left(self, bits):
        if bits == 0:
            return self
        if bits > 63:
            bits = bits % 64

        if bits > 31:
            self.hi = self.lo << (bits - 32)
            self.lo = 0
        else:
            toMoveUp = rshift32b(self.lo, 32 - bits)
            self.lo = self.lo << bits
            self.hi = (self.hi << bits) | toMoveUp
        self.hi &= M32
        self.lo &= M32
        return self

    def shift_right(self, bits):
        bits = bits % 64
        c = u64(0, 0)
        if bits == 0:
            return self.clone()
        elif bits >= 32:
            c.hi = 0
            c.lo = rshift32b(self.hi, bits - 32)
        else:
            bitsOff32 = 32 - bits
            toMoveDown = rshift32b(self.hi << bitsOff32, bitsOff32)
            c.hi = rshift32b(self.hi, bits)
            c.lo = rshift32b(self.lo, bits) | (toMoveDown << bitsOff32)
        c.hi &= M32
        c.lo &= M32
        return c

    def rotate_left(self, bits):
        if bits > 32:
            return self.rotate_right(64 - bits)
        c = u64(0, 0)
        if bits == 0:
            c.lo = rshift32b(self.lo, 0)
            c.hi = rshift32b(self.hi, 0)
        elif bits == 32:
            c.lo = self.hi
            c.hi = self.lo
        else:
            c.lo = (self.lo << bits) | rshift32b(self.hi, 32 - bits)
            c.hi = (self.hi << bits) | rshift32b(self.lo, 32 - bits)
        c.hi &= M32
        c.lo &= M32
        return c

    def set_rotate_left(self, bits):
        if bits > 32:
            return self.set_rotate_right(64 - bits)
        if bits == 0:
            return self
        elif bits == 32:
            newHigh = self.lo
            self.lo = self.hi
            self.hi = newHigh
        else:
            newHigh = (self.hi << bits) | rshift32b(self.lo, 32 - bits)
            self.lo = (self.lo << bits) | rshift32b(self.hi, 32 - bits)
            self.hi = newHigh
        self.hi &= M32
        self.lo &= M32
        return self

    def rotate_right(self, bits):
        if bits > 32:
            return self.rotateLeft(64 - bits)
        c = u64(0, 0)
        if bits == 0:
            c.lo = rshift32b(self.lo, 0)
            c.hi = rshift32b(self.hi, 0)
        elif bits == 32:
            c.lo = self.hi
            c.hi = self.lo
        else:
            c.lo = (self.hi << (32 - bits)) | rshift32b(self.lo, bits)
            c.hi = (self.lo << (32 - bits)) | rshift32b(self.hi, bits)
        c.hi &= M32
        c.lo &= M32
        return c

    def set_flip(self):
        newHigh = self.lo
        self.lo = self.hi
        self.hi = newHigh
        return self

    def set_rotate_right(self, bits):
        if bits > 32:
            return self.setRotateLeft(64 - bits)
        if bits == 0:
            return self
        elif bits == 32:
            newHigh
            newHigh = self.lo
            self.lo = self.hi
            self.hi = newHigh
        else:
            newHigh = (self.lo << (32 - bits)) | rshift32b(self.hi, bits)
            self.lo = (self.hi << (32 - bits)) | rshift32b(self.lo, bits)
            self.hi = newHigh
        self.hi &= M32
        self.lo &= M32
        return self

    def xor(self, x):
        c = u64(0, 0)
        c.hi = self.hi ^ x.hi
        c.lo = self.lo ^ x.lo
        return c

    def set_xor_one(self, x):
        self.hi ^= x.hi
        self.lo ^= x.lo
        return self

    def bit_and(self, x):
        c = u64(0, 0)
        c.hi = self.hi & x.hi
        c.lo = self.lo & x.lo
        return c

    def clone(self):
        return u64(self.hi, self.lo)

    def set_xor64(self, *args):
        for a in args:
            self.hi ^= a.hi
            self.lo ^= a.lo
        return self

    @classmethod
    def xor64(cls, *args):
        hi = args[0].hi
        lo = args[0].lo
        for a in args[1:]:
            hi ^= a.hi
            lo ^= a.lo
        return u64(hi, lo)
