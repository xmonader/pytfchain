from pyblake2 import blake2b


def blake2_string(s, digest_size=32):
    '''Calculate blake2 hash of input string

    @param s: String value to hash
    @type s: string

    @returns: blake2 hash of the input value
    @rtype: number
    '''
    if isinstance(s, str):
        s = s.encode()
    h = blake2b(s, digest_size=digest_size)
    return h.hexdigest()
