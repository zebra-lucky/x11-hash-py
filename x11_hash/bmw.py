#!/usr/bin/env python
# -*- coding: utf-8 -*-

from struct import pack
from pprint import pprint

from . import op
from .op import u64


V_INIT = [
    u64(0x80818283, 0x84858687), u64(0x88898A8B, 0x8C8D8E8F),
    u64(0x90919293, 0x94959697), u64(0x98999A9B, 0x9C9D9E9F),
    u64(0xA0A1A2A3, 0xA4A5A6A7), u64(0xA8A9AAAB, 0xACADAEAF),
    u64(0xB0B1B2B3, 0xB4B5B6B7), u64(0xB8B9BABB, 0xBCBDBEBF),
    u64(0xC0C1C2C3, 0xC4C5C6C7), u64(0xC8C9CACB, 0xCCCDCECF),
    u64(0xD0D1D2D3, 0xD4D5D6D7), u64(0xD8D9DADB, 0xDCDDDEDF),
    u64(0xE0E1E2E3, 0xE4E5E6E7), u64(0xE8E9EAEB, 0xECEDEEEF),
    u64(0xF0F1F2F3, 0xF4F5F6F7), u64(0xF8F9FAFB, 0xFCFDFEFF),
]


final = [
    u64(0xaaaaaaaa, 0xaaaaaaa0), u64(0xaaaaaaaa, 0xaaaaaaa1),
    u64(0xaaaaaaaa, 0xaaaaaaa2), u64(0xaaaaaaaa, 0xaaaaaaa3),
    u64(0xaaaaaaaa, 0xaaaaaaa4), u64(0xaaaaaaaa, 0xaaaaaaa5),
    u64(0xaaaaaaaa, 0xaaaaaaa6), u64(0xaaaaaaaa, 0xaaaaaaa7),
    u64(0xaaaaaaaa, 0xaaaaaaa8), u64(0xaaaaaaaa, 0xaaaaaaa9),
    u64(0xaaaaaaaa, 0xaaaaaaaa), u64(0xaaaaaaaa, 0xaaaaaaab),
    u64(0xaaaaaaaa, 0xaaaaaaac), u64(0xaaaaaaaa, 0xaaaaaaad),
    u64(0xaaaaaaaa, 0xaaaaaaae), u64(0xaaaaaaaa, 0xaaaaaaaf),
]


sb_a = [1, 1, 2, 2, 1, 2]
sb_b = [3, 2, 1, 2]
sb_c = [4, 13, 19, 28]
sb_d = [37, 43, 53, 59]


I16 = [None] * 16
I16.append([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
I16.append([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])
I16.append([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17])
I16.append([3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18])
I16.append([4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19])
I16.append([5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
I16.append([6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21])
I16.append([7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22])
I16.append([8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23])
I16.append([9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24])
I16.append([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25])
I16.append([11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26])
I16.append([12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27])
I16.append([13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28])
I16.append([14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29])
I16.append([15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30])


M16 = [None] * 16
M16.append([0, 1, 3, 4, 7, 10, 11])
M16.append([1, 2, 4, 5, 8, 11, 12])
M16.append([2, 3, 5, 6, 9, 12, 13])
M16.append([3, 4, 6, 7, 10, 13, 14])
M16.append([4, 5, 7, 8, 11, 14, 15])
M16.append([5, 6, 8, 9, 12, 15, 16])
M16.append([6, 7, 9, 10, 13, 0, 1])
M16.append([7, 8, 10, 11, 14, 1, 2])
M16.append([8, 9, 11, 12, 15, 2, 3])
M16.append([9, 10, 12, 13, 0, 3, 4])
M16.append([10, 11, 13, 14, 1, 4, 5])
M16.append([11, 12, 14, 15, 2, 5, 6])
M16.append([12, 13, 15, 16, 3, 6, 7])
M16.append([13, 14, 0, 1, 4, 7, 8])
M16.append([14, 15, 1, 2, 5, 8, 9])
M16.append([15, 16, 2, 3, 6, 9, 10])


def sb(n, x):
    if n >= 4:
        return x.shift_right(sb_a[n]).xor(x)

    return u64.xor64(
        x.shift_right(sb_a[n]),
        x.shift_left(sb_b[n]),
        x.rotate_left(sb_c[n]),
        x.rotate_left(sb_d[n])
    )


rbn = [0, 5, 11, 27, 32, 37, 43, 53]


def rb(n, x):
    return x.rotate_left(rbn[n])


def makeW(M,H,i, op):
    a = M[i[0]].xor(H[i[0]])
    b = M[i[1]].xor(H[i[1]])
    c = M[i[2]].xor(H[i[2]])
    d = M[i[3]].xor(H[i[3]])
    e = M[i[4]].xor(H[i[4]])
    w = op[3](op[2](op[1](op[0](a,b),c),d),e)
    return w


wbn = [
    [5, 7, 10, 13, 14],
    [6, 8, 11, 14, 15],
    [0, 7, 9, 12, 15],
    [0, 1, 8, 10, 13],
    [1, 2, 9, 11, 14],
    [3, 2, 10, 12, 15],
    [4, 0, 3, 11, 13],
    [1, 4, 5, 12, 14],
    [2, 5, 6, 13, 15],
    [0, 3, 6, 7, 14],
    [8, 1, 4, 7, 15],
    [8, 0, 2, 5, 9],
    [1, 3, 6, 9, 10],
    [2, 4, 7, 10, 11],
    [3, 5, 8, 11, 12],
    [12, 4, 6, 9, 13],
]

def plus(a,b):
    return a.plus(b)


def minus(a,b):
    return a.minus(b)


wboperators = [
    [minus, plus, plus, plus],
    [minus, plus, plus, minus],
    [plus, plus, minus, plus],
    [minus, plus, minus, plus],
    [plus, plus, minus, minus],
    [minus, plus, minus, plus],
    [minus, minus, minus, plus],
    [minus, minus, minus, minus],
    [minus, minus, plus, minus],
    [minus, plus, minus, plus],
    [minus, minus, minus, plus],
    [minus, minus, minus, plus],
    [plus, minus, minus, plus],
    [plus, plus, plus, plus],
    [minus, plus, minus, minus],
    [minus, minus, minus, plus],
]


def wb(M,H,i):
    return makeW(M,H,wbn[i],wboperators[i])


def kb(j):
    fives = u64(0x05555555, 0x55555555)
    return fives.multiply(u64(0, j))


def addElt(buffer64, state, mVars, i):
    k = kb(i)
    elt = (buffer64[mVars[0]].rotate_left(mVars[1])
        .add(buffer64[mVars[2]].rotate_left(mVars[3]))
        .minus(buffer64[mVars[5]].rotate_left(mVars[6]))
        .add(k)
        .xor(state[mVars[4]]))
    return elt


def expand2Inner(qt, mf, state, i, iVars, mVars):
    return (qt[iVars[0]]
        .plus(rb(1, qt[iVars[1]]))
        .add(qt[iVars[2]])
        .add(rb(2, qt[iVars[3]]))
        .add(qt[iVars[4]])
        .add(rb(3, qt[iVars[5]]))
        .add(qt[iVars[6]])
        .add(rb(4, qt[iVars[7]]))
        .add(qt[iVars[8]])
        .add(rb(5, qt[iVars[9]]))
        .add(qt[iVars[10]])
        .add(rb(6, qt[iVars[11]]))
        .add(qt[iVars[12]])
        .add(rb(7, qt[iVars[13]]))
        .add(sb(4, qt[iVars[14]]))
        .add(sb(5, qt[iVars[15]]))
        .add(addElt(mf, state, mVars, i)))


def expand1Inner(qt, mf, state, i, iVars, mVars):
    return (sb(1, qt[iVars[0]])
        .add(sb(2, qt[iVars[1]]))
        .add(sb(3, qt[iVars[2]]))
        .add(sb(0, qt[iVars[3]]))
        .add(sb(1, qt[iVars[4]]))
        .add(sb(2, qt[iVars[5]]))
        .add(sb(3, qt[iVars[6]]))
        .add(sb(0, qt[iVars[7]]))
        .add(sb(1, qt[iVars[8]]))
        .add(sb(2, qt[iVars[9]]))
        .add(sb(3, qt[iVars[10]]))
        .add(sb(0, qt[iVars[11]]))
        .add(sb(1, qt[iVars[12]]))
        .add(sb(2, qt[iVars[13]]))
        .add(sb(3, qt[iVars[14]]))
        .add(sb(0, qt[iVars[15]]))
        .add(addElt(mf, state, mVars, i)))


def expand1b(qt, mf, state, i):
    iVars = I16[i]
    mVars = M16[i]
    return expand1Inner(qt, mf, state, i, iVars, mVars)


def expand2b(qt, mf, state, i):
    iVars = I16[i]
    mVars = M16[i]
    return expand2Inner(qt, mf, state, i, iVars, mVars)


def makeQ(mf, state):
    qt = [None] * 32
    for i in range(16):
        w = wb(mf,state,i)
        s = sb(i % 5, w)
        qt[i] = s.plus(state[(i + 1) % 16])
    qt[16] = expand1b(qt, mf, state, 16)
    qt[17] = expand1b(qt, mf, state, 17)
    for i in range(18, 32):
        qt[i] = expand2b(qt, mf, state, i)

    return qt


def fold(int64Buffer, state):
    out = [None] * 16
    qt = makeQ(int64Buffer, state)
    xl = u64.xor64(qt[16], qt[17], qt[18], qt[19], qt[20], qt[21], qt[22], qt[23])
    xh = u64.xor64(xl, qt[24], qt[25], qt[26], qt[27], qt[28], qt[29], qt[30], qt[31])
    out[0] = u64.xor64(xh.shift_left(5), qt[16].shift_right(5), int64Buffer[0]).add(u64.xor64(xl, qt[24], qt[0]))
    out[1] = u64.xor64(xh.shift_right(7), qt[17].shift_left(8), int64Buffer[1]).add(u64.xor64(xl, qt[25], qt[1]))
    out[2] = u64.xor64(xh.shift_right(5), qt[18].shift_left(5), int64Buffer[2]).add(u64.xor64(xl, qt[26], qt[2]))
    out[3] = u64.xor64(xh.shift_right(1), qt[19].shift_left(5), int64Buffer[3]).add(u64.xor64(xl, qt[27], qt[3]))
    out[4] = u64.xor64(xh.shift_right(3), qt[20], int64Buffer[4]).add(u64.xor64(xl, qt[28], qt[4]))
    out[5] = u64.xor64(xh.shift_left(6), qt[21].shift_right(6), int64Buffer[5]).add(u64.xor64(xl, qt[29], qt[5]))
    out[6] = u64.xor64(xh.shift_right(4), qt[22].shift_left(6), int64Buffer[6]).add(u64.xor64(xl, qt[30], qt[6]))
    out[7] = u64.xor64(xh.shift_right(11), qt[23].shift_left(2), int64Buffer[7]).add(u64.xor64(xl, qt[31], qt[7]))
    out[8] = (out[4].rotate_left(9).add(u64.xor64(xh, qt[24], int64Buffer[8]))
        .add(u64.xor64(xl.shift_left(8), qt[23], qt[8])))
    out[9] = (out[5].rotate_left(10).add(u64.xor64(xh, qt[25], int64Buffer[9]))
        .add(u64.xor64(xl.shift_right(6), qt[16], qt[9])))
    out[10] = (out[6].rotate_left(11).add(u64.xor64(xh, qt[26], int64Buffer[10]))
        .add(u64.xor64(xl.shift_left(6), qt[17], qt[10])))
    out[11] = (out[7].rotate_left(12).add(u64.xor64(xh, qt[27], int64Buffer[11]))
        .add(u64.xor64(xl.shift_left(4), qt[18], qt[11])))
    out[12] = (out[0].rotate_left(13).add(u64.xor64(xh, qt[28], int64Buffer[12]))
        .add(u64.xor64(xl.shift_right(3), qt[19], qt[12])))
    out[13] = (out[1].rotate_left(14).add(u64.xor64(xh, qt[29], int64Buffer[13]))
        .add(u64.xor64(xl.shift_right(4), qt[20], qt[13])))
    out[14] = (out[2].rotate_left(15).add(u64.xor64(xh, qt[30], int64Buffer[14]))
        .add(u64.xor64(xl.shift_right(7), qt[21], qt[14])))
    out[15] = (out[3].rotate_left(16).add(u64.xor64(xh, qt[31], int64Buffer[15]))
        .add(u64.xor64(xl.shift_right(2), qt[22], qt[15])))
    return out


def compress(buf, state):
    buf64 = op.bytes_to_u64_list_le(buf, len(buf))
    return fold(buf64, state)


def bmw_update(ctx, msg):
    htmp = [None] * 16
    msg_len = len(msg)
    lenL3 = u64(0, msg_len)
    lenL3 = lenL3.shift_left(3)
    ctx['bitCount'].add(lenL3)
    buf = ctx['buffer']
    buf_len = len(buf)
    ptr = ctx['ptr']
    h1 = ctx['state']
    h2 = htmp
    while msg_len > 0:
        clen = buf_len - ptr
        if clen > msg_len:
            clen = msg_len
        op.buffer_insert(buf, ptr, msg, clen)
        msg = msg[clen:]
        msg_len -= clen
        ptr += clen
        if ptr is buf_len:
            h2 = compress(buf, h1)
            ht = h1
            h1 = h2
            h2 = ht
            ptr = 0


    ctx['ptr'] = ptr
    state = ctx['state']
    if h1 is not state:
        state_len = len(state)
        op.buffer_insert(state, 0, h1, state_len)

def bmw_close(ctx):
    h2 = [None] * 16

    buf = ctx['buffer']
    ptr = ctx['ptr']
    buf_len = len(buf)
    buf[ptr] = 0x80
    ptr += 1
    hState = ctx['state']
    if ptr > buf_len - 8:
        set_len = buf_len - ptr
        buf[ptr:ptr+set_len] = [0] * set_len
        hState = compress(buf, hState)
        ptr = 0

    set_len = buf_len - 8 - ptr
    buf[ptr:ptr+set_len] = [0] * set_len
    enc_pos = buf_len - 8
    enc_data = ctx['bitCount']
    buf[enc_pos+0:enc_pos+4] = pack('<I', enc_data.lo)
    buf[enc_pos+4:enc_pos+8] = pack('<I', enc_data.hi)
    h2 = compress(buf, hState)
    for u in range(16):
        enc_pos = 8 * u
        enc_data = h2[u]
        buf[enc_pos+0:enc_pos+4] = pack('<I', enc_data.lo)
        buf[enc_pos+4:enc_pos+8] = pack('<I', enc_data.hi)
    h1 = compress(buf, final)
    out = [None] * 16
    for u in range(8):
        v = u + 8
        out[2 * u] = op.swap32(h1[v].lo)
        out[2 * u + 1] = op.swap32(h1[v].hi)

    return out


def pack_state(state):
    res = b''
    for i in state:
        res += pack('>I', i)
    return res


def bmw(msg):
    ctx = {}
    ctx['state'] = V_INIT[:]
    ctx['ptr'] = 0
    ctx['bitCount'] = u64(0,0)
    ctx['buffer'] = bytearray(128)
    bmw_update(ctx, msg)
    res = bmw_close(ctx)
    res = pack_state(res)
    pprint(res.hex())
