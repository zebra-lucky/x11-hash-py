# -*- coding: utf-8 -*-
# from http://www.h2database.com/skein/
# Released under the public domain

from . import op


def skein(msg, out_array=False, in_array=False):
    if in_array:
        msg = op.bytes_from_i32_list(msg)
    # final: 0x80; first: 0x40; conf: 0x4; msg: 0x30; out: 0x3f
    msg_len = len(msg)
    msg = bytearray(msg)
    msg.extend([0]*1024)
    tweak = [
        [0, 32],
        [(0x80 + 0x40 + 0x4) << 24, 0]
    ] + [0, 0]
    c = [None] * 9
    buff = [83, 72, 65, 51, 1, 0, 0, 0, 0, 2] + [0] * 1024
    block(c, tweak, buff, 0)
    tweak = [
        [0, 0],
        [(0x40 + 0x30) << 24, 0]
    ] + [0, 0]
    pos = 0
    while msg_len > 64:
        tweak[0][1] += 64
        block(c, tweak, msg, pos)
        tweak[1][0] = 0x30 << 24
        msg_len -= 64
        pos += 64

    tweak[0][1] += msg_len
    tweak[1][0] |= 0x80 << 24
    block(c, tweak, msg, pos)
    tweak[0][1] = 8
    tweak[1][0] = (0x80 + 0x40 + 0x3f) << 24
    block(c, tweak, [0] * 1024, 0)
    out_hash = []
    for i in range(64):
        b = (shiftRight(c[i >> 3], (i & 7) * 8)[1] & 255)
        out_hash.append(b)
    if out_array:
        res = op.bytes_to_i32_list(bytes(out_hash))
    else:
        res = bytes(out_hash)
    return res


def shiftLeft(x, n):
    if x == None:
        return [0, 0]
    if n > 32:
        return [x[1] << (n - 32), 0]
    if n == 32:
        return [x[1], 0]
    if n == 0:
        return x
    return [(x[0] << n) | op.rshift32b(x[1], 32 - n), x[1] << n]


def shiftRight(x, n):
    if x is None:
        return [0, 0]
    if n > 32:
        return [0, op.rshift32b(x[0], (n - 32))]
    if n == 32:
        return [0, x[0]]
    if n == 0:
        return x
    return [op.rshift32b(x[0], n), (x[0] << (32 - n)) | op.rshift32b(x[1], n)]


def add(x, y):
    if y is None:
        return x
    lsw = (x[1] & 0xffff) + (y[1] & 0xffff)
    msw = op.rshift32b(x[1], 16) + op.rshift32b(y[1], 16) + op.rshift32b(lsw, 16)
    lowOrder = ((msw & 0xffff) << 16) | (lsw & 0xffff)
    lsw = (x[0] & 0xffff) + (y[0] & 0xffff) + op.rshift32b(msw, 16)
    msw = op.rshift32b(x[0], 16) + op.rshift32b(y[0], 16) + op.rshift32b(lsw, 16)
    highOrder = ((msw & 0xffff) << 16) | (lsw & 0xffff)
    return [highOrder, lowOrder]


def xor(a, b):
    if b is None:
        return a
    return [a[0] ^ b[0], a[1] ^ b[1]]


def block(c, tweak, b, off):
    R = [
        46, 36, 19, 37, 33, 42, 14, 27, 17, 49, 36, 39, 44, 56, 54, 9,
        39, 30, 34, 24, 13, 17, 10, 50, 25, 29, 39, 43, 8, 22, 56, 35
    ]
    x = [None] * 8
    t = [None] * 8
    # c[8] = [0x55555555, 0x55555555];
    c[8] = [0x1BD11BDA, 0xA9FC1A22]
    for i in range(8):
        j = 7
        k = off + i * 8 + 7
        while j >= 0:
            t[i] = shiftLeft(t[i], 8)
            t[i][1] |= b[k] & 255
            j -= 1
            k -= 1

        x[i] = add(t[i], c[i])
        c[8] = xor(c[8], c[i])

    x[5] = add(x[5], tweak[0])
    x[6] = add(x[6], tweak[1])
    tweak[2] = xor(tweak[0], tweak[1])
    for round_i in range(1,19):
        p = 16 - ((round_i & 1) << 4)
        for i in range(16):
            # m: 0, 2, 4, 6, 2, 0, 6, 4, 4, 6, 0, 2, 6, 4, 2, 0
            m = 2 * ((i + (1 + i + i) * (i >> 2)) & 3)
            n = (1 + i + i) & 7
            r = R[p + i]
            x[m] = add(x[m], x[n])
            x[n] = xor(shiftLeft(x[n], r), shiftRight(x[n], 64 - r))
            x[n] = xor(x[n], x[m])


        for i in range(8):
            x[i] = add(x[i], c[(round_i + i) % 9])
        x[5] = add(x[5], tweak[round_i % 3])
        x[6] = add(x[6], tweak[(round_i + 1) % 3])
        x[7] = add(x[7], [0, round_i])

    for i in range(8):
        c[i] = xor(t[i], x[i])
