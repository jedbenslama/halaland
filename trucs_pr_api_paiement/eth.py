import time
from web3 import Web3
from eth_account import Account


infura_url = "https://mainnet.infura.io/v3/7118aac17ed44460928e59919b048294"
w3 = Web3(Web3.HTTPProvider(infura_url))


account = Account.create()
private_key = account._private_key.hex()
wallet_address = account.address

print(f"New addr: {wallet_address}")
print(f"Private Key: {private_key}")


destination_address = "0x137512fD7CE8e6A841859227B674bF186D811D80"


def get_balance(address):
    balance = w3.eth.get_balance(address)
    print(f"{balance}")
    return w3.from_wei(balance, 'ether')


def send_payment(private_key, to_address, amount):
    nonce = w3.eth.get_transaction_count(wallet_address)
    gas_price = w3.eth.gas_price
    tx = {
        'nonce': nonce,
        'to': to_address,
        'value': w3.to_wei(amount, 'ether'),
        'gas': 21000,
        'gasPrice': gas_price
    }
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f"reussi TX: {w3.to_hex(tx_hash)}")


print("Waiting 4 paiement...")
while True:
    balance = get_balance(wallet_address)
    if balance > 0:
        print(f"recu: {balance} ETH")
        for essai in range(100):
            try:
                send_payment(private_key, destination_address, float(balance)-float(balance)*(essai/100))
                break
            except:
                print(f"Fail {float(balance)-float(balance)*(essai/100)} ETH")
        break
    time.sleep(10)  

print('tt est bon')
