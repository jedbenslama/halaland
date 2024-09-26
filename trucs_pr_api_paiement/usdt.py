from litecoinutils.keys import PrivateKey as PrivateKeyLTC
from litecoinutils.keys import P2pkhAddress
from litecoinutils.transactions import Transaction, TxInput, TxOutput
from litecoinutils.script import Script
from litecoinutils.setup import setup
from litecoinutils.utils import to_satoshis
import asyncio
from bit import PrivateKey
from bit.network import NetworkAPI
import aiohttp
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, ConversationHandler, CallbackQueryHandler, filters
from tinydb import TinyDB, Query
from telegram.constants import ParseMode
from web3 import Web3
from urllib.parse import quote
import urllib, threading
import requests, json, time, hashlib, hmac,secrets, string, random
from datetime import datetime, timedelta,timezone
import logging, asyncio, os
import concurrent.futures
from eth_account import Account


print("debut")
infura_url = "https://mainnet.infura.io/v3/7118aac17ed44460928e59919b048294"
web3 = Web3(Web3.HTTPProvider(infura_url))
usdt_contract_address = Web3.to_checksum_address("0xdAC17F958D2ee523a2206206994597C13D831ec7") #TOUCHE PAS A CETTE ADRESSE C CELLE DU CONTRACT USDT SUR LE RESEAU ETH
destination_address = Web3.to_checksum_address("0x137512fD7CE8e6A841859227B674bF186D811D80")
usdt_abi = '''
[
    {
        "constant": true,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [
            {"name": "_to", "type": "address"},
            {"name": "_value", "type": "uint256"}
        ],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "type": "function"
    }
]
'''
wallet = Account.create()
def check_and_transfer_usdt(wallet):
    if web3.is_connected():
        print("Connecté")
    else:
        print("ENLEVE LE VPN BROW")
        quit(69)
    print(f"Adresse du wallet temporaire: {wallet.address}")
    usdt_contract = web3.eth.contract(address=usdt_contract_address, abi=usdt_abi)
    def transfer_usdt_to_destination(wallet, amount):
        tx = usdt_contract.functions.transfer(destination_address, amount).build_transaction({'from': wallet.address,'nonce': web3.eth.get_transaction_count(wallet.address),'gas': 200000,'gasPrice': web3.eth.gas_price})
        signed_tx = web3.eth.account.sign_transaction(tx, wallet.key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"Transaction: {web3.to_hex(tx_hash)}")
    while True:
        balance = usdt_contract.functions.balanceOf(wallet.address).call()
        print(f"Attend l'USDT, balance: {balance}")
        if balance > 0:
            print(f"USDT reçu: {balance / 10**6} USDT")
            for essai in range(100):
                try: 
                    transfer_usdt_to_destination(wallet, float(balance) - float(balance) * (essai / 100))
                    paymentdone=True
                    break
                except Exception as e:
                    print(f"Fail {float(balance) - float(balance) * (essai / 100)} ETH, Erreur: {e}")
                    paymentdone=False
            break
        time.sleep(10)
    print(f"payment done: {paymentdone}")
    print("fin")
check_and_transfer_usdt(wallet)