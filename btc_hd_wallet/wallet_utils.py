import enum
from typing import Any, List, Union


class Bip(enum.Enum):
    BIP44 = 0
    BIP49 = 1
    BIP84 = 2
    # when it is unknown bip - go with xprv xpub tprv tpub
    UNKNOWN = 0


class Key(enum.Enum):
    PRV = 0
    PUB = 1


def list_get(lst: list, i: int) -> Any:
    try:
        return lst[i]
    except IndexError:
        return None


class Version(object):

    __slots__ = (
        "key_type",
        "bip_type",
        "testnet"
    )

    main: dict = {
        Key.PUB.name: {
            Bip.BIP44.name: 0x0488B21E,
            Bip.BIP49.name: 0x049d7cb2,
            Bip.BIP84.name: 0x04b24746
        },
        Key.PRV.name: {
            Bip.BIP44.name: 0x0488ADE4,
            Bip.BIP49.name: 0x049d7878,
            Bip.BIP84.name: 0x04b2430c
        }
    }
    test: dict = {
        Key.PUB.name: {
            Bip.BIP44.name: 0x043587CF,
            Bip.BIP49.name: 0x044a5262,
            Bip.BIP84.name: 0x045f1cf6
        },
        Key.PRV.name: {
            Bip.BIP44.name: 0x04358394,
            Bip.BIP49.name: 0x044a4e28,
            Bip.BIP84.name: 0x045f18bc
        }
    }

    def __init__(self, key_type: int, bip: int, testnet: bool):
        self.key_type = Key(key_type)
        self.bip_type = Bip(bip)
        self.testnet = testnet

    def __int__(self) -> int:
        if self.testnet:
            return self.test[self.key_type.name][self.bip_type.name]
        return self.main[self.key_type.name][self.bip_type.name]

    def __index__(self) -> int:
        return self.__int__()

    @classmethod
    def parse(cls, version_int: int) -> "Version":
        """
        Initializes version object from extended key version.

        :param version_int: extended key version
        :type version_int: int
        :return: version object
        :rtype: Version
        """
        if not isinstance(version_int, int):
            raise ValueError("has to be integer")
        if not cls.valid_version(version=version_int):
            raise ValueError("unsupported version")
        testnet = version_int in cls.testnet_versions()
        private = version_int in cls.priv_versions()
        return cls(
            key_type=Key.PRV.value if private else Key.PUB.value,
            bip=cls.bip(version=version_int),
            testnet=testnet
        )

    @classmethod
    def valid_version(cls, version: int) -> bool:
        _all = cls.testnet_versions() + cls.mainnet_versions()
        if version in _all:
            return True
        return False

    @classmethod
    def bip(cls, version: int) -> int:
        if version in cls.bip44_data().values():
            return Bip.BIP44.value
        elif version in cls.bip49_data().values():
            return Bip.BIP49.value
        elif version in cls.bip84_data().values():
            return Bip.BIP84.value
        else:
            return Bip.BIP44.value

    @classmethod
    def bip44_data(cls) -> dict:
        return {
            "xprv": cls.main[Key.PRV.name][Bip.BIP44.name],
            "xpub": cls.main[Key.PUB.name][Bip.BIP44.name],
            "tprv": cls.test[Key.PRV.name][Bip.BIP44.name],
            "tpub": cls.test[Key.PUB.name][Bip.BIP44.name],
        }

    @classmethod
    def bip49_data(cls) -> dict:
        return {
            "yprv": cls.main[Key.PRV.name][Bip.BIP49.name],
            "ypub": cls.main[Key.PUB.name][Bip.BIP49.name],
            "uprv": cls.test[Key.PRV.name][Bip.BIP49.name],
            "upub": cls.test[Key.PUB.name][Bip.BIP49.name],
        }

    @classmethod
    def bip84_data(cls) -> dict:
        return {
            "zprv": cls.main[Key.PRV.name][Bip.BIP84.name],
            "zpub": cls.main[Key.PUB.name][Bip.BIP84.name],
            "vprv": cls.test[Key.PRV.name][Bip.BIP84.name],
            "vpub": cls.test[Key.PUB.name][Bip.BIP84.name],
        }

    @staticmethod
    def get_versions(dct: dict) -> List[int]:
        res = []
        for k, v in dct.items():
            res += v.values()
        return res

    @classmethod
    def key_versions(cls, key_type: str) -> List[int]:
        return list(cls.test[key_type].values()) + \
               list(cls.main[key_type].values())

    @classmethod
    def mainnet_versions(cls) -> List[int]:
        return cls.get_versions(cls.main)

    @classmethod
    def testnet_versions(cls) -> List[int]:
        return cls.get_versions(cls.test)

    @classmethod
    def priv_versions(cls) -> List[int]:
        return cls.key_versions(key_type=Key.PRV.name)

    @classmethod
    def pub_versions(cls) -> List[int]:
        return cls.key_versions(key_type=Key.PUB.name)


class Bip32Path(object):

    __slots__ = (
        "purpose",
        "coin_type",
        "account",
        "chain",
        "addr_index",
        "private"
    )

    def __init__(self, purpose: int = None, coin_type: int = None,
                 account: int = None, chain: int = None, addr_index: int = None,
                 private=True):
        self.purpose = purpose
        self.coin_type = coin_type
        self.account = account
        self.chain = chain
        self.addr_index = addr_index
        self.private = private
        self.integrity_check()

    def integrity_check(self) -> None:
        none_found = False
        for item in self._to_list():
            if item is None:
                none_found = True
            else:
                if none_found:
                    raise RuntimeError("integrity check failure")
                if not isinstance(item, int):
                    raise ValueError("has to be int")

    def __repr__(self) -> str:
        items = [self.repr_hardened(i) for i in self.to_list()]
        items = [self.m] + items
        return "/".join(items)

    def __eq__(self, other: "Bip32Path") -> bool:
        return self.m == other.m and \
            self.purpose == other.purpose and \
            self.coin_type == other.coin_type and \
            self.account == other.account and \
            self.chain == other.chain and \
            self.addr_index == other.addr_index

    @property
    def m(self) -> str:
        return "m" if self.private else "M"

    @property
    def bitcoin_testnet(self) -> bool:
        return self.coin_type == 0x80000001

    @property
    def bitcoin_mainnet(self) -> bool:
        return self.coin_type == 0x80000000

    @property
    def external_chain(self) -> bool:
        return self.chain == 0

    @property
    def bip44(self) -> bool:
        return self.purpose == 44 + (2 ** 31)

    @property
    def bip49(self) -> bool:
        return self.purpose == 49 + (2 ** 31)

    @property
    def bip84(self) -> bool:
        return self.purpose == 84 + (2 ** 31)

    def bip(self) -> int:
        if self.bip44:
            return Bip.BIP44.value
        elif self.bip49:
            return Bip.BIP49.value
        elif self.bip84:
            return Bip.BIP84.value
        else:
            return Bip.BIP44.value

    @staticmethod
    def is_hardened(num: int) -> bool:
        return num >= 2 ** 31

    @staticmethod
    def is_private(sign) -> bool:
        return True if sign == "m" else False

    @staticmethod
    def convert_hardened(str_int: str) -> int:
        if str_int[-1] == "'":
            return int(str_int[:-1]) + (2 ** 31)
        return int(str_int)

    def repr_hardened(self, num: int) -> str:
        if self.is_hardened(num):
            return str(num - 2 ** 31) + "'"
        else:
            return str(num)

    def _to_list(self) -> List[Union[int, None]]:
        return [
            self.purpose,
            self.coin_type,
            self.account,
            self.chain,
            self.addr_index
        ]

    def to_list(self) -> List[int]:
        return [x for x in self._to_list() if x is not None]

    @classmethod
    def parse(cls, s: str) -> "Bip32Path":
        s_lst = s.split("/")
        if s_lst[0] not in ("m", "M"):
            raise ValueError("incorrect marker")
        purpose = list_get(s_lst, 1)
        coin_type = list_get(s_lst, 2)
        account = list_get(s_lst, 3)
        chain = list_get(s_lst, 4)
        addr_index = list_get(s_lst, 5)
        return cls(
            purpose=cls.convert_hardened(purpose) if purpose else None,
            coin_type=cls.convert_hardened(coin_type) if coin_type else None,
            account=cls.convert_hardened(account) if account else None,
            chain=cls.convert_hardened(chain) if chain else None,
            addr_index=cls.convert_hardened(addr_index) if addr_index else None,
            private=cls.is_private(sign=s_lst[0])
        )
