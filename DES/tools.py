def pad(s, length, fill='0', LEFT: bool = True):
    return (length - len(s)) * fill + s if LEFT else s + (length - len(s)) * fill


def hex2bin(text):
    ret = ''
    for i in text:
        tmp = bin(int(i, 16))[2:]
        ret += pad(tmp, 4)
    return ret


def bin2hex(text):
    ret = ''
    for i in range(0, len(text), 4):
        tmp = text[i:i + 4]
        ret += hex(int(tmp, 2))[2:]
    return ret
