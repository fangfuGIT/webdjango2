# _*_ coding: utf-8 _*_
__author__ = 'fangfu'
__date__ = '2018/8/13 16:33'


import base64
import random


class encode_decode(object):
    def encode(str):
        code = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
        random_str = ''
        length = len(code) - 1
        for i in range(62):
            random_str += code[random.randint(0, length)]
        bytesStr = str.encode(encoding='utf8')
        encodeStr = base64.b64encode(bytesStr)
        en = encodeStr.decode()
        str_en = "".join(x + y for x, y in zip(random_str, en))
        trantab = str_en.maketrans('=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
                                   'ewJNqaLVklFsXEzAxMviZWHm=poGgBYbuPTSnIUchjCRyOdfKtrDQ')
        str_fin = str_en.translate(trantab)
        return str_fin[::-1]

    def decode(destr):
        cstr = destr[::-1]
        trantab = cstr.maketrans('ewJNqaLVklFsXEzAxMviZWHm=poGgBYbuPTSnIUchjCRyOdfKtrDQ',
                                 '=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
        str = cstr.translate(trantab)
        str_fin = str[1::2]
        co = base64.b64decode(str_fin)
        decodestr = co.decode()
        return decodestr





