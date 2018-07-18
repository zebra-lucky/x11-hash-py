# -*- coding: utf-8 -*-

from struct import pack
from pprint import pprint

from . import op


IV512 = [
    0x0BA16B95, 0x72F999AD, 0x9FECC2AE, 0xBA3264FC,
    0x5E894929, 0x8E9F30E5, 0x2F1DAA37, 0xF0F2C558,
    0xAC506643, 0xA90635A5, 0xE25B878B, 0xAAB7878F,
    0x88817F7A, 0x0A02892B, 0x559A7550, 0x598F657E,
    0x7EEF60A1, 0x6B70E3E8, 0x9C1714D1, 0xB958E2A8,
    0xAB02675E, 0xED1C014F, 0xCD8D65BB, 0xFDB7A257,
    0x09254899, 0xD699C7BC, 0x9019B6DC, 0x2B9022E4,
    0x8FA14956, 0x21BF9BD3, 0xB94D0943, 0x6FFDDC22,
]


# The powers of 41 modulo 257. We use exponents from 0 to 255, inclusive.
alpha_tab = [
    1, 41, 139, 45, 46, 87, 226, 14, 60, 147, 116, 130,
    190, 80, 196, 69, 2, 82, 21, 90, 92, 174, 195, 28,
    120, 37, 232, 3, 123, 160, 135, 138, 4, 164, 42, 180,
    184, 91, 133, 56, 240, 74, 207, 6, 246, 63, 13, 19,
    8, 71, 84, 103, 111, 182, 9, 112, 223, 148, 157, 12,
    235, 126, 26, 38, 16, 142, 168, 206, 222, 107, 18, 224,
    189, 39, 57, 24, 213, 252, 52, 76, 32, 27, 79, 155,
    187, 214, 36, 191, 121, 78, 114, 48, 169, 247, 104, 152,
    64, 54, 158, 53, 117, 171, 72, 125, 242, 156, 228, 96,
    81, 237, 208, 47, 128, 108, 59, 106, 234, 85, 144, 250,
    227, 55, 199, 192, 162, 217, 159, 94, 256, 216, 118, 212,
    211, 170, 31, 243, 197, 110, 141, 127, 67, 177, 61, 188,
    255, 175, 236, 167, 165, 83, 62, 229, 137, 220, 25, 254,
    134, 97, 122, 119, 253, 93, 215, 77, 73, 166, 124, 201,
    17, 183, 50, 251, 11, 194, 244, 238, 249, 186, 173, 154,
    146, 75, 248, 145, 34, 109, 100, 245, 22, 131, 231, 219,
    241, 115, 89, 51, 35, 150, 239, 33, 68, 218, 200, 233,
    44, 5, 205, 181, 225, 230, 178, 102, 70, 43, 221, 66,
    136, 179, 143, 209, 88, 10, 153, 105, 193, 203, 99, 204,
    140, 86, 185, 132, 15, 101, 29, 161, 176, 20, 49, 210,
    129, 149, 198, 151, 23, 172, 113, 7, 30, 202, 58, 65,
    95, 40, 98, 163
]


# beta^(255*i) mod 257
yoff_b_n = [
    1, 163, 98, 40, 95, 65, 58, 202, 30, 7, 113, 172,
    23, 151, 198, 149, 129, 210, 49, 20, 176, 161, 29, 101,
    15, 132, 185, 86, 140, 204, 99, 203, 193, 105, 153, 10,
    88, 209, 143, 179, 136, 66, 221, 43, 70, 102, 178, 230,
    225, 181, 205, 5, 44, 233, 200, 218, 68, 33, 239, 150,
    35, 51, 89, 115, 241, 219, 231, 131, 22, 245, 100, 109,
    34, 145, 248, 75, 146, 154, 173, 186, 249, 238, 244, 194,
    11, 251, 50, 183, 17, 201, 124, 166, 73, 77, 215, 93,
    253, 119, 122, 97, 134, 254, 25, 220, 137, 229, 62, 83,
    165, 167, 236, 175, 255, 188, 61, 177, 67, 127, 141, 110,
    197, 243, 31, 170, 211, 212, 118, 216, 256, 94, 159, 217,
    162, 192, 199, 55, 227, 250, 144, 85, 234, 106, 59, 108,
    128, 47, 208, 237, 81, 96, 228, 156, 242, 125, 72, 171,
    117, 53, 158, 54, 64, 152, 104, 247, 169, 48, 114, 78,
    121, 191, 36, 214, 187, 155, 79, 27, 32, 76, 52, 252,
    213, 24, 57, 39, 189, 224, 18, 107, 222, 206, 168, 142,
    16, 38, 26, 126, 235, 12, 157, 148, 223, 112, 9, 182,
    111, 103, 84, 71, 8, 19, 13, 63, 246, 6, 207, 74,
    240, 56, 133, 91, 184, 180, 42, 164, 4, 138, 135, 160,
    123, 3, 232, 37, 120, 28, 195, 174, 92, 90, 21, 82,
    2, 69, 196, 80, 190, 130, 116, 147, 60, 14, 226, 87,
    46, 45, 139, 41
]


# beta^(255*i) + beta^(253*i) mod 257
yoff_b_f = [
    2, 203, 156, 47, 118, 214, 107, 106, 45, 93, 212, 20,
    111, 73, 162, 251, 97, 215, 249, 53, 211, 19, 3, 89,
    49, 207, 101, 67, 151, 130, 223, 23, 189, 202, 178, 239,
    253, 127, 204, 49, 76, 236, 82, 137, 232, 157, 65, 79,
    96, 161, 176, 130, 161, 30, 47, 9, 189, 247, 61, 226,
    248, 90, 107, 64, 0, 88, 131, 243, 133, 59, 113, 115,
    17, 236, 33, 213, 12, 191, 111, 19, 251, 61, 103, 208,
    57, 35, 148, 248, 47, 116, 65, 119, 249, 178, 143, 40,
    189, 129, 8, 163, 204, 227, 230, 196, 205, 122, 151, 45,
    187, 19, 227, 72, 247, 125, 111, 121, 140, 220, 6, 107,
    77, 69, 10, 101, 21, 65, 149, 171, 255, 54, 101, 210,
    139, 43, 150, 151, 212, 164, 45, 237, 146, 184, 95, 6,
    160, 42, 8, 204, 46, 238, 254, 168, 208, 50, 156, 190,
    106, 127, 34, 234, 68, 55, 79, 18, 4, 130, 53, 208,
    181, 21, 175, 120, 25, 100, 192, 178, 161, 96, 81, 127,
    96, 227, 210, 248, 68, 10, 196, 31, 9, 167, 150, 193,
    0, 169, 126, 14, 124, 198, 144, 142, 240, 21, 224, 44,
    245, 66, 146, 238, 6, 196, 154, 49, 200, 222, 109, 9,
    210, 141, 192, 138, 8, 79, 114, 217, 68, 128, 249, 94,
    53, 30, 27, 61, 52, 135, 106, 212, 70, 238, 30, 185,
    10, 132, 146, 136, 117, 37, 251, 150, 180, 188, 247, 156,
    236, 192, 108, 86
]


WB_DATA = [
    [
        [4, 0, 1, 185],
        [6, 0, 1, 185],
        [0, 0, 1, 185],
        [2, 0, 1, 185],
        [7, 0, 1, 185],
        [5, 0, 1, 185],
        [3, 0, 1, 185],
        [1, 0, 1, 185]
    ],
    [
        [15, 0, 1, 185],
        [11, 0, 1, 185],
        [12, 0, 1, 185],
        [8, 0, 1, 185],
        [9, 0, 1, 185],
        [13, 0, 1, 185],
        [10, 0, 1, 185],
        [14, 0, 1, 185]
    ],
    [
        [17, -256, -128, 233],
        [18, -256, -128, 233],
        [23, -256, -128, 233],
        [20, -256, -128, 233],
        [22, -256, -128, 233],
        [21, -256, -128, 233],
        [16, -256, -128, 233],
        [19, -256, -128, 233]
    ],
    [
        [30, -383, -255, 233],
        [24, -383, -255, 233],
        [25, -383, -255, 233],
        [31, -383, -255, 233],
        [27, -383, -255, 233],
        [29, -383, -255, 233],
        [28, -383, -255, 233],
        [26, -383, -255, 233]
    ]
]


def REDS1(x):
    return ((x & 0xFF) - (x >> 8))


def REDS2(x):
    return ((x & 0xFFFF) + (x >> 16))


def IF(x, y, z):
    return ((y ^ z) & x) ^ (z)


def MAJ(x, y, z):
    return (x & y) | ((x | y) & (z))


def FFT_LOOP(q, qOffset, hk, _as):
    m = q[(qOffset)]
    n = q[(qOffset) + (hk)]
    q[(qOffset)] = m + n
    q[(qOffset) + (hk)] = m - n
    u = v = 0
    firstTime = True
    while u < hk:
        if not firstTime:
            m = q[(qOffset) + u + 0]
            n = q[(qOffset) + u + 0 + (hk)]
            t = REDS2(n * alpha_tab[v + 0 * (_as)])
            q[(qOffset) + u + 0] = m + t
            q[(qOffset) + u + 0 + (hk)] = m - t
        else:
            firstTime = False
        m = q[(qOffset) + u + 1]
        n = q[(qOffset) + u + 1 + (hk)]
        t = REDS2(n * alpha_tab[v + int(_as)])
        q[(qOffset) + u + 1] = m + t
        q[(qOffset) + u + 1 + (hk)] = m - t
        m = q[(qOffset) + u + 2]
        n = q[(qOffset) + u + 2 + (hk)]
        t = REDS2(n * alpha_tab[v + 2 * (_as)])
        q[(qOffset) + u + 2] = m + t
        q[(qOffset) + u + 2 + (hk)] = m - t
        m = q[(qOffset) + u + 3]
        n = q[(qOffset) + u + 3 + (hk)]
        t = REDS2(n * alpha_tab[v + 3 * (_as)])
        q[(qOffset) + u + 3] = m + t
        q[(qOffset) + u + 3 + (hk)] = m - t
        u += 4
        v += 4 * _as


def FFT8(x, xOffset, xs, d):
    x0 = x[(xOffset)]
    x1 = x[(xOffset) + (xs)]
    x2 = x[(xOffset) + 2 * (xs)]
    x3 = x[(xOffset) + 3 * (xs)]
    a0 = x0 + x2
    a1 = x0 + (x2 << 4)
    a2 = x0 - x2
    a3 = x0 - (x2 << 4)
    b0 = x1 + x3
    b1 = REDS1((x1 << 2) + (x3 << 6))
    b2 = (x1 << 4) - (x3 << 4)
    b3 = REDS1((x1 << 6) + (x3 << 2))
    d[0] = a0 + b0
    d[1] = a1 + b1
    d[2] = a2 + b2
    d[3] = a3 + b3
    d[4] = a0 - b0
    d[5] = a1 - b1
    d[6] = a2 - b2
    d[7] = a3 - b3


def FFT16(x, xOffset, q, qOffset, xs):
    d1 = [None] * 8
    d2 = [None] * 8
    FFT8(x, xOffset, (xs) << 1, d1)
    FFT8(x, (xOffset) + (xs), (xs) << 1, d2)
    for i in range(8):
        q[(qOffset) + i] = d1[i] + (d2[i] << i)

    for i in range(8):
        q[(qOffset) + 8 + i] = d1[i] - (d2[i] << i)


def FFT32(x, xOffset, q, qOffset, xs):
    xd = xs << 1
    FFT16(x, xOffset, q, qOffset, xd)
    FFT16(x, xOffset + xs, q, qOffset + 16, xd)
    FFT_LOOP(q, qOffset, 16, 8)


def FFT64(x, xOffset, q, qOffset, xs):
    xd = xs << 1
    FFT32(x, xOffset, q, qOffset, xd)
    FFT32(x, xOffset + xs, q, qOffset + 32, xd)
    FFT_LOOP(q, qOffset, 32, 4)


def FFT256(x, xOffset, q, qOffset, xs):
    FFT64(x, xOffset, q, qOffset, (xs) << 2)
    FFT64(x, (xOffset) + ((xs) * 2), q, qOffset + 64, (xs) << 2)
    FFT_LOOP(q, qOffset, 64, 2)
    FFT64(x, (xOffset) + (xs), q, qOffset + 128, (xs) << 2)
    FFT64(x, (xOffset) + ((xs) * 3), q, qOffset + 192, (xs) << 2)
    FFT_LOOP(q, qOffset + 128, 64, 2)
    FFT_LOOP(q, qOffset, 128, 1)


PP8 = [
    [1, 0, 3, 2, 5, 4, 7, 6],
    [6, 7, 4, 5, 2, 3, 0, 1],
    [2, 3, 0, 1, 6, 7, 4, 5],
    [3, 2, 1, 0, 7, 6, 5, 4],
    [5, 4, 7, 6, 1, 0, 3, 2],
    [7, 6, 5, 4, 3, 2, 1, 0],
    [4, 5, 6, 7, 0, 1, 2, 3]
]


M7 = [
    [0, 1, 2, 3],
    [1, 2, 3, 4],
    [2, 3, 4, 5],
    [3, 4, 5, 6],
    [4, 5, 6, 0],
    [5, 6, 0, 1],
    [6, 0, 1, 2],
    [0, 1, 2, 3]
]


def INNER(l, h, mm):
    return (((l * mm) & 0xFFFF) + ((h * mm) << 16))


def W_BIG(sb, o1, o2, mm, q):
    r = [None] * 8
    for i in range(8):
        r[i] = INNER(q[16 * (sb) + 2 * i + o1], q[16 * (sb) + 2 * i + o2], mm)
    return r


def WB(x, y, q):
    wb = WB_DATA[x][y]
    return W_BIG(wb[0], wb[1], wb[2], wb[3], q)


def STEP_ELT(n, w, fun, s, ppb, tA, A, B, C, D):
    tt = op.t32(D[n] + (w) + fun(A[n], B[n], C[n]))
    A[n] = op.t32(op.rotl32(tt, s) + tA[ppb[n]])
    D[n] = C[n]
    C[n] = B[n]
    B[n] = tA[n]


def STEP_BIG(w, fun, r, s, pp8b, A, B, C, D):
    tA = [None] * 8
    for i in range(8):
        tA[i] = op.rotl32(A[i], r)

    for i in range(8):
        STEP_ELT(i, w[i], fun, s, pp8b, tA, A, B, C, D)


def ONE_ROUND_BIG(ri, isp, p0, p1, p2, p3, A, B, C, D, q):
    STEP_BIG(WB(ri, 0, q), IF, p0, p1, PP8[M7[0][isp]], A, B, C, D)
    STEP_BIG(WB(ri, 1, q), IF, p1, p2, PP8[M7[1][isp]], A, B, C, D)
    STEP_BIG(WB(ri, 2, q), IF, p2, p3, PP8[M7[2][isp]], A, B, C, D)
    STEP_BIG(WB(ri, 3, q), IF, p3, p0, PP8[M7[3][isp]], A, B, C, D)
    STEP_BIG(WB(ri, 4, q), MAJ, p0, p1, PP8[M7[4][isp]], A, B, C, D)
    STEP_BIG(WB(ri, 5, q), MAJ, p1, p2, PP8[M7[5][isp]], A, B, C, D)
    STEP_BIG(WB(ri, 6, q), MAJ, p2, p3, PP8[M7[6][isp]], A, B, C, D)
    STEP_BIG(WB(ri, 7, q), MAJ, p3, p0, PP8[M7[7][isp]], A, B, C, D)


def compress(ctx, last):
    q = [None] * 256
    A = [None] * 8
    B = [None] * 8
    C = [None] * 8
    D = [None] * 8
    FFT256(ctx['buffer'], 0, q, 0, 1)
    if last:
        for i in range(256):
            tq = q[i] + yoff_b_f[i]
            tq = REDS2(tq)
            tq = REDS1(tq)
            tq = REDS1(tq)
            q[i] = (tq if tq <= 128 else tq - 257)
    else:
        for i in range(256):
            tq = q[i] + yoff_b_n[i]
            tq = REDS2(tq)
            tq = REDS1(tq)
            tq = REDS1(tq)
            q[i] = (tq if tq <= 128 else tq - 257)

    state = ctx['state']
    op.buffer_insert(A,0,state,8)
    op.buffer_insert(B,0,state,8,8)
    op.buffer_insert(C,0,state,8,16)
    op.buffer_insert(D,0,state,8,24)
    x = op.swap32_list(op.bytes_to_i32_list(ctx['buffer']))
    op.buffer_xor_insert(A,0,x,0,8)
    op.buffer_xor_insert(B,0,x,8,8)
    op.buffer_xor_insert(C,0,x,16,8)
    op.buffer_xor_insert(D,0,x,24,8)

    ONE_ROUND_BIG(0, 0, 3, 23, 17, 27, A, B, C, D, q)
    ONE_ROUND_BIG(1, 1, 28, 19, 22, 7, A, B, C, D, q)
    ONE_ROUND_BIG(2, 2, 29, 9, 15, 5, A, B, C, D, q)
    ONE_ROUND_BIG(3, 3, 4, 13, 10, 25, A, B, C, D, q)

    STEP_BIG(state[0:8],IF, 4, 13, PP8[4],A,B,C,D)
    STEP_BIG(state[8:16],IF, 13, 10, PP8[5],A,B,C,D)
    STEP_BIG(state[16:24],IF, 10, 25, PP8[6],A,B,C,D)
    STEP_BIG(state[24:32],IF, 25, 4, PP8[0],A,B,C,D)
    op.buffer_insert(state,0,A,8)
    op.buffer_insert(state,8,B,8)
    op.buffer_insert(state,16,C,8)
    op.buffer_insert(state,24,D,8)
    ctx['state'] = state


def simd_update(ctx, msg):
    ptr = ctx['ptr']
    buf = ctx['buffer']
    buf_len = len(buf)
    msg_len = len(msg)
    while msg_len > 0:
        clen = buf_len - ptr
        if clen > msg_len:
            clen = msg_len
        op.buffer_insert(buf, ptr, msg, clen)
        ptr += clen
        msg = msg[clen:]
        msg_len -= clen
        if ptr == buf_len:
            ctx['ptr'] = ptr
            ctx['buffer'] = buf
            compress(ctx, 0)
            ptr = ctx['ptr'] = 0
            countLow = ctx['countLow']
            countLow = op.t32(countLow + 1)
            if countLow == 0:
                ctx['countHigh'] += 1

            ctx['countLow'] = countLow
    ctx['ptr'] = ptr


def encode_count(dst, offset, low, high, ptr, n):
    low = op.t32(low << 10)
    high = op.t32(high << 10) + (low >> 22)
    low += (ptr << 3) + n
    dst[offset] = low & 0xFF
    dst[offset + 1] = op.rshift32b(low & 0xFF00, 8)
    dst[offset + 2] = op.rshift32b(low & 0xFF0000, 8)
    dst[offset + 3] = op.rshift32b(low & 0xFF000000, 8)
    dst[offset + 4] = high & 0xFF
    dst[offset + 5] = op.rshift32b(high & 0xFF00, 8)
    dst[offset + 6] = op.rshift32b(high & 0xFF0000, 8)
    dst[offset + 7] = op.rshift32b(high & 0xFF000000, 8)


def simd_close(ctx, ub, n):
    buf = ctx['buffer']
    buf_len = len(buf)
    ptr = ctx['ptr']

    if ptr > 0 or n > 0:
        set_len = buf_len - ptr
        buf[ptr:ptr+set_len] = [0] * set_len
        buf[ptr] = ub & (0xFF << (8 - n))
        compress(ctx, 0)

    buf[0:buf_len] = [0] * buf_len
    encode_count(buf, 0, ctx['countLow'], ctx['countHigh'], ptr, n)
    compress(ctx, 1)
    out = [None] * 16
    for u in range(16):
        state = ctx['state']
        out[u] = op.swap32(state[u])
    return out


def pack_state(state):
    res = b''
    for i in state:
        res += pack('>I', i)
    return res


def simd(msg):
    ctx = {}
    ctx['state'] = IV512[:]
    ctx['ptr'] = 0
    ctx['countLow'] = 0
    ctx['countHigh'] = 0
    ctx['buffer'] = bytearray(128)
    simd_update(ctx, msg)
    res = simd_close(ctx, 0, 0)
    res = pack_state(res)
    pprint(res.hex())
