import json
from algosdk import account, mnemonic, transaction
from algosdk.v2client import algod

from sandbox import get_accounts


# # This is a complete code example that:
# #   1. Create a new account
# #   2. Fund your created account from another one


def create_account():
    # Change algod_token and algod_address to connect to a different client
    algod_address = "http://localhost:4001"
    algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    algod_client = algod.AlgodClient(algod_token, algod_address)

    fund_addr, fund_sk = get_accounts().pop()
    # Generate new account for this transaction
    my_secret_key, my_address = account.generate_account()

    print("My address: {}".format(my_address))
    print("My private key: {}".format(my_secret_key))
    print("My mnemonic: {}".format(mnemonic.from_private_key(my_secret_key)))
    # Check your balance. It should be 0 microAlgos

    account_info = algod_client.account_info(my_address)
    print("Account balance: {} microAlgos".format(account_info.get("amount")) + "\n")

    # build transaction
    print("Building transaction")
    params = algod_client.suggested_params()

    amount = 1000000
    unsigned_txn = transaction.PaymentTxn(fund_addr, params, my_address, amount)

    # sign transaction
    print("Signing transaction")
    signed_txn = unsigned_txn.sign(fund_sk)
    print("Sending transaction")
    txid = algod_client.send_transaction(signed_txn)
    print("Transaction Info:")
    print("Signed transaction with txID: {}".format(txid))

    # wait for confirmation
    try:
        print("Waiting for confirmation")
        confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4)
    except Exception as err:
        print(err)
        return
    print(
        "txID: {}".format(txid),
        " confirmed in round: {}".format(confirmed_txn.get("confirmed-round", 0)),
    )
    print("Transaction information: {}".format(json.dumps(confirmed_txn, indent=4)))

    print("Starting Account balance: {} microAlgos".format(account_info.get("amount")))
    print("Amount transfered: {} microAlgos".format(amount))
    return mnemonic.from_private_key(my_secret_key)


create_account()
