from litecoinutils.keys import PrivateKey as PrivateKeyLTC
from litecoinutils.keys import P2pkhAddress
from litecoinutils.transactions import Transaction, TxInput, TxOutput
from litecoinutils.script import Script
from litecoinutils.setup import setup
from litecoinutils.utils import to_satoshis
import requests
import time

setup('mainnet')
priv = PrivateKeyLTC()
wif = priv.to_wif()
print('Private Key (WIF):', wif)
pub = priv.get_public_key()
address = pub.get_address()
address_str = address.to_string()

def send_litecoin(priv, wif, pub, address, address_str):
    blockcypher_token = '606539f2d6aa47b0b33c2ef55e06163d'
    print('Litecoin Address:', address_str)
    
    url_balance = f'https://api.blockcypher.com/v1/ltc/main/addrs/{address_str}/balance?token={blockcypher_token}'
    print('Waiting for incoming transaction to address:', address_str)
    
    while True:
        response = requests.get(url_balance)
        data = response.json()
        balance = data['final_balance']
        if balance > 0:
            print('Received funds:', balance, 'litoshis')
            break
        else:
            print('No funds received yet. Checking again in 10 seconds...')
            time.sleep(10)
    
    url_utxos = f'https://api.blockcypher.com/v1/ltc/main/addrs/{address_str}?unspentOnly=true&includeScript=true&token={blockcypher_token}'
    response = requests.get(url_utxos)
    utxo_data = response.json()
    
    utxos = utxo_data.get('txrefs', [])
    if not utxos:
        print('No UTXOs found!')
        return
    
    inputs = []
    total_input = 0
    for utxo in utxos:
        txid = utxo['tx_hash']
        vout = utxo['tx_output_n']
        value = utxo['value']
        total_input += value
        txin = TxInput(txid, vout)
        inputs.append(txin)
    
    print('Total input amount:', total_input, 'litoshis')
    fee = 100000
    amount_to_send = total_input - fee
    
    if amount_to_send <= 0:
        print('Amount to send is less than or equal to zero after subtracting fees!')
        return
    
    destination_address_str = 'LKuXRfxUVG33BkEA2kBkgLUoK9p2BYY391'
    destination_address = P2pkhAddress(destination_address_str)
    txout = TxOutput(amount_to_send, destination_address.to_script_pub_key())
    tx = Transaction(inputs, [txout])
    
    for i, txin in enumerate(tx.inputs):
        sig = priv.sign_input(tx, i, address.to_script_pub_key())
        txin.script_sig = Script([sig, pub.to_hex()])
    
    raw_tx = tx.serialize()
    print('Raw Transaction:', raw_tx)
    
    url_push = f'https://api.blockcypher.com/v1/ltc/main/txs/push?token={blockcypher_token}'
    data = {'tx': raw_tx}
    response = requests.post(url_push, json=data)
    
    if response.status_code in [200, 201]:
        print('Transaction sent successfully!')
        tx_hash = response.json().get('tx', {}).get('hash')
        print('Transaction Hash:', tx_hash)
    else:
        print('Error sending transaction:')
        print(response.text())

# Call the function to send Litecoin
send_litecoin(priv, wif, pub, address, address_str)
