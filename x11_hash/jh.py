#!/usr/bin/env python
# -*- coding: utf-8 -*-

from struct import pack
from pprint import pprint

from . import op
from .op import u64


Jh_BlockSize = 64
Jh_StateSize = 32


JH_HX = 8
JH_HY = 4


IV512 = [
    (0x6fd14b96), (0x3e00aa17), (0x636a2e05), (0x7a15d543),
    (0x8a225e8d), (0x0c97ef0b), (0xe9341259), (0xf2b3c361),
    (0x891da0c1), (0x536f801e), (0x2aa9056b), (0xea2b6d80),
    (0x588eccdb), (0x2075baa6), (0xa90f3a76), (0xbaf83bf7),
    (0x0169e605), (0x41e34a69), (0x46b58a8e), (0x2e6fe65a),
    (0x1047a7d0), (0xc1843c24), (0x3b6e71b1), (0x2d5ac199),
    (0xcf57f6ec), (0x9db1f856), (0xa706887c), (0x5716b156),
    (0xe3c2fcdf), (0xe68517fb), (0x545a4678), (0xcc8cdd4b),
]


C = [
    0xa2ded572, 0x67f815df, 0x0a15847b, 0x571523b7, 0x90d6ab81, 0xf6875a4d,
    0xc54f9f4e, 0x402bd1c3, 0xe03a98ea, 0x9cfa455c, 0x99d2c503, 0x9a99b266,
    0xb4960266, 0x8a53bbf2, 0x1a1456b5, 0x31a2db88, 0x5c5aa303, 0xdb0e199a,
    0x0ab23f40, 0x1044c187, 0x8019051c, 0x1d959e84, 0xadeb336f, 0xdccde75e,
    0x9213ba10, 0x416bbf02, 0x156578dc, 0xd027bbf7, 0x39812c0a, 0x5078aa37,
    0xd2bf1a3f, 0xd3910041, 0x0d5a2d42, 0x907eccf6, 0x9c9f62dd, 0xce97c092,
    0x0ba75c18, 0xac442bc7, 0xd665dfd1, 0x23fcc663, 0x036c6e97, 0x1ab8e09e,
    0x7e450521, 0xa8ec6c44, 0xbb03f1ee, 0xfa618e5d, 0xb29796fd, 0x97818394,
    0x37858e4a, 0x2f3003db, 0x2d8d672a, 0x956a9ffb, 0x8173fe8a, 0x6c69b8f8,
    0x4672c78a, 0x14427fc0, 0x8f15f4c5, 0xc45ec7bd, 0xa76f4475, 0x80bb118f,
    0xb775de52, 0xbc88e4ae, 0x1e00b882, 0xf4a3a698, 0x338ff48e, 0x1563a3a9,
    0x24565faa, 0x89f9b7d5, 0x20edf1b6, 0xfde05a7c, 0x5ae9ca36, 0x362c4206,
    0x433529ce, 0x3d98fe4e, 0x74f93a53, 0xa74b9a73, 0x591ff5d0, 0x86814e6f,
    0x81ad9d0e, 0x9f5ad8af, 0x670605a7, 0x6a6234ee, 0xbe280b8b, 0x2717b96e,
    0x26077447, 0x3f1080c6, 0x6f7ea0e0, 0x7b487ec6, 0xa50a550d, 0xc0a4f84a,
    0x9fe7e391, 0x9ef18e97, 0x81727686, 0xd48d6050, 0x415a9e7e, 0x62b0e5f3,
    0xec1f9ffc, 0x7a205440, 0x001ae4e3, 0x84c9f4ce, 0xf594d74f, 0xd895fa9d,
    0x117e2e55, 0xa554c324, 0x2872df5b, 0x286efebd, 0xe27ff578, 0xb2c4a50f,
    0xef7c8905, 0x2ed349ee, 0x85937e44, 0x7f5928eb, 0x37695f70, 0x4a3124b3,
    0xf128865e, 0x65e4d61d, 0x04771bc7, 0xe720b951, 0xe843fe74, 0x8a87d423,
    0xa3e8297d, 0xf2947692, 0x097acbdd, 0xc1d9309b, 0xfb301b1d, 0xe01bdc5b,
    0x4f4924da, 0xbf829cf2, 0x31bae7a4, 0xffbf70b4, 0x0544320d, 0x48bcf8de,
    0x32fcae3b, 0x39d3bb53, 0xc1c39f45, 0xa08b29e0, 0xfd05c9e5, 0x0f09aef7,
    0x12347094, 0x34f19042, 0x01b771a2, 0x95ed44e3, 0x368e3be9, 0x4a982f4f,
    0x631d4088, 0x15f66ca0, 0x4b44c147, 0xffaf5287, 0xf14abb7e, 0x30c60ae2,
    0xc5b67046, 0xe68c6ecc, 0x56a4d5a4, 0x00ca4fbd, 0x4b849dda, 0xae183ec8,
    0x45ce5773, 0xadd16430, 0x68cea6e8, 0x67255c14, 0xf28cdaa3, 0x16e10ecb,
    0x5806e933, 0x9a99949a, 0x20b2601f, 0x7b846fc2, 0x7facced1, 0x1885d1a0,
    0xa15b5932, 0xd319dd8d, 0xc01c9a50, 0x46b4a5aa, 0x67633d9f, 0xba6b04e4,
    0xab19caf6, 0x7eee560b, 0xea79b11f, 0x742128a9, 0x35f7bde9, 0xee51363b,
    0x5aac571d, 0x76d35075, 0xfec2463a, 0x01707da3, 0xafc135f7, 0x42d8a498,
    0x20eced78, 0x79676b9e, 0x15638341, 0xa8db3aea, 0x4d3bc3fa, 0x832c8332,
    0x1f3b40a7, 0xf347271c, 0x34f04059, 0x9a762db7, 0x6c4e3ee7, 0xfd4f21d2,
    0x398dfdb8, 0xef5957dc, 0x490c9b8d, 0xdaeb492b, 0x49d7a25b, 0x0d70f368,
    0xd0ae3b7d, 0x84558d7a, 0xf0e9a5f5, 0x658ef8e4, 0xf4a2b8a0, 0x533b1036,
    0x9e07a80c, 0x5aec3e75, 0x92946891, 0x4f88e856, 0x555cb05b, 0x4cbcbaf8,
    0x993bbbe3, 0x7b9487f3, 0xd6f4da75, 0x5d1c6b72, 0x28acae64, 0x6db334dc,
    0x50a5346c, 0x71db28b8, 0xf2e261f8, 0x2a518d10, 0x3364dbe3, 0xfc75dd59,
    0xf1bcac1c, 0xa23fce43, 0x3cd1bb67, 0xb043e802, 0xca5b0a33, 0x75a12988,
    0x4d19347f, 0x5c5316b4, 0xc3943b92, 0x1e4d790e, 0xd7757479, 0x3fafeeb6,
    0xf7d4a8ea, 0x21391abe, 0x097ef45c, 0x5127234c, 0x5324a326, 0xd23c32ba,
    0x4a17a344, 0xadd5a66d, 0xa63e1db5, 0x08c9f2af, 0x983d5983, 0x563c6b91,
    0xa17cf84c, 0x4d608672, 0xcc3ee246, 0xf6c76e08, 0xb333982f, 0x5e76bcb1,
    0xa566d62b, 0x2ae6c4ef, 0xe8b6f406, 0x36d4c1be, 0x1582ee74, 0x6321efbc,
    0x0d4ec1fd, 0x69c953f4, 0xc45a7da7, 0x26585806, 0x1614c17e, 0x16fae006,
    0x3daf907e, 0x3f9d6328, 0xe3f2c9d2, 0x0cd29b00, 0x30ceaa5f, 0x300cd4b7,
    0x16512a74, 0x9832e0f2, 0xd830eb0d, 0x9af8cee3, 0x7b9ec54b, 0x9279f1b5,
    0x6ee651ff, 0xd3688604, 0x574d239b, 0x316796e6, 0xf3a6e6cc, 0x05750a17,
    0xd98176b1, 0xce6c3213, 0x8452173c, 0x62a205f8, 0xb3cb2bf4, 0x47154778,
    0x825446ff, 0x486a9323, 0x0758df38, 0x65655e4e, 0x897cfcf2, 0x8e5086fc,
    0x442e7031, 0x86ca0bd0, 0xa20940f0, 0x4e477830, 0x39eea065, 0x8338f7d1,
    0x37e95ef7, 0xbd3a2ce4, 0x26b29721, 0x6ff81301, 0xd1ed44a3, 0xe7de9fef,
    0x15dfa08b, 0xd9922576, 0xf6f7853c, 0xbe42dc12, 0x7ceca7d8, 0x7eb027ab,
    0xda7d8d53, 0xdea83eaa, 0x93ce25aa, 0xd86902bd, 0xfd43f65a, 0xf908731a,
    0xdaef5fc0, 0xa5194a17, 0x33664d97, 0x6a21fd4c, 0x3198b435, 0x701541db,
    0xbb0f1eea, 0x9b54cded, 0xa163d09a, 0x72409751, 0xbf9d75f6, 0xe26f4791,
]


def Sb(x, c):
    x[3] = ~x[3]
    x[0] ^= (c) & ~x[2]
    tmp = (c) ^ (x[0] & x[1])
    x[0] ^= x[2] & x[3]
    x[3] ^= ~x[1] & x[2]
    x[1] ^= x[0] & x[2]
    x[2] ^= x[0] & ~x[3]
    x[0] ^= x[1] | x[3]
    x[3] ^= x[1] & x[2]
    x[1] ^= tmp & x[0]
    x[2] ^= tmp
    return x


def Lb(x):
    x[4] ^= x[1]
    x[5] ^= x[2]
    x[6] ^= x[3] ^ x[0]
    x[7] ^= x[0]
    x[0] ^= x[5]
    x[1] ^= x[6]
    x[2] ^= x[7] ^ x[4]
    x[3] ^= x[4]
    return x


def Ceven(n, r):
    return C[((r) << 3) + 3 - n]


def Codd(n, r):
    return C[((r) << 3) + 7 - n]


def S(x0, x1, x2, x3, cb, r):
    x = Sb([x0[3], x1[3], x2[3], x3[3]], cb(3, r))
    x0[3] = x[0]
    x1[3] = x[1]
    x2[3] = x[2]
    x3[3] = x[3]
    x = Sb([x0[2], x1[2], x2[2], x3[2]], cb(2, r))
    x0[2] = x[0]
    x1[2] = x[1]
    x2[2] = x[2]
    x3[2] = x[3]
    x = Sb([x0[1], x1[1], x2[1], x3[1]], cb(1, r))
    x0[1] = x[0]
    x1[1] = x[1]
    x2[1] = x[2]
    x3[1] = x[3]
    x = Sb([x0[0], x1[0], x2[0], x3[0]], cb(0, r))
    x0[0] = x[0]
    x1[0] = x[1]
    x2[0] = x[2]
    x3[0] = x[3]


def L(x0, x1, x2, x3, x4, x5, x6, x7):
    x = Lb([x0[3], x1[3], x2[3], x3[3], x4[3], x5[3], x6[3], x7[3]])
    x0[3] = x[0]
    x1[3] = x[1]
    x2[3] = x[2]
    x3[3] = x[3]
    x4[3] = x[4]
    x5[3] = x[5]
    x6[3] = x[6]
    x7[3] = x[7]
    x = Lb([x0[2], x1[2], x2[2], x3[2], x4[2], x5[2], x6[2], x7[2]])
    x0[2] = x[0]
    x1[2] = x[1]
    x2[2] = x[2]
    x3[2] = x[3]
    x4[2] = x[4]
    x5[2] = x[5]
    x6[2] = x[6]
    x7[2] = x[7]
    x = Lb([x0[1], x1[1], x2[1], x3[1], x4[1], x5[1], x6[1], x7[1]])
    x0[1] = x[0]
    x1[1] = x[1]
    x2[1] = x[2]
    x3[1] = x[3]
    x4[1] = x[4]
    x5[1] = x[5]
    x6[1] = x[6]
    x7[1] = x[7]
    x = Lb([x0[0], x1[0], x2[0], x3[0], x4[0], x5[0], x6[0], x7[0]])
    x0[0] = x[0]
    x1[0] = x[1]
    x2[0] = x[2]
    x3[0] = x[3]
    x4[0] = x[4]
    x5[0] = x[5]
    x6[0] = x[6]
    x7[0] = x[7]


def Wz(x, c, n):
    t = (x[3] & (c)) << (n)
    x[3] = ((x[3] >> (n)) & (c)) | t
    t = (x[2] & (c)) << (n)
    x[2] = ((x[2] >> (n)) & (c)) | t
    t = (x[1] & (c)) << (n)
    x[1] = ((x[1] >> (n)) & (c)) | t
    t = (x[0] & (c)) << (n)
    x[0] = ((x[0] >> (n)) & (c)) | t


def W(ro, x):
    if ro == 0:
        return Wz(x, (0x55555555), 1)
    elif ro == 1:
        return Wz(x, (0x33333333), 2)
    elif ro == 2:
        return Wz(x, (0x0F0F0F0F), 4)
    elif ro == 3:
        return Wz(x, (0x00FF00FF), 8)
    elif ro == 4:
        return Wz(x, (0x0000FFFF), 16)
    elif ro == 5:
        t = x[3]
        x[3] = x[2]
        x[2] = t
        t = x[1]
        x[1] = x[0]
        x[0] = t
        return
    elif ro == 6:
        t = x[3]
        x[3] = x[1]
        x[1] = t
        t = x[2]
        x[2] = x[0]
        x[0] = t


def SL(h, r, ro):
    S(h[0], h[2], h[4], h[6], Ceven, r)
    S(h[1], h[3], h[5], h[7], Codd, r)
    L(h[0], h[2], h[4], h[6], h[1], h[3], h[5], h[7])
    W(ro, h[1])
    W(ro, h[3])
    W(ro, h[5])
    W(ro, h[7])


def READ_STATE(h, state):
    h[0][3] = state[0]
    h[0][2] = state[1]
    h[0][1] = state[2]
    h[0][0] = state[3]
    h[1][3] = state[4]
    h[1][2] = state[5]
    h[1][1] = state[6]
    h[1][0] = state[7]
    h[2][3] = state[8]
    h[2][2] = state[9]
    h[2][1] = state[10]
    h[2][0] = state[11]
    h[3][3] = state[12]
    h[3][2] = state[13]
    h[3][1] = state[14]
    h[3][0] = state[15]
    h[4][3] = state[16]
    h[4][2] = state[17]
    h[4][1] = state[18]
    h[4][0] = state[19]
    h[5][3] = state[20]
    h[5][2] = state[21]
    h[5][1] = state[22]
    h[5][0] = state[23]
    h[6][3] = state[24]
    h[6][2] = state[25]
    h[6][1] = state[26]
    h[6][0] = state[27]
    h[7][3] = state[28]
    h[7][2] = state[29]
    h[7][1] = state[30]
    h[7][0] = state[31]


def WRITE_STATE(h, state):
    state[0] = h[0][3]
    state[1] = h[0][2]
    state[2] = h[0][1]
    state[3] = h[0][0]
    state[4] = h[1][3]
    state[5] = h[1][2]
    state[6] = h[1][1]
    state[7] = h[1][0]
    state[8] = h[2][3]
    state[9] = h[2][2]
    state[10] = h[2][1]
    state[11] = h[2][0]
    state[12] = h[3][3]
    state[13] = h[3][2]
    state[14] = h[3][1]
    state[15] = h[3][0]
    state[16] = h[4][3]
    state[17] = h[4][2]
    state[18] = h[4][1]
    state[19] = h[4][0]
    state[20] = h[5][3]
    state[21] = h[5][2]
    state[22] = h[5][1]
    state[23] = h[5][0]
    state[24] = h[6][3]
    state[25] = h[6][2]
    state[26] = h[6][1]
    state[27] = h[6][0]
    state[28] = h[7][3]
    state[29] = h[7][2]
    state[30] = h[7][1]
    state[31] = h[7][0]


def E8(h):
    for r in range(0, 42, 7):
        SL(h, r + 0, 0)
        SL(h, r + 1, 1)
        SL(h, r + 2, 2)
        SL(h, r + 3, 3)
        SL(h, r + 4, 4)
        SL(h, r + 5, 5)
        SL(h, r + 6, 6)


def bufferXORInsertBackwards(buf, data, x, y, bufferOffsetX=0, bufferOffsetY=0):
    for i in range(x):
        for j in range(x):
            m = i + bufferOffsetX
            n = bufferOffsetY + y - 1 - j
            buf[m][n] = buf[m][n] ^ data[i * 4 + j]


def jh_update(ctx, msg, msg_len=None):
    buf = ctx['buffer']
    buf_len = len(buf)
    ptr = ctx['ptr']
    if msg_len is None:
        msg_len = len(msg)
    if msg_len < buf_len - ptr:
        op.buffer_insert(buf, ptr, msg, msg_len)
        ptr += msg_len
        ctx['ptr'] = ptr
        return

    V = [None] * JH_HX
    for i in range(JH_HX):
        V[i] = [None] * JH_HY

    READ_STATE(V, ctx['state'])
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
            bufferXORInsertBackwards(V, buf32, 4, 4)
            E8(V)
            bufferXORInsertBackwards(V, buf32, 4, 4, 4, 0)
            blockCountLow = ctx['blockCountLow']
            blockCountLow = op.t32(blockCountLow + 1)
            ctx['blockCountLow'] = blockCountLow 
            if blockCountLow == 0:
                ctx['blockCountHigh'] += 1
            ptr = 0
    WRITE_STATE(V, ctx['state'])
    ctx['ptr'] = ptr


def jh_close(ctx):
    buf = bytearray(128)
    l = [None] * 4
    buf[0] = 0x80
    ptr = ctx['ptr']
    if ptr is 0:
        numz = 47
    else:
        numz = 111 - ptr
    buf[1:1+numz] = [0] * numz
    blockCountLow = ctx['blockCountLow']
    blockCountHigh = ctx['blockCountHigh']
    l[0] = op.t32(blockCountLow << 9) + (ptr << 3)
    l[1] = op.t32(blockCountLow >> 23) + op.t32(blockCountHigh << 9)
    l[2] = op.t32(blockCountHigh >> 23)
    l[3] = 0
    lBytes = op.bytes_from_i32_list(op.swap32_list(l))
    op.buffer_insert(buf, 1 + numz, lBytes[::-1], 16)
    jh_update(ctx, buf, numz + 17)
    out = [None] * 16
    state = ctx['state']
    for u in range(16):
        out[u] = op.swap32(state[u + 16])
    return out


def pack_state(state):
    res = b''
    for i in state:
        res += pack('>I', i)
    return res


def jh(msg):
    ctx = {}
    ctx['state'] = op.swap32_list(IV512)
    ctx['ptr'] = 0
    ctx['buffer'] = bytearray(Jh_BlockSize)
    ctx['blockCountHigh'] = 0
    ctx['blockCountLow'] = 0
    jh_update(ctx, msg)
    res = jh_close(ctx)
    res = pack_state(res)
    pprint(res.hex())
