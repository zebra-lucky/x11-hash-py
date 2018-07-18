# -*- coding: utf-8 -*-

from . import aes
from . import op


ECHO_BlockSize = 128


def subWords(W, pK):
    for n in range(16):
        X = W[n]
        Y = [None] * 4
        aes.AES_ROUND_LE(X, pK, Y)
        aes.AES_ROUND_NOKEY_LE(Y, X)
        pK[0] = op.t32(pK[0] + 1)
        if pK[0] == 0:
            pK[1] = op.t32(pK[1] + 1)
            if pK[1] == 0:
                pK[2] = op.t32(pK[2] + 1)
                if pK[2] == 0:
                    pK[3] = op.t32(pK[3] + 1)


def shiftRow1(W, a, b, c, d):
    tmp = W[a][0]
    W[a][0] = W[b][0]
    W[b][0] = W[c][0]
    W[c][0] = W[d][0]
    W[d][0] = tmp
    tmp = W[a][1]
    W[a][1] = W[b][1]
    W[b][1] = W[c][1]
    W[c][1] = W[d][1]
    W[d][1] = tmp
    tmp = W[a][2]
    W[a][2] = W[b][2]
    W[b][2] = W[c][2]
    W[c][2] = W[d][2]
    W[d][2] = tmp
    tmp = W[a][3]
    W[a][3] = W[b][3]
    W[b][3] = W[c][3]
    W[c][3] = W[d][3]
    W[d][3] = tmp


def shiftRow2(W, a, b, c, d):
    tmp = W[a][0]
    W[a][0] = W[c][0]
    W[c][0] = tmp
    tmp = W[b][0]
    W[b][0] = W[d][0]
    W[d][0] = tmp
    tmp = W[a][1]
    W[a][1] = W[c][1]
    W[c][1] = tmp
    tmp = W[b][1]
    W[b][1] = W[d][1]
    W[d][1] = tmp
    tmp = W[a][2]
    W[a][2] = W[c][2]
    W[c][2] = tmp
    tmp = W[b][2]
    W[b][2] = W[d][2]
    W[d][2] = tmp
    tmp = W[a][3]
    W[a][3] = W[c][3]
    W[c][3] = tmp
    tmp = W[b][3]
    W[b][3] = W[d][3]
    W[d][3] = tmp


def shiftRow3(W, a, b, c, d):
    shiftRow1(W, d, c, b, a)


def shiftRows(W):
    shiftRow1(W, 1, 5, 9, 13)
    shiftRow2(W, 2, 6, 10, 14)
    shiftRow3(W, 3, 7, 11, 15)


def mixColumn(W, ia, ib, ic, id):
    for n in range(4):
        a = W[ia][n]
        b = W[ib][n]
        c = W[ic][n]
        d = W[id][n]
        ab = a ^ b
        bc = b ^ c
        cd = c ^ d
        abx = (op.rshift32b((ab & (0x80808080)), 7) * 27 ^
            ((ab & (0x7F7F7F7F)) << 1))
        bcx = (op.rshift32b((bc & (0x80808080)), 7) * 27 ^
            ((bc & (0x7F7F7F7F)) << 1))
        cdx = (op.rshift32b((cd & (0x80808080)), 7) * 27 ^
            ((cd & (0x7F7F7F7F)) << 1))
        W[ia][n] = abx ^ bc ^ d
        W[ib][n] = bcx ^ a ^ cd
        W[ic][n] = cdx ^ ab ^ d
        W[id][n] = abx ^ bcx ^ cdx ^ ab ^ c


def finalize(ctx, W):
    state = ctx['state']
    buf32 = op.swap32_list(op.bytes_to_i32_list(ctx['buffer']))
    for u in range(8):
        for v in range(4):
            state[u][v] ^= buf32[u * 4 + v] ^ W[u][v] ^ W[u + 8][v]
    ctx['state'] = state


def inputBlock(ctx, W):
    op.buffer_insert_2d(W, 0, 0, ctx['state'], 8, 4)
    buf32 = op.swap32_list(op.bytes_to_i32_list(ctx['buffer']))
    for u in range(8):
        W[u + 8][0] = (buf32[4 * u])
        W[u + 8][1] = (buf32[4 * u + 1])
        W[u + 8][2] = (buf32[4 * u + 2])
        W[u + 8][3] = (buf32[4 * u + 3])


def mixColumns(W):
    mixColumn(W, 0, 1, 2, 3)
    mixColumn(W, 4, 5, 6, 7)
    mixColumn(W, 8, 9, 10, 11)
    mixColumn(W, 12, 13, 14, 15)


def ROUND(W,K):
    subWords(W,K)
    shiftRows(W)
    mixColumns(W)


def compress(ctx):
    W = [None] * 16
    for i in range(16):
        W[i] = [None] * 4
    K = [None] * 4
    C = ctx['C']
    op.buffer_insert(K, 0, C, 4)
    inputBlock(ctx, W)
    for u in range(10):
        ROUND(W,K)
    finalize(ctx,W)


def incrCounter(ctx, val):
    C = ctx['C']
    C[0] = op.t32(C[0] + op.t32(val))
    if C[0] < op.t32(val):
        C[1] = op.t32(C[1] + 1)
        if C[1] == 0:
            C[2] = op.t32(C[2] + 1)
            if C[2] == 0:
                C[3] = op.t32(C[3] + 1);
    ctx['C'] = C



def echoInit(ctx):
    state = [None] * 8
    for i in range(8):
        state[i] = [None] * 4
    state[0][0] = 512
    state[0][1] = state[0][2] = state[0][3] = 0
    state[1][0] = 512
    state[1][1] = state[1][2] = state[1][3] = 0
    state[2][0] = 512
    state[2][1] = state[2][2] = state[2][3] = 0
    state[3][0] = 512
    state[3][1] = state[3][2] = state[3][3] = 0
    state[4][0] = 512
    state[4][1] = state[4][2] = state[4][3] = 0
    state[5][0] = 512
    state[5][1] = state[5][2] = state[5][3] = 0
    state[6][0] = 512
    state[6][1] = state[6][2] = state[6][3] = 0
    state[7][0] = 512
    state[7][1] = state[7][2] = state[7][3] = 0
    ctx['state'] = state
    ctx['ptr'] = 0
    C = [0] * 4
    ctx['C'] = C
    ctx['buffer'] = bytearray(ECHO_BlockSize)


def echo_update(ctx, msg):
    buf = ctx['buffer']
    ptr = ctx['ptr']
    msg_len = len(msg)
    buf_len = len(buf)
    if msg_len < buf_len - ptr:
        op.buffer_insert(buf, ptr, msg, msg_len)
        ptr += msg_len
        ctx['ptr'] = ptr
        return

    while msg_len > 0:
        clen = buf_len - ptr
        if clen > msg_len:
            clen = msg_len
        op.buffer_insert(buf, ptr, msg, clen)
        ptr += clen
        msg = msg[clen:]
        msg_len -= clen
        if ptr == buf_len:
            incrCounter(ctx, 1024)
            compress(ctx)
            ptr = 0
    ctx['ptr'] = ptr


def echo_close(ctx):
    out = [None] * 16
    buf = ctx['buffer']
    buf_len = len(buf)
    ptr = ctx['ptr']
    elen = (ptr << 3)
    incrCounter(ctx, elen)
    C = ctx['C']
    cBytes = op.bytes_from_i32_list(op.swap32_list(C))
    if elen is 0:
        C[0] = C[1] = C[2] = C[3] = 0
        ctx['C'] = C

    buf[ptr] = 0x80
    ptr += 1

    set_len = buf_len - ptr
    buf[ptr:ptr+set_len] = [0] * set_len
    if ptr > (buf_len - 18):
        compress(ctx)
        ctx['C'][0:4] = [0] * 4
        buf[0:buf_len] = [0] * buf_len

    buf[buf_len-17] = 2
    op.buffer_insert(buf, buf_len-16, cBytes, 16)
    compress(ctx)
    for u in range(4):
        for v in range(4):
            state = ctx['state']
            out[u*4 + v] = op.swap32(state[u][v])
    return out


def echo(msg, out_array=False, in_array=False):
    ctx = {}
    echoInit(ctx)
    if in_array:
        msg = op.bytes_from_i32_list(msg)
    echo_update(ctx, msg)
    res = echo_close(ctx)
    if not out_array:
        res = op.bytes_from_i32_list(res)
    return res
