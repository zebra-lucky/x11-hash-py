#!/usr/bin/env python
# -*- coding: utf-8 -*-

from struct import pack
from pprint import pprint

from . import op
from .op import u64


Cubehash_BlockSize = 32
Cubehash_StateSize = 32


IV512 = [
    0x2AEA2A61, 0x50F494D4, 0x2D538B8B,
    0x4167D83E, 0x3FEE2313, 0xC701CF8C,
    0xCC39968E, 0x50AC5695, 0x4D42C787,
    0xA647A8B3, 0x97CF0BEF, 0x825B4537,
    0xEEF864D2, 0xF22090C4, 0xD0E5CD33,
    0xA23911AE, 0xFCD398D9, 0x148FE485,
    0x1B017BEF, 0xB6444532, 0x6A536159,
    0x2FF5781C, 0x91FA7934, 0x0DBADEA9,
    0xD65C8A2B, 0xA5A70E75, 0xB1C62456,
    0xBC796576, 0x1921C8F7, 0xE7989AF1,
    0x7795D246, 0xD43E3B44,
]


def ROUND_EVEN(x):
    x[16] = 0xFFFFFFFF & (x[0] + x[16])
    x[0] = op.rotl32(x[0], 7)
    x[17] = 0xFFFFFFFF & (x[1] + x[17])
    x[1] = op.rotl32(x[1], 7)
    x[18] = 0xFFFFFFFF & (x[2] + x[18])
    x[2] = op.rotl32(x[2], 7)
    x[19] = 0xFFFFFFFF & (x[3] + x[19])
    x[3] = op.rotl32(x[3], 7)
    x[20] = 0xFFFFFFFF & (x[4] + x[20])
    x[4] = op.rotl32(x[4], 7)
    x[21] = 0xFFFFFFFF & (x[5] + x[21])
    x[5] = op.rotl32(x[5], 7)
    x[22] = 0xFFFFFFFF & (x[6] + x[22])
    x[6] = op.rotl32(x[6], 7)
    x[23] = 0xFFFFFFFF & (x[7] + x[23])
    x[7] = op.rotl32(x[7], 7)
    x[24] = 0xFFFFFFFF & (x[8] + x[24])
    x[8] = op.rotl32(x[8], 7)
    x[25] = 0xFFFFFFFF & (x[9] + x[25])
    x[9] = op.rotl32(x[9], 7)
    x[26] = 0xFFFFFFFF & (x[10] + x[26])
    x[10] = op.rotl32(x[10], 7)
    x[27] = 0xFFFFFFFF & (x[11] + x[27])
    x[11] = op.rotl32(x[11], 7)
    x[28] = 0xFFFFFFFF & (x[12] + x[28])
    x[12] = op.rotl32(x[12], 7)
    x[29] = 0xFFFFFFFF & (x[13] + x[29])
    x[13] = op.rotl32(x[13], 7)
    x[30] = 0xFFFFFFFF & (x[14] + x[30])
    x[14] = op.rotl32(x[14], 7)
    x[31] = 0xFFFFFFFF & (x[15] + x[31])
    x[15] = op.rotl32(x[15], 7)
    x[8] ^= x[16]
    x[9] ^= x[17]
    x[10] ^= x[18]
    x[11] ^= x[19]
    x[12] ^= x[20]
    x[13] ^= x[21]
    x[14] ^= x[22]
    x[15] ^= x[23]
    x[0] ^= x[24]
    x[1] ^= x[25]
    x[2] ^= x[26]
    x[3] ^= x[27]
    x[4] ^= x[28]
    x[5] ^= x[29]
    x[6] ^= x[30]
    x[7] ^= x[31]
    x[18] = 0xFFFFFFFF & (x[8] + x[18])
    x[8] = op.rotl32(x[8], 11)
    x[19] = 0xFFFFFFFF & (x[9] + x[19])
    x[9] = op.rotl32(x[9], 11)
    x[16] = 0xFFFFFFFF & (x[10] + x[16])
    x[10] = op.rotl32(x[10], 11)
    x[17] = 0xFFFFFFFF & (x[11] + x[17])
    x[11] = op.rotl32(x[11], 11)
    x[22] = 0xFFFFFFFF & (x[12] + x[22])
    x[12] = op.rotl32(x[12], 11)
    x[23] = 0xFFFFFFFF & (x[13] + x[23])
    x[13] = op.rotl32(x[13], 11)
    x[20] = 0xFFFFFFFF & (x[14] + x[20])
    x[14] = op.rotl32(x[14], 11)
    x[21] = 0xFFFFFFFF & (x[15] + x[21])
    x[15] = op.rotl32(x[15], 11)
    x[26] = 0xFFFFFFFF & (x[0] + x[26])
    x[0] = op.rotl32(x[0], 11)
    x[27] = 0xFFFFFFFF & (x[1] + x[27])
    x[1] = op.rotl32(x[1], 11)
    x[24] = 0xFFFFFFFF & (x[2] + x[24])
    x[2] = op.rotl32(x[2], 11)
    x[25] = 0xFFFFFFFF & (x[3] + x[25])
    x[3] = op.rotl32(x[3], 11)
    x[30] = 0xFFFFFFFF & (x[4] + x[30])
    x[4] = op.rotl32(x[4], 11)
    x[31] = 0xFFFFFFFF & (x[5] + x[31])
    x[5] = op.rotl32(x[5], 11)
    x[28] = 0xFFFFFFFF & (x[6] + x[28])
    x[6] = op.rotl32(x[6], 11)
    x[29] = 0xFFFFFFFF & (x[7] + x[29])
    x[7] = op.rotl32(x[7], 11)
    x[12] ^= x[18]
    x[13] ^= x[19]
    x[14] ^= x[16]
    x[15] ^= x[17]
    x[8] ^= x[22]
    x[9] ^= x[23]
    x[10] ^= x[20]
    x[11] ^= x[21]
    x[4] ^= x[26]
    x[5] ^= x[27]
    x[6] ^= x[24]
    x[7] ^= x[25]
    x[0] ^= x[30]
    x[1] ^= x[31]
    x[2] ^= x[28]
    x[3] ^= x[29]


def ROUND_ODD(x):
    x[19] = 0xFFFFFFFF & (x[12] + x[19])
    x[12] = op.rotl32(x[12], 7)
    x[18] = 0xFFFFFFFF & (x[13] + x[18])
    x[13] = op.rotl32(x[13], 7)
    x[17] = 0xFFFFFFFF & (x[14] + x[17])
    x[14] = op.rotl32(x[14], 7)
    x[16] = 0xFFFFFFFF & (x[15] + x[16])
    x[15] = op.rotl32(x[15], 7)
    x[23] = 0xFFFFFFFF & (x[8] + x[23])
    x[8] = op.rotl32(x[8], 7)
    x[22] = 0xFFFFFFFF & (x[9] + x[22])
    x[9] = op.rotl32(x[9], 7)
    x[21] = 0xFFFFFFFF & (x[10] + x[21])
    x[10] = op.rotl32(x[10], 7)
    x[20] = 0xFFFFFFFF & (x[11] + x[20])
    x[11] = op.rotl32(x[11], 7)
    x[27] = 0xFFFFFFFF & (x[4] + x[27])
    x[4] = op.rotl32(x[4], 7)
    x[26] = 0xFFFFFFFF & (x[5] + x[26])
    x[5] = op.rotl32(x[5], 7)
    x[25] = 0xFFFFFFFF & (x[6] + x[25])
    x[6] = op.rotl32(x[6], 7)
    x[24] = 0xFFFFFFFF & (x[7] + x[24])
    x[7] = op.rotl32(x[7], 7)
    x[31] = 0xFFFFFFFF & (x[0] + x[31])
    x[0] = op.rotl32(x[0], 7)
    x[30] = 0xFFFFFFFF & (x[1] + x[30])
    x[1] = op.rotl32(x[1], 7)
    x[29] = 0xFFFFFFFF & (x[2] + x[29])
    x[2] = op.rotl32(x[2], 7)
    x[28] = 0xFFFFFFFF & (x[3] + x[28])
    x[3] = op.rotl32(x[3], 7)
    x[4] ^= x[19]
    x[5] ^= x[18]
    x[6] ^= x[17]
    x[7] ^= x[16]
    x[0] ^= x[23]
    x[1] ^= x[22]
    x[2] ^= x[21]
    x[3] ^= x[20]
    x[12] ^= x[27]
    x[13] ^= x[26]
    x[14] ^= x[25]
    x[15] ^= x[24]
    x[8] ^= x[31]
    x[9] ^= x[30]
    x[10] ^= x[29]
    x[11] ^= x[28]
    x[17] = 0xFFFFFFFF & (x[4] + x[17])
    x[4] = op.rotl32(x[4], 11)
    x[16] = 0xFFFFFFFF & (x[5] + x[16])
    x[5] = op.rotl32(x[5], 11)
    x[19] = 0xFFFFFFFF & (x[6] + x[19])
    x[6] = op.rotl32(x[6], 11)
    x[18] = 0xFFFFFFFF & (x[7] + x[18])
    x[7] = op.rotl32(x[7], 11)
    x[21] = 0xFFFFFFFF & (x[0] + x[21])
    x[0] = op.rotl32(x[0], 11)
    x[20] = 0xFFFFFFFF & (x[1] + x[20])
    x[1] = op.rotl32(x[1], 11)
    x[23] = 0xFFFFFFFF & (x[2] + x[23])
    x[2] = op.rotl32(x[2], 11)
    x[22] = 0xFFFFFFFF & (x[3] + x[22])
    x[3] = op.rotl32(x[3], 11)
    x[25] = 0xFFFFFFFF & (x[12] + x[25])
    x[12] = op.rotl32(x[12], 11)
    x[24] = 0xFFFFFFFF & (x[13] + x[24])
    x[13] = op.rotl32(x[13], 11)
    x[27] = 0xFFFFFFFF & (x[14] + x[27])
    x[14] = op.rotl32(x[14], 11)
    x[26] = 0xFFFFFFFF & (x[15] + x[26])
    x[15] = op.rotl32(x[15], 11)
    x[29] = 0xFFFFFFFF & (x[8] + x[29])
    x[8] = op.rotl32(x[8], 11)
    x[28] = 0xFFFFFFFF & (x[9] + x[28])
    x[9] = op.rotl32(x[9], 11)
    x[31] = 0xFFFFFFFF & (x[10] + x[31])
    x[10] = op.rotl32(x[10], 11)
    x[30] = 0xFFFFFFFF & (x[11] + x[30])
    x[11] = op.rotl32(x[11], 11)
    x[0] ^= x[17]
    x[1] ^= x[16]
    x[2] ^= x[19]
    x[3] ^= x[18]
    x[4] ^= x[21]
    x[5] ^= x[20]
    x[6] ^= x[23]
    x[7] ^= x[22]
    x[8] ^= x[25]
    x[9] ^= x[24]
    x[10] ^= x[27]
    x[11] ^= x[26]
    x[12] ^= x[29]
    x[13] ^= x[28]
    x[14] ^= x[31]
    x[15] ^= x[30]


def SIXTEEN_ROUNDS(x):
    ROUND_EVEN(x)
    ROUND_ODD(x)
    ROUND_EVEN(x)
    ROUND_ODD(x)
    ROUND_EVEN(x)
    ROUND_ODD(x)
    ROUND_EVEN(x)
    ROUND_ODD(x)
    ROUND_EVEN(x)
    ROUND_ODD(x)
    ROUND_EVEN(x)
    ROUND_ODD(x)
    ROUND_EVEN(x)
    ROUND_ODD(x)
    ROUND_EVEN(x)
    ROUND_ODD(x)


def cubehash_update(ctx, msg):
    x = [None] * Cubehash_StateSize
    buf = ctx['buffer']
    ptr = ctx['ptr']
    msg_len = len(msg)
    buf_len = len(buf)
    if msg_len < buf_len - ptr:
        op.buffer_insert(buf, ptr, msg, msg_len)
        ptr += msg_len
        ctx['ptr'] = ptr
        return

    state = ctx['state']
    for i in range(Cubehash_StateSize):
        x[i] = state[i]

    while msg_len > 0:
        clen = buf_len - ptr
        if clen > msg_len:
            clen = msg_len
        op.buffer_insert(buf, ptr, msg, clen)
        ptr += clen
        msg = msg[clen:]
        msg_len -= clen
        if ptr == buf_len:
            buf32 = op.swap32_list(op.bytes_to_i32_list(buf))
            op.buffer_xor_insert(x, 0, buf32, 0, 8)
            SIXTEEN_ROUNDS(x)
            ptr = 0

    ctx['state'] = x
    ctx['ptr'] = ptr


def cubehash_close(ctx):
    x = [None] * Cubehash_StateSize
    buf = ctx['buffer']
    ptr = ctx['ptr']
    buf[ptr] = 0x80
    ptr += 1
    buf_len = len(buf)
    set_len = buf_len - ptr
    buf[ptr:ptr+set_len] = [0] * set_len

    state = ctx['state']
    for i in range(Cubehash_StateSize):
        x[i] = state[i]

    buf32 = op.swap32_list(op.bytes_to_i32_list(buf))
    op.buffer_xor_insert(x, 0, buf32, 0, 8)

    for i in range(11):
        SIXTEEN_ROUNDS(x)
        if i == 0:
            x[31] ^= 0xFFFFFFFF & 1
    ctx['state'] = x
    out = [None] * 16
    for u in range(16):
        out[u] = op.swap32(x[u])
    return out


def pack_state(state):
    res = b''
    for i in state:
        res += pack('>I', i)
    return res


def cubehash(msg):
    ctx = {}
    ctx['state'] = IV512[:]
    ctx['ptr'] = 0
    ctx['buffer'] = bytearray(Cubehash_BlockSize)
    cubehash_update(ctx, msg)
    res = cubehash_close(ctx)
    res = pack_state(res)
    pprint(res.hex())
