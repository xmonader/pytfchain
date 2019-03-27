
from .PrimitiveTypes import BinaryData, Hash, Currency, Blockstake
from .FulfillmentTypes import FulfillmentFactory
from .ConditionTypes import ConditionFactory
from .ThreeBot import ThreeBotTypesFactory
from .CryptoTypes import PublicKey, PublicKeySpecifier
from .TransactionFactory import TransactionFactory
from tfchain.crypto import MerkleTree


class TFChainTypeFactory:
    """
    TFChain Types Factory class
    """

    def __init__(self):
        self._transaction_factory = TransactionFactory()
        self._fulfillment_factory = FulfillmentFactory()
        self._condition_factory = ConditionFactory()
        self._threebot_types_factory = ThreeBotTypesFactory()

    @property
    def transactions(self):
        return self._transaction_factory

    @property
    def fulfillments(self):
        """
        Fulfillment types.
        """
        return self._fulfillment_factory

    @property
    def conditions(self):
        """
        Condition types.
        """
        return self._condition_factory

    @property
    def threebot(self):
        """
        ThreeBot types.
        """
        return self._threebot_types_factory

    def currency_new(self, value=0):
        """
        Create a new currency value.

        @param value: str or int that defines the value to be set, 0 by default
        """
        return Currency(value=value)

    def blockstake_new(self, value=0):
        """
        Create a new block stake value.

        @param value: str or int that defines the value to be set, 0 by default
        """
        return Blockstake(value=value)

    def hash_new(self, value=None):
        """
        Create a new hash value.

        @param value: bytearray, bytes or str that defines the hash value to be set, nil hash by default
        """
        return Hash(value=value)

    def binary_data_new(self, value=None, fixed_size=None, strencoding=None):
        """
        Create a new binary data value.

        @param value: bytearray, bytes or str that defines the hash value to be set, nil hash by default
        """
        return BinaryData(value=value, fixed_size=fixed_size, strencoding=strencoding)

    def public_key_new(self, hash=None):
        """
        Create a new NIL or ED25519 public key.

        @param hash: bytearray, bytes or str that defines the hash value to be set, nil hash by default
        """
        if not hash:
            return PublicKey()
        return PublicKey(specifier=PublicKeySpecifier.ED25519, hash=hash)

    def public_key_from_json(self, obj):
        """
        Create a new public key from a json string.

        @param obj: str that contains a nil str or a json string
        """
        return PublicKey.from_json(obj)

    def merkle_tree_new(self):
        """
        Create a new MerkleTree
        """
        return Tree(hash_func=lambda o: bytes.fromhex(blake2_string(o)))
