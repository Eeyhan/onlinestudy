import hashlib


def gen_md5(value):
    hash_key = 'password'
    res = value + hash_key
    res = hashlib.md5(res.encode()).hexdigest()

    return res

