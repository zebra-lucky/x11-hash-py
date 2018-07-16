#!/usr/bin/env python
# -*- coding: utf-8 -*-

from struct import pack
from pprint import pprint

from . import op
from .op import u64


CB = [
    u64(0x243f6a88, 0x85a308d3), u64(0x13198a2e, 0x03707344),
    u64(0xa4093822, 0x299f31d0), u64(0x082efa98, 0xec4e6c89),
    u64(0x452821e6, 0x38d01377), u64(0xbe5466cf, 0x34e90c6c),
    u64(0xc0ac29b7, 0xc97c50dd), u64(0x3f84d5b5, 0xb5470917),
    u64(0x9216d5d9, 0x8979fb1b), u64(0xd1310ba6, 0x98dfb5ac),
    u64(0x2ffd72db, 0xd01adfb7), u64(0xb8e1afed, 0x6a267e96),
    u64(0xba7c9045, 0xf12c7f99), u64(0x24a19947, 0xb3916cf7),
    u64(0x0801f2e2, 0x858efc16), u64(0x636920d8, 0x71574e69),
]


Z = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    [14, 10, 4, 8, 9, 15, 13, 6, 1, 12, 0, 2, 11, 7, 5, 3],
    [11, 8, 12, 0, 5, 2, 15, 13, 10, 14, 3, 6, 7, 1, 9, 4],
    [7, 9, 3, 1, 13, 12, 11, 14, 2, 6, 5, 10, 4, 0, 15, 8],
    [9, 0, 5, 7, 2, 4, 10, 15, 14, 1, 11, 12, 6, 8, 3, 13],
    [2, 12, 6, 10, 0, 11, 8, 3, 4, 13, 7, 5, 15, 14, 1, 9],
    [12, 5, 1, 15, 14, 13, 4, 10, 0, 7, 6, 3, 9, 2, 8, 11],
    [13, 11, 7, 14, 12, 1, 3, 9, 5, 0, 15, 4, 8, 6, 2, 10],
    [6, 15, 14, 9, 11, 3, 0, 8, 12, 2, 13, 7, 1, 4, 10, 5],
    [10, 2, 8, 4, 7, 6, 1, 5, 15, 11, 9, 14, 3, 12, 13, 0]
]


initial_values = [
    u64(0x6a09e667, 0xf3bcc908), u64(0xbb67ae85, 0x84caa73b),
    u64(0x3c6ef372, 0xfe94f82b), u64(0xa54ff53a, 0x5f1d36f1),
    u64(0x510e527f, 0xade682d1), u64(0x9b05688c, 0x2b3e6c1f),
    u64(0x1f83d9ab, 0xfb41bd6b), u64(0x5be0cd19, 0x137e2179),
]


def GB(m0, m1, c0, c1, a, b, c, d):
    a.add(m0.xor(c1).add(b))
    d.set_xor_one(a).set_flip()
    c.add(d)
    b.set_xor_one(c).set_rotate_right(25)
    a.add(m1.xor(c0).add(b))
    d.set_xor_one(a).set_rotate_right(16)
    c.add(d)
    b.set_xor_one(c).set_rotate_right(11)


def blake_round(r, V, M):
    GB(M[Z[r][0]], M[Z[r][1]], CB[Z[r][0]], CB[Z[r][1]], V[0], V[4], V[8], V[0xC])
    GB(M[Z[r][2]], M[Z[r][3]], CB[Z[r][2]], CB[Z[r][3]], V[1], V[5], V[9], V[0xD])
    GB(M[Z[r][4]], M[Z[r][5]], CB[Z[r][4]], CB[Z[r][5]], V[2], V[6], V[0xA], V[0xE])
    GB(M[Z[r][6]], M[Z[r][7]], CB[Z[r][6]], CB[Z[r][7]], V[3], V[7], V[0xB], V[0xF])
    GB(M[Z[r][8]], M[Z[r][9]], CB[Z[r][8]], CB[Z[r][9]], V[0], V[5], V[0xA], V[0xF])
    GB(M[Z[r][10]], M[Z[r][11]], CB[Z[r][10]], CB[Z[r][11]], V[1], V[6], V[0xB], V[0xC])
    GB(M[Z[r][12]], M[Z[r][13]], CB[Z[r][12]], CB[Z[r][13]], V[2], V[7], V[8], V[0xD])
    GB(M[Z[r][14]], M[Z[r][15]], CB[Z[r][14]], CB[Z[r][15]], V[3], V[4], V[9], V[0xE])


def compress(M, H, S, T0, T1):
    V = [None] * 16
    op.buffer_insert_u64(V, 0, H, 8)
    V[8] = S[0].xor(CB[0])
    V[9] = S[1].xor(CB[1])
    V[10] = S[2].xor(CB[2])
    V[11] = S[3].xor(CB[3])
    V[12] = T0.xor(CB[4])
    V[13] = T0.xor(CB[5])
    V[14] = T1.xor(CB[6])
    V[15] = T1.xor(CB[7])
    for i in range(16):
        blake_round(i % 10, V, M)
    for i in range(8):
        H[i] = u64.xor64(H[i], S[i%4], V[i], V[8+i])


def blake_update(ctx, msg):
    buf = ctx['buffer']
    ptr = ctx['ptr']
    msg_len = len(msg)
    buf_len = len(buf)

    if msg_len < buf_len - ptr:
        msg_end = ptr + msg_len
        buf[ptr:msg_end] = msg
        ctx['ptr'] = msg_end
        return

    H = [None] * 8
    S = [None] * 4
    T0 = ctx['T0'].clone()
    T1 = ctx['T1'].clone()

    op.buffer_insert_u64(H, 0, ctx['state'], 8)
    op.buffer_insert_u64(S, 0, ctx['salt'], 4)
    while msg_len > 0:
        clen = buf_len - ptr
        if clen > msg_len:
            clen = msg_len

        clen_end = ptr + clen
        buf[ptr:clen_end] = msg[:clen]
        ptr = clen_end
        msg = msg[clen:]
        msg_len -= clen

        if ptr == buf_len:
            T0.add(u64(0, 1024))
            if T0.hi < 0 or T0.lo < 1024:
                 T1.add_one()

            buf64 = op.bytes_to_u64_list(buf, buf_len)
            compress(buf64, H, S, T0, T1)
            ptr = 0

    ctx['state'] = H
    ctx['salt'] = S
    ctx['T0'] = T0
    ctx['T1'] = T1
    ctx['ptr'] = ptr


def blake_close(ctx):
    buf = bytearray(128)
    ptr = ctx['ptr']
    bit_len = u64(0, ptr).shift_left(3)
    T0 = ctx['T0']
    T1 = ctx['T1']
    tl = T0.plus(bit_len)
    th = T1.clone()

    buf[ptr] = 0x80
    if ptr == 0:
        T0 = u64(0xFFFFFFFF, 0xFFFFFC00)
        T1 = u64(0xFFFFFFFF, 0xFFFFFFFF)
    elif T0.is_zero():
        T0 = u64(0xFFFFFFFF, 0xFFFFFC00).plus(bit_len)
        T1 = T1.minus(u64(0, 1))
    else:
        T0 = T0.minus(u64(0, 1024).minus(bit_len))

    ctx['T0'] = T0.clone()
    ctx['T1'] = T1.clone()

    if bit_len.lo <= 894:
        set_len = 111 - ptr
        buf[ptr+1:ptr+1+set_len] = [0] * set_len
        buf[111] |= 1
        buf[112:112+4] = pack('>I', th.hi)
        buf[116:116+4] = pack('>I', th.lo)
        buf[120:120+4] = pack('>I', tl.hi)
        buf[124:124+4] = pack('>I', tl.lo)
        blake_update(ctx, buf[ptr:])
    else:
        set_len = 127 - ptr
        buf[ptr+1:ptr+1+set_len] = [0] * set_len
        blake_update(ctx, buf[ptr:])
        ctx['T0'] = u64(0xFFFFFFFF, 0xFFFFFC00)
        ctx['T1'] = u64(0xFFFFFFFF, 0xFFFFFFFF)
        buf[0:112] = [0] * 112
        buf[111] = 1
        buf[112:112+4] = pack('>I', th.hi)
        buf[116:116+4] = pack('>I', th.lo)
        buf[120:120+4] = pack('>I', tl.hi)
        buf[124:124+4] = pack('>I', tl.lo)
        blake_update(ctx, buf)


def pack_state(state):
    res = b''
    for u64v in state:
        res += pack('>I', u64v.hi)
        res += pack('>I', u64v.lo)
    return res


def blake(msg):
    ctx = {}
    ctx['state'] = initial_values[:]
    ctx['salt'] = [u64(0, 0), u64(0, 0), u64(0, 0), u64(0, 0)]
    ctx['T0'] = u64(0, 0)
    ctx['T1'] = u64(0, 0)
    ctx['ptr'] = 0
    ctx['buffer'] = bytearray(128)
    blake_update(ctx, msg)
    blake_close(ctx)
    res = pack_state(ctx['state'])
    pprint(res.hex())
