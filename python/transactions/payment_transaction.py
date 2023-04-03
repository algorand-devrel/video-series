import json

import base64
from algosdk import account
from algosdk import mnemonic
from algosdk.v2client import algod
from algosdk.future.transaction import *


def getting_started_example():
    algod_address = "http://localhost:4001"
    # algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    # algod_client = algod.AlgodClient(algod_token, algod_address)
    algod_address = "http://hackathon.algodev.network:9100"
    algod_token = "ef920e2e7e002953f4b29a8af720efe8e4ecc75ff102b165e0472834b25832c1"

    algod_client = algod.AlgodClient(algod_token, algod_address)

    # algod_token = 'WpYvadV1w53mSODr6Xrq77tw0ODcgHAx9iJBn5tb'
    # algod_address = 'https://testnet-algorand.api.purestake.io/ps2'
    # purestake_token = {'X-Api-key': algod_token}
    # algod_client = algod.AlgodClient(algod_token, algod_address, headers=purestake_token)

    passphrase = "price clap dilemma swim genius fame lucky crack torch hunt maid palace ladder unlock symptom rubber scale load acoustic drop oval cabbage review abstract embark"

    # generate a public/private key pair
    secret_key = mnemonic.to_private_key(passphrase)
    my_address = mnemonic.to_public_key(passphrase)

    print("My address: {}".format(my_address))

    # Generate new account for this transaction
    # secret_key, my_address = account.generate_account()
    # fund it at dispenser https://dispenser.testnet.aws.algodev.network/

    print("My address: {}".format(my_address))
    account_info = algod_client.account_info(my_address)
    print("Account balance: {} microAlgos".format(account_info.get('amount')))

    # build transaction
    params = algod_client.suggested_params()
    # comment out the next two (2) lines to use suggested fees
    # params.flat_fee = True
    # params.fee = 1000
    receiver = "GD64YIY3TWGDMCNPP553DZPPR6LDUSFQOIJVFDPPXWEG3FVOJCCDBBHU5A"
    note = "Hello World".encode()

    unsigned_txn = PaymentTxn(my_address, params, receiver, 100000, None, note)

    # sign transaction
    signed_txn = unsigned_txn.sign(secret_key)
    # signed_txn = unsigned_txn.sign(mnemonic.to_private_key(passphrase))


# wait for confirmation
    try:
        txid = algod_client.send_transaction(signed_txn)
        print("Signed transaction with txID: {}".format(txid))
        confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
        print("txID: {}".format(txid), " confirmed in round: {}".format(
            confirmed_txn.get("confirmed-round", 0)))

    except Exception as err:
        print(err)
        return

    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
    print("Decoded note: {}".format(base64.b64decode(
        confirmed_txn["txn"]["txn"]["note"]).decode()))


getting_started_example()
