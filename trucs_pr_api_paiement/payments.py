from litecoinutils.transactions import Transaction as Transaction2
from litecoinutils.transactions import TxInput, TxOutput
from litecoinutils.keys import PrivateKey, P2pkhAddress
from litecoinutils.utils import to_satoshis
from litecoinutils.setup import setup
from ecdsa import SigningKey as SigningKey2
from ecdsa import SECP256k1
from ecdsa.util import sigencode_der
import datetime
import re
import os
from nacl.signing import SigningKey
import ecdsa
from ecpy.curves import Curve
from ecpy.keys import ECPublicKey, ECPrivateKey
from sha3 import keccak_256
from web3 import Web3
import requests
import base58
import hashlib
from bit import Key
from bit.network import NetworkAPI
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.transaction import Transaction
from solders.system_program import transfer, TransferParams
from solana.rpc.api import Client
from solana.rpc.types import TxOpts


def ltcpp():
    def sha256(data):
        digest = hashlib.new("sha256")
        digest.update(data)
        return digest.digest()

    def ripemd160(data):
        d = hashlib.new("ripemd160")
        d.update(data)
        return d.digest()

    def b58(data):
        B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
        if data[0] == 0:
            return "1" + b58(data[1:])
        x = sum([v * (256 ** i) for i, v in enumerate(data[::-1])])
        ret = ""
        while x > 0:
            ret = B58[x % 58] + ret
            x = x // 58
        return ret

    class Point:
        def __init__(self,
                     x=0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
                     y=0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8,
                     p=2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 - 1):
            self.x = x
            self.y = y
            self.p = p

        def __add__(self, other):
            return self.__radd__(other)

        def __mul__(self, other):
            return self.__rmul__(other)

        def __rmul__(self, other):
            n = self
            q = None
            for i in range(256):
                if other & (1 << i):
                    q = q + n
                n = n + n
            return q

        def __radd__(self, other):
            if other is None:
                return self
            x1 = other.x
            y1 = other.y
            x2 = self.x
            y2 = self.y
            p = self.p
            if self == other:
                l = pow(2 * y2 % p, p-2, p) * (3 * x2 * x2) % p
            else:
                l = pow(x1 - x2, p-2, p) * (y1 - y2) % p
            newX = (l ** 2 - x2 - x1) % p
            newY = (l * x2 - l * newX - y2) % p
            return Point(newX, newY)

        def toBytes(self):
            x = self.x.to_bytes(32, "big")
            y = self.y.to_bytes(32, "big")
            return b"\x04" + x + y

    def getPublicKey(privkey):
        SPEC256k1 = Point()
        pk = int.from_bytes(privkey, "big")
        hash160 = ripemd160(sha256((SPEC256k1 * pk).toBytes()))
        address = b"\x30" + hash160
        address = b58(address + sha256(sha256(address))[:4])
        return address

    def getWif(privkey):
        wif = b"\xB0" + privkey
        wif = b58(wif + sha256(sha256(wif))[:4])
        return wif

    randomBytes = os.urandom(32)
    class result:
        prv = getWif(randomBytes)
        pub = getPublicKey(randomBytes)
    return result
def btcpp():
    def sha256(data):
        digest = hashlib.new("sha256")
        digest.update(data)
        return digest.digest()


    def ripemd160(x):
        d = hashlib.new("ripemd160")
        d.update(x)
        return d.digest()


    def b58(data):
        B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

        if data[0] == 0:
            return "1" + b58(data[1:])

        x = sum([v * (256 ** i) for i, v in enumerate(data[::-1])])
        ret = ""
        while x > 0:
            ret = B58[x % 58] + ret
            x = x // 58

        return ret


    class Point:
        def __init__(self,
            x=0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
            y=0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8,
            p=2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 - 1):
            self.x = x
            self.y = y
            self.p = p

        def __add__(self, other):
            return self.__radd__(other)

        def __mul__(self, other):
            return self.__rmul__(other)

        def __rmul__(self, other):
            n = self
            q = None

            for i in range(256):
                if other & (1 << i):
                    q = q + n
                n = n + n

            return q

        def __radd__(self, other):
            if other is None:
                return self
            x1 = other.x
            y1 = other.y
            x2 = self.x
            y2 = self.y
            p = self.p

            if self == other:
                l = pow(2 * y2 % p, p-2, p) * (3 * x2 * x2) % p
            else:
                l = pow(x1 - x2, p-2, p) * (y1 - y2) % p

            newX = (l ** 2 - x2 - x1) % p
            newY = (l * x2 - l * newX - y2) % p

            return Point(newX, newY)

        def toBytes(self):
            x = self.x.to_bytes(32, "big")
            y = self.y.to_bytes(32, "big")
            return b"\x04" + x + y


    def getPublicKey(privkey):
        SPEC256k1 = Point()
        pk = int.from_bytes(privkey, "big")
        hash160 = ripemd160(sha256((SPEC256k1 * pk).toBytes()))
        address = b"\x00" + hash160

        address = b58(address + sha256(sha256(address))[:4])
        return address


    def getWif(privkey):
        wif = b"\x80" + privkey
        wif = b58(wif + sha256(sha256(wif))[:4])
        return wif


    randomBytes = os.urandom(32)
    class result:
        prv=getWif(randomBytes)
        pub=getPublicKey(randomBytes)
    return result
def solpp():
    seed = os.urandom(32)
    signing_key = SigningKey(seed)
    private_key = (signing_key.encode() + signing_key.verify_key.encode()).hex()
    public_key = base58.b58encode(signing_key.verify_key.encode()).decode()

    class result:
        prv=private_key
        pub=public_key
    return result
def ethpp():
    private_key = eval("0x"+os.urandom(32).hex())

    cv = Curve.get_curve('secp256k1')
    pv_key = ECPrivateKey(private_key, cv)
    pu_key = pv_key.get_public_key()

    class result:
        prv=hex(private_key)
        pub='0x' + keccak_256(pu_key.W.x.to_bytes(32, byteorder='big') + pu_key.W.y.to_bytes(32, byteorder='big')).digest()[-20:].hex()
    return result

def getsolbal(addr):

    headers = {
        'Content-Type': 'application/json',
    }

    json_data = {
        'jsonrpc': '2.0',
        'id': 1,
        'method': 'getBalance',
        'params': [
        addr,
        ],
    }

    response = requests.post('https://api.mainnet-beta.solana.com', headers=headers, json=json_data)
    return response.json()["result"]["value"]*0.000000001
def getethbal(addr):
    headers = {
        'Content-Type': 'application/json',
    }

    json_data = {
        'jsonrpc': '2.0',
        'method': 'eth_getBalance',
        'params': [
            addr,
            'safe',
        ],
        'id': 1,
    }

    response = requests.post('https://mainnet.infura.io/v3/API_TOKEN_BLOCKCYPHER', headers=headers, json=json_data)
    return int(response.json()["result"],16)/10**18
def getltcbal(addr):
    return requests.get('https://api.blockcypher.com/v1/ltc/main/addrs/'+addr+'/balance?token=API_TOKEN_BLOCKCYPHER').json()['final_balance']/100000000
def getbtcbal(addr):
    return requests.get(f"https://api.blockcypher.com/v1/btc/main/addrs/{addr}/balance?token=API_TOKEN_BLOCKCYPHER").json()["final_balance"]/100000000

def sendeth(private_key, destination, montant):
    rpc_url = "https://mainnet.infura.io/v3/API_TOKEN_BLOCKCYPHER"
    web3 = Web3(Web3.HTTPProvider(rpc_url))
    if not web3.is_connected():
        raise Exception("Unable to connect to the Ethereum network")
    account = web3.eth.account.from_key(private_key)
    from_address = account.address
    nonce = web3.eth.get_transaction_count(from_address)
    transaction = {
        'to': destination,
        'value': web3.to_wei(montant, 'ether'),
        'gas': 21000,
        'gasPrice': web3.eth.gas_price,
        'nonce': nonce,
        'chainId': web3.eth.chain_id
    }
    signed_transaction = web3.eth.account.sign_transaction(transaction, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_transaction.raw_transaction)
    return web3.to_hex(tx_hash)
def sendltc(private_wif, destination, amount):
    private_wif=base58.b58encode_check(base58.b58decode_check(private_wif) + b'\x01').decode()
    blockcypher_token="API_TOKEN_BLOCKCYPHER"
    amount=int(amount*100000000)
    decoded_wif = base58.b58decode_check(private_wif)
    private_key = decoded_wif[1:-1]
    sk = SigningKey2.from_string(private_key, curve=SECP256k1)
    vk = sk.verifying_key
    public_key = b"\x04" + vk.to_string()
    public_key_hash = hashlib.new("ripemd160", hashlib.sha256(public_key).digest()).digest()
    from_address = base58.b58encode_check(b"\x30" + public_key_hash).decode("utf-8")
    new_tx_url = "https://api.blockcypher.com/v1/ltc/main/txs/new"
    tx_skeleton = {
        "inputs": [{"addresses": [from_address]}],
        "outputs": [{"addresses": [destination], "value": amount}],
    }
    response = requests.post(new_tx_url, json=tx_skeleton)
    if response.status_code != 201:
        raise Exception(f"Error creating transaction: {response.text}")
    tx_data = response.json()
    to_sign = tx_data["tosign"]
    signatures = []
    pubkeys = []
    for msg in to_sign:
        msg_bytes = bytes.fromhex(msg)
        signature = sk.sign_digest(msg_bytes, sigencode=sigencode_der)
        signatures.append(signature.hex())
        pubkeys.append(public_key.hex())
    tx_data["signatures"] = signatures
    tx_data["pubkeys"] = pubkeys
    push_url = f"https://api.blockcypher.com/v1/ltc/main/txs/send?token={blockcypher_token}"
    response = requests.post(push_url, json=tx_data)
    if response.status_code != 201:
        raise Exception(f"Error broadcasting transaction: {response.text}")
    return response.json()
def sendbtc(private_key, destination, amount):
    key = Key(private_key)
    tx_hash = key.send([(destination, amount, 'btc')])
    return tx_hash
def sendsol(private_key, destination, amount):
    client = Client("https://api.mainnet-beta.solana.com")
    private_key_bytes = bytes.fromhex(private_key)
    sender_keypair = Keypair.from_bytes(private_key_bytes)
    destination_pubkey = Pubkey.from_string(destination)
    lamports = int(amount * 10**9)
    transfer_instruction = transfer(
        TransferParams(
            from_pubkey=sender_keypair.pubkey(),
            to_pubkey=destination_pubkey,
            lamports=lamports
        )
    )
    recent_blockhash = client.get_latest_blockhash().value.blockhash
    transaction = Transaction.new_signed_with_payer(
        instructions=[transfer_instruction],
        payer=sender_keypair.pubkey(),
        signing_keypairs=[sender_keypair],
        recent_blockhash=recent_blockhash
    )
    response = client.send_transaction(transaction, opts=TxOpts(skip_preflight=False))
