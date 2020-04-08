import unittest
from bip32_hd_wallet import PrivKeyNode, bip32_seed_from_mnemonic
from helper import hash160, h160_to_p2wpkh_address


class TestBip84(unittest.TestCase):
    def test_vector_1(self):
        mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
        root_prv = "zprvAWgYBBk7JR8Gjrh4UJQ2uJdG1r3WNRRfURiABBE3RvMXYSrRJL62XuezvGdPvG6GFBZduosCc1YP5wixPox7zhZLfiUm8aunE96BBa4Kei5"
        root_pub = "zpub6jftahH18ngZxLmXaKw3GSZzZsszmt9WqedkyZdezFtWRFBZqsQH5hyUmb4pCEeZGmVfQuP5bedXTB8is6fTv19U1GQRyQUKQGUTzyHACMF"
        node = PrivKeyNode.master_key(
            bip32_seed=bip32_seed_from_mnemonic(mnemonic=mnemonic)
        )
        self.assertEqual(node.extended_public_key(version=0x04b24746), root_pub)
        self.assertEqual(node.extended_private_key(version=0x04b2430c), root_prv)

        privkey = "KyZpNDKnfs94vbrwhJneDi77V6jF64PWPF8x5cdJb8ifgg2DUc9d"
        pubkey = "0330d54fd0dd420a6e5f8d3624f5f3482cae350f79d5f0753bf5beef9c2d91af3c"
        address = "bc1qcr8te4kr609gcawutmrza0j4xv80jy8z306fyu"
        # Account 0, first receiving address = m/84'/0'/0'/0/0
        child = node.derive_path(index_list=[84 + 2**31, 2**31, 2**31, 0, 0])
        self.assertEqual(child.private_key.wif(), privkey)
        self.assertEqual(child.public_key.sec().hex(), pubkey)
        self.assertEqual(
            h160_to_p2wpkh_address(hash160(child.public_key.sec())),
            address
        )

        privkey = "Kxpf5b8p3qX56DKEe5NqWbNUP9MnqoRFzZwHRtsFqhzuvUJsYZCy"
        pubkey = "03e775fd51f0dfb8cd865d9ff1cca2a158cf651fe997fdc9fee9c1d3b5e995ea77"
        address = "bc1qnjg0jd8228aq7egyzacy8cys3knf9xvrerkf9g"
        # Account 0, second receiving address = m/84'/0'/0'/0/1
        child = node.derive_path(index_list=[84 + 2**31, 2**31, 2**31, 0, 1])
        self.assertEqual(child.private_key.wif(), privkey)
        self.assertEqual(child.public_key.sec().hex(), pubkey)
        self.assertEqual(
            h160_to_p2wpkh_address(hash160(child.public_key.sec())),
            address
        )

        privkey = "KxuoxufJL5csa1Wieb2kp29VNdn92Us8CoaUG3aGtPtcF3AzeXvF"
        pubkey = "03025324888e429ab8e3dbaf1f7802648b9cd01e9b418485c5fa4c1b9b5700e1a6"
        address = "bc1q8c6fshw2dlwun7ekn9qwf37cu2rn755upcp6el"
        # Account 0, first change address = m/84'/0'/0'/1/0
        child = node.derive_path(index_list=[84 + 2**31, 2**31, 2**31, 1, 0])
        self.assertEqual(child.private_key.wif(), privkey)
        self.assertEqual(child.public_key.sec().hex(), pubkey)
        self.assertEqual(
            h160_to_p2wpkh_address(hash160(child.public_key.sec())),
            address
        )

    def test_vector_2(self):
        mnemonic = "banner list crush drill oxygen grit donate chair expect cloud artist window dignity company salad clinic follow drive narrow crater enlist tortoise stay rain"
        root_prv = "zprvAWgYBBk7JR8GkcWB8q5mgDpogpFeNqyVjpci1VHK6JYJnnihE2a6wqAJJevA6HXD58vzF74DHBrpAZPEQNrugy6y1ZocLGuR4fMbkVtQBYJ"
        root_pub = "zpub6jftahH18ngZy6aeErcn3MmYEr68nJhM73YJosgvee5Hfb3qmZtMVdUn9vmFPn81ZLTMwbC6b2zLcw17wGfg97jjZMYftosaCFee3wNg4ih"
        node = PrivKeyNode.master_key(
            bip32_seed=bip32_seed_from_mnemonic(mnemonic=mnemonic)
        )
        self.assertEqual(node.extended_public_key(version=0x04b24746), root_pub)
        self.assertEqual(node.extended_private_key(version=0x04b2430c),
                         root_prv)

        privkey = "KwPVPXy7HXg7h575VFENH8VEZedSNKmVEww9SBwVcY97oWf4iXZb"
        pubkey = "027b2dedd385c39132883a9ee31a4176fc7951a3ce61bfa9138c3eb9f818391b74"
        address = "bc1q0xc3z0qkux40884uqzan8ny4hmth4srl9fm5f3"
        # Account 0, first receiving address = m/84'/0'/0'/0/0
        child = node.derive_path(
            index_list=[84 + 2 ** 31, 2 ** 31, 2 ** 31, 0, 0])
        self.assertEqual(child.private_key.wif(), privkey)
        self.assertEqual(child.public_key.sec().hex(), pubkey)
        self.assertEqual(
            h160_to_p2wpkh_address(hash160(child.public_key.sec())),
            address
        )

        privkey = "L3XXZ8mcJ4j2E39T6CC9GSk4coPKH6srRn9sGdj9UJahRfUasqNk"
        pubkey = "024c128fbc3d35d13de68fc6d641dd9a3f220117d2565546aeb9051c9f37617d14"
        address = "bc1qzhrav6ktxvgyet00uup8pw7lwr7s2p9z4p5uar"
        # Account 0, second receiving address = m/84'/0'/0'/0/1
        child = node.derive_path(
            index_list=[84 + 2 ** 31, 2 ** 31, 2 ** 31, 0, 1])
        self.assertEqual(child.private_key.wif(), privkey)
        self.assertEqual(child.public_key.sec().hex(), pubkey)
        self.assertEqual(
            h160_to_p2wpkh_address(hash160(child.public_key.sec())),
            address
        )

        privkey = "L1tEGjKn8oCY5ZoAQFo9PQk9ttcidcV5qkwXsMZfum13LFizmdoQ"
        pubkey = "039d576e00f67c7953776d8bbd3f2f82b8eb139ab1251e284efb143a136be6c57b"
        address = "bc1qsr3a7v4cmnakvharlacssz034vjrqw8sd03cp9"
        # Account 0, first change address = m/84'/0'/0'/1/0
        child = node.derive_path(
            index_list=[84 + 2 ** 31, 2 ** 31, 2 ** 31, 1, 0])
        self.assertEqual(child.private_key.wif(), privkey)
        self.assertEqual(child.public_key.sec().hex(), pubkey)
        self.assertEqual(
            h160_to_p2wpkh_address(hash160(child.public_key.sec())),
            address
        )
