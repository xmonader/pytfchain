from tfchain.crypto.merkletree import Tree
from tfchain.crypto.utils import blake2_string


def test_basic_merkletree():
    tree = Tree(hash_func=lambda o: bytes.fromhex(blake2_string(o)))
    tree.push(bytearray([1]))
    tree.push(bytearray([2]))
    tree.push(bytearray([3]))
    tree.push(bytearray([4]))
    tree.push(bytearray([5]))
    root = tree.root().hex()
    assert root == '0002789a97a9feee38af3709f06377ef0ad7d91407cbcad1ccb8605556b6578e'
    print('Root is {}'.format(root))
