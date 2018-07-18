# -*- coding: utf-8 -*-

from . import op
from . import aes


IV512 = [
    0x72FCCDD8, 0x79CA4727, 0x128A077B, 0x40D55AEC,
    0xD1901A06, 0x430AE307, 0xB29F5CD1, 0xDF07FBFC,
    0x8E45D73D, 0x681AB538, 0xBDE86578, 0xDD577E47,
    0xE275EADE, 0x502D9FCD, 0xB9357178, 0x022A4B9A,
]


def AES_ROUND_NOKEY(x):
    t = [None] * 4
    op.buffer_insert(t, 0, x, 4)
    aes.AES_ROUND_NOKEY_LE(t, x)
    return x


def KEY_EXPAND_ELT(k, start, end):
    kt = k[start:end]
    l = AES_ROUND_NOKEY([kt[1], kt[2], kt[3], kt[0]])
    op.buffer_insert(k, start, l, end-start)


def c512(ctx, msg):
    m = op.bytes_to_i32_list(msg)
    p = [None] * 16
    x = [None] * 4
    rk = [None] * 32

    h = ctx['h']
    count = ctx['count']
    op.buffer_insert(p, 0, h, 16)
    # round 0
    rk[0] = op.swap32(m[0])
    x[0] = p[4] ^ rk[0]
    rk[1] = op.swap32(m[1])
    x[1] = p[5] ^ rk[1]
    rk[2] = op.swap32(m[2])
    x[2] = p[6] ^ rk[2]
    rk[3] = op.swap32(m[3])
    x[3] = p[7] ^ rk[3]
    AES_ROUND_NOKEY(x)
    rk[4] = op.swap32(m[4])
    x[0] ^= rk[4]
    rk[5] = op.swap32(m[5])
    x[1] ^= rk[5]
    rk[6] = op.swap32(m[6])
    x[2] ^= rk[6]
    rk[7] = op.swap32(m[7])
    x[3] ^= rk[7]
    AES_ROUND_NOKEY(x)
    rk[8] = op.swap32(m[8])
    x[0] ^= rk[8]
    rk[9] = op.swap32(m[9])
    x[1] ^= rk[9]
    rk[10] = op.swap32(m[10])
    x[2] ^= rk[10]
    rk[11] = op.swap32(m[11])
    x[3] ^= rk[11]
    AES_ROUND_NOKEY(x)
    rk[12] = op.swap32(m[12])
    x[0] ^= rk[12]
    rk[13] = op.swap32(m[13])
    x[1] ^= rk[13]
    rk[14] = op.swap32(m[14])
    x[2] ^= rk[14]
    rk[15] = op.swap32(m[15])
    x[3] ^= rk[15]
    AES_ROUND_NOKEY(x)
    p[0] ^= x[0]
    p[1] ^= x[1]
    p[2] ^= x[2]
    p[3] ^= x[3]
    rk[16] = op.swap32(m[16])
    x[0] = p[12] ^ rk[16]
    rk[17] = op.swap32(m[17])
    x[1] = p[13] ^ rk[17]
    rk[18] = op.swap32(m[18])
    x[2] = p[14] ^ rk[18]
    rk[19] = op.swap32(m[19])
    x[3] = p[15] ^ rk[19]
    AES_ROUND_NOKEY(x)
    rk[20] = op.swap32(m[20])
    x[0] ^= rk[20]
    rk[21] = op.swap32(m[21])
    x[1] ^= rk[21]
    rk[22] = op.swap32(m[22])
    x[2] ^= rk[22]
    rk[23] = op.swap32(m[23])
    x[3] ^= rk[23]
    AES_ROUND_NOKEY(x)
    rk[24] = op.swap32(m[24])
    x[0] ^= rk[24]
    rk[25] = op.swap32(m[25])
    x[1] ^= rk[25]
    rk[26] = op.swap32(m[26])
    x[2] ^= rk[26]
    rk[27] = op.swap32(m[27])
    x[3] ^= rk[27]
    AES_ROUND_NOKEY(x)
    rk[28] = op.swap32(m[28])
    x[0] ^= rk[28]
    rk[29] = op.swap32(m[29])
    x[1] ^= rk[29]
    rk[30] = op.swap32(m[30])
    x[2] ^= rk[30]
    rk[31] = op.swap32(m[31])
    x[3] ^= rk[31]
    AES_ROUND_NOKEY(x)
    p[8] ^= x[0]
    p[9] ^= x[1]
    p[10] ^= x[2]
    p[11] ^= x[3]

    for r in range(3):
        # round 1, 5, 9
        KEY_EXPAND_ELT(rk, 0, 4)
        rk[0] ^= rk[28]
        rk[1] ^= rk[29]
        rk[2] ^= rk[30]
        rk[3] ^= rk[31]
        if r == 0:
            rk[0] ^= count[0]
            rk[1] ^= count[1]
            rk[2] ^= count[2]
            rk[3] ^= op.t32(~count[3])

        x[0] = p[0] ^ rk[0]
        x[1] = p[1] ^ rk[1]
        x[2] = p[2] ^ rk[2]
        x[3] = p[3] ^ rk[3]
        AES_ROUND_NOKEY(x)
        KEY_EXPAND_ELT(rk, 4, 8)
        rk[4] ^= rk[0]
        rk[5] ^= rk[1]
        rk[6] ^= rk[2]
        rk[7] ^= rk[3]
        if r == 1:
            rk[4] ^= count[3]
            rk[5] ^= count[2]
            rk[6] ^= count[1]
            rk[7] ^= op.t32(~count[0])

        x[0] ^= rk[4]
        x[1] ^= rk[5]
        x[2] ^= rk[6]
        x[3] ^= rk[7]
        AES_ROUND_NOKEY(x)
        KEY_EXPAND_ELT(rk, 8, 12)
        rk[8] ^= rk[4]
        rk[9] ^= rk[5]
        rk[10] ^= rk[6]
        rk[11] ^= rk[7]
        x[0] ^= rk[8]
        x[1] ^= rk[9]
        x[2] ^= rk[10]
        x[3] ^= rk[11]
        AES_ROUND_NOKEY(x)
        KEY_EXPAND_ELT(rk, 12, 16)
        rk[12] ^= rk[8]
        rk[13] ^= rk[9]
        rk[14] ^= rk[10]
        rk[15] ^= rk[11]
        x[0] ^= rk[12]
        x[1] ^= rk[13]
        x[2] ^= rk[14]
        x[3] ^= rk[15]
        AES_ROUND_NOKEY(x)
        p[12] ^= x[0]
        p[13] ^= x[1]
        p[14] ^= x[2]
        p[15] ^= x[3]
        KEY_EXPAND_ELT(rk, 16, 20)
        rk[16] ^= rk[12]
        rk[17] ^= rk[13]
        rk[18] ^= rk[14]
        rk[19] ^= rk[15]
        x[0] = p[8] ^ rk[16]
        x[1] = p[9] ^ rk[17]
        x[2] = p[10] ^ rk[18]
        x[3] = p[11] ^ rk[19]
        AES_ROUND_NOKEY(x)
        KEY_EXPAND_ELT(rk, 20, 24)
        rk[20] ^= rk[16]
        rk[21] ^= rk[17]
        rk[22] ^= rk[18]
        rk[23] ^= rk[19]
        x[0] ^= rk[20]
        x[1] ^= rk[21]
        x[2] ^= rk[22]
        x[3] ^= rk[23]
        AES_ROUND_NOKEY(x)
        KEY_EXPAND_ELT(rk, 24, 28)
        rk[24] ^= rk[20]
        rk[25] ^= rk[21]
        rk[26] ^= rk[22]
        rk[27] ^= rk[23]
        x[0] ^= rk[24]
        x[1] ^= rk[25]
        x[2] ^= rk[26]
        x[3] ^= rk[27]
        AES_ROUND_NOKEY(x)
        KEY_EXPAND_ELT(rk, 28, 32)
        rk[28] ^= rk[24]
        rk[29] ^= rk[25]
        rk[30] ^= rk[26]
        rk[31] ^= rk[27]
        if r == 2:
            rk[28] ^= count[2]
            rk[29] ^= count[3]
            rk[30] ^= count[0]
            rk[31] ^= op.t32(~count[1])

        x[0] ^= rk[28]
        x[1] ^= rk[29]
        x[2] ^= rk[30]
        x[3] ^= rk[31]
        AES_ROUND_NOKEY(x)
        p[4] ^= x[0]
        p[5] ^= x[1]
        p[6] ^= x[2]
        p[7] ^= x[3]
        # round 2, 6, 10
        rk[0] ^= rk[25]
        x[0] = p[12] ^ rk[0]
        rk[1] ^= rk[26]
        x[1] = p[13] ^ rk[1]
        rk[2] ^= rk[27]
        x[2] = p[14] ^ rk[2]
        rk[3] ^= rk[28]
        x[3] = p[15] ^ rk[3]
        AES_ROUND_NOKEY(x)
        rk[4] ^= rk[29]
        x[0] ^= rk[4]
        rk[5] ^= rk[30]
        x[1] ^= rk[5]
        rk[6] ^= rk[31]
        x[2] ^= rk[6]
        rk[7] ^= rk[0]
        x[3] ^= rk[7]
        AES_ROUND_NOKEY(x)
        rk[8] ^= rk[1]
        x[0] ^= rk[8]
        rk[9] ^= rk[2]
        x[1] ^= rk[9]
        rk[10] ^= rk[3]
        x[2] ^= rk[10]
        rk[11] ^= rk[4]
        x[3] ^= rk[11]
        AES_ROUND_NOKEY(x)
        rk[12] ^= rk[5]
        x[0] ^= rk[12]
        rk[13] ^= rk[6]
        x[1] ^= rk[13]
        rk[14] ^= rk[7]
        x[2] ^= rk[14]
        rk[15] ^= rk[8]
        x[3] ^= rk[15]
        AES_ROUND_NOKEY(x)
        p[8] ^= x[0]
        p[9] ^= x[1]
        p[10] ^= x[2]
        p[11] ^= x[3]
        rk[16] ^= rk[9]
        x[0] = p[4] ^ rk[16]
        rk[17] ^= rk[10]
        x[1] = p[5] ^ rk[17]
        rk[18] ^= rk[11]
        x[2] = p[6] ^ rk[18]
        rk[19] ^= rk[12]
        x[3] = p[7] ^ rk[19]
        AES_ROUND_NOKEY(x)
        rk[20] ^= rk[13]
        x[0] ^= rk[20]
        rk[21] ^= rk[14]
        x[1] ^= rk[21]
        rk[22] ^= rk[15]
        x[2] ^= rk[22]
        rk[23] ^= rk[16]
        x[3] ^= rk[23]
        AES_ROUND_NOKEY(x)
        rk[24] ^= rk[17]
        x[0] ^= rk[24]
        rk[25] ^= rk[18]
        x[1] ^= rk[25]
        rk[26] ^= rk[19]
        x[2] ^= rk[26]
        rk[27] ^= rk[20]
        x[3] ^= rk[27]
        AES_ROUND_NOKEY(x)
        rk[28] ^= rk[21]
        x[0] ^= rk[28]
        rk[29] ^= rk[22]
        x[1] ^= rk[29]
        rk[30] ^= rk[23]
        x[2] ^= rk[30]
        rk[31] ^= rk[24]
        x[3] ^= rk[31]
        AES_ROUND_NOKEY(x)
        p[0] ^= x[0]
        p[1] ^= x[1]
        p[2] ^= x[2]
        p[3] ^= x[3]
        # round 3, 7, 11
        KEY_EXPAND_ELT(rk, 0, 4)
        rk[0] ^= rk[28]
        rk[1] ^= rk[29]
        rk[2] ^= rk[30]
        rk[3] ^= rk[31]
        x[0] = p[8] ^ rk[0]
        x[1] = p[9] ^ rk[1]
        x[2] = p[10] ^ rk[2]
        x[3] = p[11] ^ rk[3]
        AES_ROUND_NOKEY(x)
        KEY_EXPAND_ELT(rk, 4, 8)
        rk[4] ^= rk[0]
        rk[5] ^= rk[1]
        rk[6] ^= rk[2]
        rk[7] ^= rk[3]
        x[0] ^= rk[4]
        x[1] ^= rk[5]
        x[2] ^= rk[6]
        x[3] ^= rk[7]
        AES_ROUND_NOKEY(x)
        KEY_EXPAND_ELT(rk, 8, 12)
        rk[8] ^= rk[4]
        rk[9] ^= rk[5]
        rk[10] ^= rk[6]
        rk[11] ^= rk[7]
        x[0] ^= rk[8]
        x[1] ^= rk[9]
        x[2] ^= rk[10]
        x[3] ^= rk[11]
        AES_ROUND_NOKEY(x)
        KEY_EXPAND_ELT(rk, 12, 16)
        rk[12] ^= rk[8]
        rk[13] ^= rk[9]
        rk[14] ^= rk[10]
        rk[15] ^= rk[11]
        x[0] ^= rk[12]
        x[1] ^= rk[13]
        x[2] ^= rk[14]
        x[3] ^= rk[15]
        AES_ROUND_NOKEY(x)
        p[4] ^= x[0]
        p[5] ^= x[1]
        p[6] ^= x[2]
        p[7] ^= x[3]
        KEY_EXPAND_ELT(rk, 16, 20)
        rk[16] ^= rk[12]
        rk[17] ^= rk[13]
        rk[18] ^= rk[14]
        rk[19] ^= rk[15]
        x[0] = p[0] ^ rk[16]
        x[1] = p[1] ^ rk[17]
        x[2] = p[2] ^ rk[18]
        x[3] = p[3] ^ rk[19]
        AES_ROUND_NOKEY(x)
        KEY_EXPAND_ELT(rk, 20, 24)
        rk[20] ^= rk[16]
        rk[21] ^= rk[17]
        rk[22] ^= rk[18]
        rk[23] ^= rk[19]
        x[0] ^= rk[20]
        x[1] ^= rk[21]
        x[2] ^= rk[22]
        x[3] ^= rk[23]
        AES_ROUND_NOKEY(x)
        KEY_EXPAND_ELT(rk, 24, 28)
        rk[24] ^= rk[20]
        rk[25] ^= rk[21]
        rk[26] ^= rk[22]
        rk[27] ^= rk[23]
        x[0] ^= rk[24]
        x[1] ^= rk[25]
        x[2] ^= rk[26]
        x[3] ^= rk[27]
        AES_ROUND_NOKEY(x)
        KEY_EXPAND_ELT(rk, 28, 32)
        rk[28] ^= rk[24]
        rk[29] ^= rk[25]
        rk[30] ^= rk[26]
        rk[31] ^= rk[27]
        x[0] ^= rk[28]
        x[1] ^= rk[29]
        x[2] ^= rk[30]
        x[3] ^= rk[31]
        AES_ROUND_NOKEY(x)
        p[12] ^= x[0]
        p[13] ^= x[1]
        p[14] ^= x[2]
        p[15] ^= x[3]
        # round 4, 8, 12
        rk[0] ^= rk[25]
        x[0] = p[4] ^ rk[0]
        rk[1] ^= rk[26]
        x[1] = p[5] ^ rk[1]
        rk[2] ^= rk[27]
        x[2] = p[6] ^ rk[2]
        rk[3] ^= rk[28]
        x[3] = p[7] ^ rk[3]
        AES_ROUND_NOKEY(x)
        rk[4] ^= rk[29]
        x[0] ^= rk[4]
        rk[5] ^= rk[30]
        x[1] ^= rk[5]
        rk[6] ^= rk[31]
        x[2] ^= rk[6]
        rk[7] ^= rk[0]
        x[3] ^= rk[7]
        AES_ROUND_NOKEY(x)
        rk[8] ^= rk[1]
        x[0] ^= rk[8]
        rk[9] ^= rk[2]
        x[1] ^= rk[9]
        rk[10] ^= rk[3]
        x[2] ^= rk[10]
        rk[11] ^= rk[4]
        x[3] ^= rk[11]
        AES_ROUND_NOKEY(x)
        rk[12] ^= rk[5]
        x[0] ^= rk[12]
        rk[13] ^= rk[6]
        x[1] ^= rk[13]
        rk[14] ^= rk[7]
        x[2] ^= rk[14]
        rk[15] ^= rk[8]
        x[3] ^= rk[15]
        AES_ROUND_NOKEY(x)
        p[0] ^= x[0]
        p[1] ^= x[1]
        p[2] ^= x[2]
        p[3] ^= x[3]
        rk[16] ^= rk[9]
        x[0] = p[12] ^ rk[16]
        rk[17] ^= rk[10]
        x[1] = p[13] ^ rk[17]
        rk[18] ^= rk[11]
        x[2] = p[14] ^ rk[18]
        rk[19] ^= rk[12]
        x[3] = p[15] ^ rk[19]
        AES_ROUND_NOKEY(x)
        rk[20] ^= rk[13]
        x[0] ^= rk[20]
        rk[21] ^= rk[14]
        x[1] ^= rk[21]
        rk[22] ^= rk[15]
        x[2] ^= rk[22]
        rk[23] ^= rk[16]
        x[3] ^= rk[23]
        AES_ROUND_NOKEY(x)
        rk[24] ^= rk[17]
        x[0] ^= rk[24]
        rk[25] ^= rk[18]
        x[1] ^= rk[25]
        rk[26] ^= rk[19]
        x[2] ^= rk[26]
        rk[27] ^= rk[20]
        x[3] ^= rk[27]
        AES_ROUND_NOKEY(x)
        rk[28] ^= rk[21]
        x[0] ^= rk[28]
        rk[29] ^= rk[22]
        x[1] ^= rk[29]
        rk[30] ^= rk[23]
        x[2] ^= rk[30]
        rk[31] ^= rk[24]
        x[3] ^= rk[31]
        AES_ROUND_NOKEY(x)
        p[8] ^= x[0]
        p[9] ^= x[1]
        p[10] ^= x[2]
        p[11] ^= x[3]

    # round 13
    KEY_EXPAND_ELT(rk, 0, 4)
    rk[0] ^= rk[28]
    rk[1] ^= rk[29]
    rk[2] ^= rk[30]
    rk[3] ^= rk[31]
    x[0] = p[0] ^ rk[0]
    x[1] = p[1] ^ rk[1]
    x[2] = p[2] ^ rk[2]
    x[3] = p[3] ^ rk[3]
    AES_ROUND_NOKEY(x)
    KEY_EXPAND_ELT(rk, 4, 8)
    rk[4] ^= rk[0]
    rk[5] ^= rk[1]
    rk[6] ^= rk[2]
    rk[7] ^= rk[3]
    x[0] ^= rk[4]
    x[1] ^= rk[5]
    x[2] ^= rk[6]
    x[3] ^= rk[7]
    AES_ROUND_NOKEY(x)
    KEY_EXPAND_ELT(rk, 8, 12)
    rk[8] ^= rk[4]
    rk[9] ^= rk[5]
    rk[10] ^= rk[6]
    rk[11] ^= rk[7]
    x[0] ^= rk[8]
    x[1] ^= rk[9]
    x[2] ^= rk[10]
    x[3] ^= rk[11]
    AES_ROUND_NOKEY(x)
    KEY_EXPAND_ELT(rk, 12, 16)
    rk[12] ^= rk[8]
    rk[13] ^= rk[9]
    rk[14] ^= rk[10]
    rk[15] ^= rk[11]
    x[0] ^= rk[12]
    x[1] ^= rk[13]
    x[2] ^= rk[14]
    x[3] ^= rk[15]
    AES_ROUND_NOKEY(x)
    p[12] ^= x[0]
    p[13] ^= x[1]
    p[14] ^= x[2]
    p[15] ^= x[3]
    KEY_EXPAND_ELT(rk, 16, 20)
    rk[16] ^= rk[12]
    rk[17] ^= rk[13]
    rk[18] ^= rk[14]
    rk[19] ^= rk[15]
    x[0] = p[8] ^ rk[16]
    x[1] = p[9] ^ rk[17]
    x[2] = p[10] ^ rk[18]
    x[3] = p[11] ^ rk[19]
    AES_ROUND_NOKEY(x)
    KEY_EXPAND_ELT(rk, 20, 24)
    rk[20] ^= rk[16]
    rk[21] ^= rk[17]
    rk[22] ^= rk[18]
    rk[23] ^= rk[19]
    x[0] ^= rk[20]
    x[1] ^= rk[21]
    x[2] ^= rk[22]
    x[3] ^= rk[23]
    AES_ROUND_NOKEY(x)
    KEY_EXPAND_ELT(rk, 24, 28)
    rk[24] ^= rk[20] ^ count[1]
    rk[25] ^= rk[21] ^ count[0]
    rk[26] ^= rk[22] ^ count[3]
    rk[27] ^= rk[23] ^ op.t32(~count[2])
    x[0] ^= rk[24]
    x[1] ^= rk[25]
    x[2] ^= rk[26]
    x[3] ^= rk[27]
    AES_ROUND_NOKEY(x)
    KEY_EXPAND_ELT(rk, 28, 32)
    rk[28] ^= rk[24]
    rk[29] ^= rk[25]
    rk[30] ^= rk[26]
    rk[31] ^= rk[27]
    x[0] ^= rk[28]
    x[1] ^= rk[29]
    x[2] ^= rk[30]
    x[3] ^= rk[31]
    AES_ROUND_NOKEY(x)
    p[4] ^= x[0]
    p[5] ^= x[1]
    p[6] ^= x[2]
    p[7] ^= x[3]
    h[0] ^= p[8]
    h[1] ^= p[9]
    h[2] ^= p[10]
    h[3] ^= p[11]
    h[4] ^= p[12]
    h[5] ^= p[13]
    h[6] ^= p[14]
    h[7] ^= p[15]
    h[8] ^= p[0]
    h[9] ^= p[1]
    h[10] ^= p[2]
    h[11] ^= p[3]
    h[12] ^= p[4]
    h[13] ^= p[5]
    h[14] ^= p[6]
    h[15] ^= p[7]

    ctx['h'] = h
    ctx['count'] = count


def shavite_update(ctx, msg):
    buf = ctx['buffer']
    ptr = ctx['ptr']
    msg_len = len(msg)
    buf_len = len(buf)
    while msg_len > 0:
        clen = buf_len - ptr
        if clen > msg_len:
            clen = msg_len
        op.buffer_insert(buf, ptr, msg, clen)
        ptr += clen
        msg = msg[clen:]
        msg_len -= clen
        if ptr is buf_len:
            count = ctx['count']
            count[0] = op.t32(count[0] + 1024)
            if count[0] == 0:
                count[1] = op.t32(count[1] + 1)
                if count[1] == 0:
                    count[2] = op.t32(count[2] + 1)
                    if count[2] == 0:
                        count[3] = op.t32(count[3] + 1)



            ctx['count'] = count
            c512(ctx, buf)
            ptr = 0
    ctx['ptr'] = ptr


def shavite_close(ctx, ub, n):
    count = [None] * 4

    buf = ctx['buffer']
    ptr = ctx['ptr']

    ctx['count'][0] += (ptr << 3) + n
    count[0] = ctx['count'][0]
    count[1] = ctx['count'][1]
    count[2] = ctx['count'][2]
    count[3] = ctx['count'][3]
    z = 0x80 >> n
    z = ((ub & -z) | z) & 0xFF
    if ptr == 0 and n == 0:
        buf[0] = 0x80
        buf[1:110] = [0] * 109
        ctx['count'] = [0] * 4
    elif ptr < 110:
        buf[ptr] = z
        ptr += 1
        set_len = 110 - ptr
        buf[ptr:ptr+set_len] = [0] * set_len
    else:
        buf[ptr] = z
        ptr += 1
        set_len = 128 - ptr
        buf[ptr:ptr+set_len] = [0] * set_len
        c512(ctx, buf)
        buf[:110] = [0] * 110
        ctx['count'] = [0] * 4

    countSwapped = op.swap32_list(count)
    countBytes = op.bytes_from_i32_list(countSwapped)
    op.buffer_insert(buf, 110, countBytes, 16)
    buf[126] = (16 << 5) & 0xFF  #just to copy the spec (doesn't make sense)
    buf[127] = op.rshift32b(16, 3)
    c512(ctx, buf)

    out = [None] * 16
    for u in range(16):
        out[u] = op.swap32(ctx['h'][u])
    return out


def shavite(msg, out_array=False, in_array=False):
    ctx = {}
    ctx['ptr'] = 0
    ctx['count'] = [0] * 4
    ctx['h'] = IV512[:]
    ctx['buffer'] = bytearray(128)
    if in_array:
        msg = op.bytes_from_i32_list(msg)
    shavite_update(ctx, msg)
    res = shavite_close(ctx, 0, 0)
    if not out_array:
        res = op.bytes_from_i32_list(res)
    return res
