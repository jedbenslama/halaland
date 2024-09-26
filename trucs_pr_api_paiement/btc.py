import time
from bit import PrivateKey
from bit.network import NetworkAPI
import json
import requests
key = PrivateKey()
print(f"privatekey: {key.to_wif()}")
wallet_address = key.address
print(f"New wallet addr: {wallet_address}")
def attetenvoie(destination_address, private_key):
    while True:
        balance = float(private_key.get_balance('btc'))
        print(f"Balance: {balance} BTC")
        if balance > 0:
            print("Argent recu sending...")
            for essai in range(100): 
                try:
                    tx_hash = private_key.send([(destination_address, balance-balance*(essai/100), 'btc')])
                    break
                except Exception as e:
                    print(e)
                    print(f"pas reussi avec {balance-balance*(essai/100)} BTC")
            print(f"reussi TX: {tx_hash}")
            break
        time.sleep(10)
attetenvoie("bc1qvhjtu49kts9t9pwqd04rcsqx22c4etckun78vg", key)
