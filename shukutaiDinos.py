from math import floor
from PIL import Image
import requests
import datetime
from arweave import Wallet, Transaction
from arweave.transaction_uploader import get_uploader
import time
import os
import json
import base58
from solana.keypair import Keypair
from solana.publickey import PublicKey
from cryptography.fernet import Fernet
import api.metaplex_api as metaplex_api
import random

def shukutaiMintEgg(walletID, amount, finalPercent):
    for i in range(amount):
        rarityList = {
            "Common": "https://arweave.net/lMd-rSSzHFcuFz6w-4KoeNFDr2_uKW0Yo3uEztI-Eak?ext=json",
            "Uncommon": "https://arweave.net/JtN-WSEMUQGHVpsCA6BSM55G2VeHzsGPo0fZtu49NGQ?ext=json",
            "Rare": "https://arweave.net/lfxw2MeeguAD2ft5wRALTFDKEZPfgV3WPZvp3sVuyTU?ext=json",
            "Legendary": "https://arweave.net/kgCvY7jiVdYWoVKqLBujtOzYBENFRJJqIvafSCKXfiw?ext=json",
        }
        weightsTuple = (finalPercent[0], finalPercent[1], finalPercent[2], finalPercent[3])
        randomRarity = random.choices(["Common", "Uncommon", "Rare", "Legendary"], weights=weightsTuple, k=1)[0]
        arweaveURL = rarityList[randomRarity]

        text_file = open("./SHUKUTAIKEYPAIR.json", "r")
        lines = text_file.read()[1:-1].split(',')
        key_from_file = [int(x) for x in lines]
        keypair = Keypair(key_from_file[:32])
        pubKey = PublicKey(walletID)
        cfg = {
            "PRIVATE_KEY": base58.b58encode(keypair.seed).decode("ascii"),
            "PUBLIC_KEY": str(keypair.public_key),
            "DECRYPTION_KEY": Fernet.generate_key().decode("ascii"),
        }
        api = metaplex_api.MetaplexAPI(cfg)
        api_endpoint = "RPC URL"
        print("Endpoint set to " + api_endpoint)
        result = api.deploy(api_endpoint, "Shukutai Dino Egg", "SHUK", fees=700)

        resultJSON = json.loads(result)
        finalized = False
        urlConfirm = "BACK END TO CHECK TRANSACTION CONFIRMATIONS HERE" 
        headersConfirm = {'content-type': 'application/json'}
        myobjConfirm = {'tx': resultJSON["result"]}
        confirmations = requests.post(urlConfirm, data=json.dumps(myobjConfirm), headers=headersConfirm)
        confirmations = confirmations.json()
        if "blockTime" in confirmations.keys():
            finalized = True
            print("Deploy completed. Result: ", result)
        while finalized is not True:
            result = api.deploy(api_endpoint, "Shukutai Dino Egg", "SHUK", fees=700)
            resultJSON = json.loads(result)
            myobjConfirm = {'tx': resultJSON["result"]}
            confirmations = requests.post(urlConfirm, data=json.dumps(myobjConfirm), headers=headersConfirm)
            confirmations = confirmations.json()
            if "blockTime" in confirmations.keys():
                finalized = True
                print("Deploy completed. Result: ", result)

        contract_key = json.loads(result).get('contract')
        print("Mint Complete. Mint ID: ", contract_key)
        # conduct a mint, and send to a recipient, e.g. wallet_2
        mint_res = api.mint(api_endpoint, contract_key, pubKey, arweaveURL)
        print("Mint completed. Result: %s", mint_res)


shukutaiMintEgg()
