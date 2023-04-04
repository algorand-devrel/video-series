import json
import base64

from algosdk import account, mnemonic, transaction
from algosdk.v2client import algod

from sandbox import get_accounts


def getting_started_example():
    algod_address = "http://localhost:4001"
    algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    algod_client = algod.AlgodClient(algod_token, algod_address)

    # generate a public/private key pair
    secret_key, addr = account.generate_account()

    print(f"My address: {addr}")
    print(f"My mnemonic: {mnemonic.from_private_key(secret_key)}")

    account_info = algod_client.account_info(addr)
    print("Account balance: {} microAlgos".format(account_info.get("amount")))

    # fund account
    fund_addr, fund_sk = get_accounts().pop()
    ptxn = transaction.PaymentTxn(
        fund_addr, algod_client.suggested_params(), addr, int(1e8)
    )
    txid = algod_client.send_transaction(ptxn.sign(fund_sk))
    transaction.wait_for_confirmation(algod_client, txid, 4)

    # build transaction
    params = algod_client.suggested_params()
    note = "Hello World".encode()

    # we're paying back the original funding address
    unsigned_txn = transaction.PaymentTxn(addr, params, fund_addr, 100000, None, note)

    # sign transaction
    signed_txn = unsigned_txn.sign(secret_key)

    # wait for confirmation
    try:
        txid = algod_client.send_transaction(signed_txn)
        print("Signed transaction with txID: {}".format(txid))
        confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4)
        print(
            "txID: {}".format(txid),
            " confirmed in round: {}".format(confirmed_txn.get("confirmed-round", 0)),
        )

    except Exception as err:
        print(err)
        return

    print("Transaction information: {}".format(json.dumps(confirmed_txn, indent=4)))
    print(
        "Decoded note: {}".format(
            base64.b64decode(confirmed_txn["txn"]["txn"]["note"]).decode()
        )
    )


getting_started_example()
