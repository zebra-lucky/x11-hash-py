# -*- coding: utf-8 -*-

from . import op


V_INIT = [
    [
        0x6d251e69, 0x44b051e0, 0x4eaa6fb4, 0xdbf78465,
        0x6e292011, 0x90152df4, 0xee058139, 0xdef610bb,
    ],
    [
        0xc3b44b95, 0xd9d2f256, 0x70eee9a0, 0xde099fa3,
        0x5d9b0557, 0x8fc944b3, 0xcf1ccf0e, 0x746cd581,
    ],
    [
        0xf7efc89d, 0x5dba5781, 0x04016ce5, 0xad659c05,
        0x0306194f, 0x666d1836, 0x24aa230a, 0x8b264ae7,
    ],
    [
        0x858075d5, 0x36d79cce, 0xe571f7d7, 0x204b1f67,
        0x35870c6a, 0x57e9e923, 0x14bcb808, 0x7cde72ce,
    ],
    [
        0x6c68e9be, 0x5ec41e22, 0xc825b7c7, 0xaffb4363,
        0xf5df3999, 0x0fc688f1, 0xb07224cc, 0x03e86cea,
    ]
]


RC00 = [
    0x303994a6, 0xc0e65299, 0x6cc33a12, 0xdc56983e,
    0x1e00108f, 0x7800423d, 0x8f5b7882, 0x96e1db12,
]


RC04 = [
    0xe0337818, 0x441ba90d, 0x7f34d442, 0x9389217f,
    0xe5a8bce6, 0x5274baf4, 0x26889ba7, 0x9a226e9d,
]


RC10 = [
    0xb6de10ed, 0x70f47aae, 0x0707a3d4, 0x1c1e8f51,
    0x707a3d45, 0xaeb28562, 0xbaca1589, 0x40a46f3e,
]


RC14 = [
    0x01685f3d, 0x05a17cf4, 0xbd09caca, 0xf4272b28,
    0x144ae5cc, 0xfaa7ae2b, 0x2e48f1c1, 0xb923c704,
]


RC20 = [
    0xfc20d9d2, 0x34552e25, 0x7ad8818f, 0x8438764a,
    0xbb6de032, 0xedb780c8, 0xd9847356, 0xa2c78434,
]


RC24 = [
    0xe25e72c1, 0xe623bb72, 0x5c58a4a4, 0x1e38e2e7,
    0x78e38b9d, 0x27586719, 0x36eda57f, 0x703aace7,
]


RC30 = [
    0xb213afa5, 0xc84ebe95, 0x4e608a22, 0x56d858fe,
    0x343b138f, 0xd0ec4e3d, 0x2ceb4882, 0xb3ad2208,
]


RC34 = [
    0xe028c9bf, 0x44756f91, 0x7e8fce32, 0x956548be,
    0xfe191be2, 0x3cb226e5, 0x5944a28e, 0xa1c4c355,
]


RC40 = [
    0xf0d2e9e3, 0xac11d7fa, 0x1bcb66f2, 0x6f2d9bc9,
    0x78602649, 0x8edae952, 0x3b6ba548, 0xedae9520,
]


RC44 = [
    0x5090d577, 0x2d1925ab, 0xb46496ac, 0xd1925ab0,
    0x29131ab6, 0x0fc053c3, 0x3f014f0c, 0xfc053c31,
]


def M2(d, s):
    tmp = s[7]
    d[7] = s[6]
    d[6] = s[5]
    d[5] = s[4]
    d[4] = s[3] ^ tmp
    d[3] = s[2] ^ tmp
    d[2] = s[1]
    d[1] = s[0] ^ tmp
    d[0] = tmp


# V is a table of states
def MI5(buf, V):
    M = [None]*8
    a = [None]*8
    b = [None]*8
    M[0] = buf[0]
    M[1] = buf[1]
    M[2] = buf[2]
    M[3] = buf[3]
    M[4] = buf[4]
    M[5] = buf[5]
    M[6] = buf[6]
    M[7] = buf[7]
    op.xor_table(a, V[0], V[1], 8)
    op.xor_table(b, V[2], V[3], 8)
    op.xor_table(a, a, b, 8)
    op.xor_table(a, a, V[4], 8)
    M2(a, a)
    op.xor_table(V[0], a, V[0], 8)
    op.xor_table(V[1], a, V[1], 8)
    op.xor_table(V[2], a, V[2], 8)
    op.xor_table(V[3], a, V[3], 8)
    op.xor_table(V[4], a, V[4], 8)
    M2(b, V[0])
    op.xor_table(b, b, V[1], 8)
    M2(V[1], V[1])
    op.xor_table(V[1], V[1], V[2], 8)
    M2(V[2], V[2])
    op.xor_table(V[2], V[2], V[3], 8)
    M2(V[3], V[3])
    op.xor_table(V[3], V[3], V[4], 8)
    M2(V[4], V[4])
    op.xor_table(V[4], V[4], V[0], 8)
    M2(V[0], b)
    op.xor_table(V[0], V[0], V[4], 8)
    M2(V[4], V[4])
    op.xor_table(V[4], V[4], V[3], 8)
    M2(V[3], V[3])
    op.xor_table(V[3], V[3], V[2], 8)
    M2(V[2], V[2])
    op.xor_table(V[2], V[2], V[1], 8)
    M2(V[1], V[1])
    op.xor_table(V[1], V[1], b, 8)
    op.xor_table(V[0], V[0], M, 8)
    M2(M, M)
    op.xor_table(V[1], V[1], M, 8)
    M2(M, M)
    op.xor_table(V[2], V[2], M, 8)
    M2(M, M)
    op.xor_table(V[3], V[3], M, 8)
    M2(M, M)
    op.xor_table(V[4], V[4], M, 8)


def TWEAK5(V):
    V[1][4] = op.rotl32(V[1][4], 1)
    V[1][5] = op.rotl32(V[1][5], 1)
    V[1][6] = op.rotl32(V[1][6], 1)
    V[1][7] = op.rotl32(V[1][7], 1)
    V[2][4] = op.rotl32(V[2][4], 2)
    V[2][5] = op.rotl32(V[2][5], 2)
    V[2][6] = op.rotl32(V[2][6], 2)
    V[2][7] = op.rotl32(V[2][7], 2)
    V[3][4] = op.rotl32(V[3][4], 3)
    V[3][5] = op.rotl32(V[3][5], 3)
    V[3][6] = op.rotl32(V[3][6], 3)
    V[3][7] = op.rotl32(V[3][7], 3)
    V[4][4] = op.rotl32(V[4][4], 4)
    V[4][5] = op.rotl32(V[4][5], 4)
    V[4][6] = op.rotl32(V[4][6], 4)
    V[4][7] = op.rotl32(V[4][7], 4)


def SUB_CRUMB(a0, a1, a2, a3):
    tmp = (a0)
    (a0) |= (a1)
    (a2) ^= (a3)
    (a1) = op.t32(~(a1))
    (a0) ^= (a3)
    (a3) &= tmp
    (a1) ^= (a3)
    (a3) ^= (a2)
    (a2) &= (a0)
    (a0) = op.t32(~(a0))
    (a2) ^= (a1)
    (a1) |= (a3)
    tmp ^= (a1)
    (a3) ^= (a2)
    (a2) &= (a1)
    (a1) ^= (a0)
    (a0) = tmp
    return [a0, a1, a2, a3]


def MIX_WORD(u, v):
    (v) ^= (u)
    (u) = op.rotl32((u), 2) ^ (v)
    (v) = op.rotl32((v), 14) ^ (u)
    (u) = op.rotl32((u), 10) ^ (v)
    (v) = op.rotl32((v), 1)
    return [u,v]


def P5(V):
    TWEAK5(V)
    for r in range(8):
        tmp = SUB_CRUMB(V[0][0], V[0][1], V[0][2], V[0][3])
        V[0][0] = tmp[0]
        V[0][1] = tmp[1]
        V[0][2] = tmp[2]
        V[0][3] = tmp[3]
        tmp = SUB_CRUMB(V[0][5], V[0][6], V[0][7], V[0][4])
        V[0][5] = tmp[0]
        V[0][6] = tmp[1]
        V[0][7] = tmp[2]
        V[0][4] = tmp[3]
        tmp = MIX_WORD(V[0][0], V[0][4])
        V[0][0] = tmp[0]
        V[0][4] = tmp[1]
        tmp = MIX_WORD(V[0][1], V[0][5])
        V[0][1] = tmp[0]
        V[0][5] = tmp[1]
        tmp = MIX_WORD(V[0][2], V[0][6])
        V[0][2] = tmp[0]
        V[0][6] = tmp[1]
        tmp = MIX_WORD(V[0][3], V[0][7])
        V[0][3] = tmp[0]
        V[0][7] = tmp[1]
        V[0][0] ^= RC00[r]
        V[0][4] ^= RC04[r]

    for r in range(8):
        tmp = SUB_CRUMB(V[1][0], V[1][1], V[1][2], V[1][3])
        V[1][0] = tmp[0]
        V[1][1] = tmp[1]
        V[1][2] = tmp[2]
        V[1][3] = tmp[3]
        tmp = SUB_CRUMB(V[1][5], V[1][6], V[1][7], V[1][4])
        V[1][5] = tmp[0]
        V[1][6] = tmp[1]
        V[1][7] = tmp[2]
        V[1][4] = tmp[3]
        tmp = MIX_WORD(V[1][0], V[1][4])
        V[1][0] = tmp[0]
        V[1][4] = tmp[1]
        tmp = MIX_WORD(V[1][1], V[1][5])
        V[1][1] = tmp[0]
        V[1][5] = tmp[1]
        tmp = MIX_WORD(V[1][2], V[1][6])
        V[1][2] = tmp[0]
        V[1][6] = tmp[1]
        tmp = MIX_WORD(V[1][3], V[1][7])
        V[1][3] = tmp[0]
        V[1][7] = tmp[1]
        V[1][0] ^= RC10[r]
        V[1][4] ^= RC14[r]

    for r in range(8):
        tmp = SUB_CRUMB(V[2][0], V[2][1], V[2][2], V[2][3])
        V[2][0] = tmp[0]
        V[2][1] = tmp[1]
        V[2][2] = tmp[2]
        V[2][3] = tmp[3]
        tmp = SUB_CRUMB(V[2][5], V[2][6], V[2][7], V[2][4])
        V[2][5] = tmp[0]
        V[2][6] = tmp[1]
        V[2][7] = tmp[2]
        V[2][4] = tmp[3]
        tmp = MIX_WORD(V[2][0], V[2][4])
        V[2][0] = tmp[0]
        V[2][4] = tmp[1]
        tmp = MIX_WORD(V[2][1], V[2][5])
        V[2][1] = tmp[0]
        V[2][5] = tmp[1]
        tmp = MIX_WORD(V[2][2], V[2][6])
        V[2][2] = tmp[0]
        V[2][6] = tmp[1]
        tmp = MIX_WORD(V[2][3], V[2][7])
        V[2][3] = tmp[0]
        V[2][7] = tmp[1]
        V[2][0] ^= RC20[r]
        V[2][4] ^= RC24[r]

    for r in range(8):
        tmp = SUB_CRUMB(V[3][0], V[3][1], V[3][2], V[3][3])
        V[3][0] = tmp[0]
        V[3][1] = tmp[1]
        V[3][2] = tmp[2]
        V[3][3] = tmp[3]
        tmp = SUB_CRUMB(V[3][5], V[3][6], V[3][7], V[3][4])
        V[3][5] = tmp[0]
        V[3][6] = tmp[1]
        V[3][7] = tmp[2]
        V[3][4] = tmp[3]
        tmp = MIX_WORD(V[3][0], V[3][4])
        V[3][0] = tmp[0]
        V[3][4] = tmp[1]
        tmp = MIX_WORD(V[3][1], V[3][5])
        V[3][1] = tmp[0]
        V[3][5] = tmp[1]
        tmp = MIX_WORD(V[3][2], V[3][6])
        V[3][2] = tmp[0]
        V[3][6] = tmp[1]
        tmp = MIX_WORD(V[3][3], V[3][7])
        V[3][3] = tmp[0]
        V[3][7] = tmp[1]
        V[3][0] ^= RC30[r]
        V[3][4] ^= RC34[r]

    for r in range(8):
        tmp = SUB_CRUMB(V[4][0], V[4][1], V[4][2], V[4][3])
        V[4][0] = tmp[0]
        V[4][1] = tmp[1]
        V[4][2] = tmp[2]
        V[4][3] = tmp[3]
        tmp = SUB_CRUMB(V[4][5], V[4][6], V[4][7], V[4][4])
        V[4][5] = tmp[0]
        V[4][6] = tmp[1]
        V[4][7] = tmp[2]
        V[4][4] = tmp[3]
        tmp = MIX_WORD(V[4][0], V[4][4])
        V[4][0] = tmp[0]
        V[4][4] = tmp[1]
        tmp = MIX_WORD(V[4][1], V[4][5])
        V[4][1] = tmp[0]
        V[4][5] = tmp[1]
        tmp = MIX_WORD(V[4][2], V[4][6])
        V[4][2] = tmp[0]
        V[4][6] = tmp[1]
        tmp = MIX_WORD(V[4][3], V[4][7])
        V[4][3] = tmp[0]
        V[4][7] = tmp[1]
        V[4][0] ^= RC40[r]
        V[4][4] ^= RC44[r]


def luffa5_update(ctx, msg):
    V = [None] * 5
    for i in range(5):
        V[i] = [None] * 8

    buf = ctx['buffer']
    ptr = ctx['ptr']
    buf_len = len(buf)
    msg_len = len(msg)
    if msg_len < buf_len - ptr:
        op.buffer_insert(buf, ptr, msg, msg_len)
        ptr += msg_len
        ctx['ptr'] = ptr
        return

    state = ctx['state']
    for i in range(5):
        for j in range(8):
            V[i][j] = state[i][j]

    while msg_len > 0:
        clen = buf_len - ptr
        if clen > msg_len:
            clen = msg_len
        op.buffer_insert(buf, ptr, msg, clen)
        ptr += clen
        msg = msg[clen:]
        msg_len -= clen
        if ptr == buf_len:
            buf32 = op.bytes_to_i32_list(buf)
            MI5(buf32, V)
            P5(V)
            ptr = 0

    ctx['state'] = V
    ctx['ptr'] = ptr


def luffa5_close(ctx, ub, n):
    V = [None] * 5
    for i in range(5):
        V[i] = [None] * 8

    buf = ctx['buffer']
    ptr = ctx['ptr']
    state = ctx['state']
    buf_len = len(buf)
    z = 0x80 >> n
    buf[ptr] = ((ub & -z) | z) & 0xFF
    ptr += 1
    set_len = buf_len - ptr
    buf[ptr:ptr+set_len] = [0] * set_len
    for i in range(5):
        for j in range(8):
            V[i][j] = state[i][j]


    out = [None] * 16
    for i in range(3):
        buf32 = op.bytes_to_i32_list(buf)
        MI5(buf32, V)
        P5(V)
        if i == 0:
            buf[:buf_len] = [0] * buf_len
        elif i == 1:
            out[0] = V[0][0] ^ V[1][0] ^ V[2][0] ^ V[3][0] ^ V[4][0]
            out[1] = V[0][1] ^ V[1][1] ^ V[2][1] ^ V[3][1] ^ V[4][1]
            out[2] = V[0][2] ^ V[1][2] ^ V[2][2] ^ V[3][2] ^ V[4][2]
            out[3] = V[0][3] ^ V[1][3] ^ V[2][3] ^ V[3][3] ^ V[4][3]
            out[4] = V[0][4] ^ V[1][4] ^ V[2][4] ^ V[3][4] ^ V[4][4]
            out[5] = V[0][5] ^ V[1][5] ^ V[2][5] ^ V[3][5] ^ V[4][5]
            out[6] = V[0][6] ^ V[1][6] ^ V[2][6] ^ V[3][6] ^ V[4][6]
            out[7] = V[0][7] ^ V[1][7] ^ V[2][7] ^ V[3][7] ^ V[4][7]
        elif i == 2:
            out[8] = V[0][0] ^ V[1][0] ^ V[2][0] ^ V[3][0] ^ V[4][0]
            out[9] = V[0][1] ^ V[1][1] ^ V[2][1] ^ V[3][1] ^ V[4][1]
            out[10] = V[0][2] ^ V[1][2] ^ V[2][2] ^ V[3][2] ^ V[4][2]
            out[11] = V[0][3] ^ V[1][3] ^ V[2][3] ^ V[3][3] ^ V[4][3]
            out[12] = V[0][4] ^ V[1][4] ^ V[2][4] ^ V[3][4] ^ V[4][4]
            out[13] = V[0][5] ^ V[1][5] ^ V[2][5] ^ V[3][5] ^ V[4][5]
            out[14] = V[0][6] ^ V[1][6] ^ V[2][6] ^ V[3][6] ^ V[4][6]
            out[15] = V[0][7] ^ V[1][7] ^ V[2][7] ^ V[3][7] ^ V[4][7]
    return out


def luffa5(msg, out_array=False, in_array=False):
    ctx = {}
    ctx['state'] = V_INIT
    ctx['ptr'] = 0
    ctx['buffer'] = bytearray(32)
    if in_array:
        msg = op.bytes_from_i32_list(msg)
    luffa5_update(ctx, msg)
    res = luffa5_close(ctx, 0, 0)
    if not out_array:
        res = op.bytes_from_i32_list(res)
    return res
