import json
from algosdk.v2client import algod
from algosdk import transaction
from sandbox import get_accounts

accts = get_accounts()

accounts = []
for a in accts:
    accounts.append({"pk": a[0], "sk": a[1]})


print("Account 1 address: {}".format(accounts[0]["pk"]))
print("Account 2 address: {}".format(accounts[1]["pk"]))
print("Account 3 address: {}".format(accounts[2]["pk"]))


algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
algod_client = algod.AlgodClient(algod_token=algod_token, algod_address=algod_address)


def print_created_asset(algodclient: algod.AlgodClient, addr: str, assetid: int):
    """Utility function used to print created asset for account and assetid"""

    account_info = algodclient.account_info(addr)
    idx = 0
    for my_account_info in account_info["created-assets"]:
        scrutinized_asset = account_info["created-assets"][idx]
        idx = idx + 1
        if scrutinized_asset["index"] == assetid:
            print("Asset ID: {}".format(scrutinized_asset["index"]))
            print(json.dumps(my_account_info["params"], indent=4))
            break


def print_asset_holding(algodclient: algod.AlgodClient, addr: str, assetid: int):
    """Utility function used to print asset holding for account and assetid"""

    # note: if you have an indexer instance available it is easier to just use this
    # response = myindexer.accounts(asset_id = assetid)
    # then loop thru the accounts returned and match the account you are looking for
    account_info = algodclient.account_info(addr)
    idx = 0
    for my_account_info in account_info["assets"]:
        scrutinized_asset = account_info["assets"][idx]
        idx = idx + 1
        if scrutinized_asset["asset-id"] == assetid:
            print("Asset ID: {}".format(scrutinized_asset["asset-id"]))
            print(json.dumps(scrutinized_asset, indent=4))
            break


# CREATE ASSET
# Get network params for transactions before every transaction.
params = algod_client.suggested_params()

# Account 1 creates an asset called latinum and
# sets Account 2 as the manager, reserve, freeze, and clawback address.
# Asset Creation transaction
txn = transaction.AssetConfigTxn(
    sender=accounts[0]["pk"],
    sp=params,
    total=1000,
    default_frozen=False,
    unit_name="LATINUM",
    asset_name="latinum",
    manager=accounts[1]["pk"],
    reserve=accounts[1]["pk"],
    freeze=accounts[1]["pk"],
    clawback=accounts[1]["pk"],
    url="https://path/to/my/asset/details",
    decimals=0,
)
# Sign with secret key of creator
stxn = txn.sign(accounts[0]["sk"])

# Send the transaction to the network and retrieve the txid.
try:
    txid = algod_client.send_transaction(stxn)
    print("Signed transaction with txID: {}".format(txid))
    # Wait for the transaction to be confirmed
    confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4)
    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn["confirmed-round"]))
    print("Transaction information: {}".format(json.dumps(confirmed_txn, indent=4)))
except Exception as err:
    print(err)
# Retrieve the asset ID of the newly created asset by first
# ensuring that the creation transaction was confirmed,
# then grabbing the asset id from the transaction.


try:
    # Pull account info for the creator
    # account_info = algod_client.account_info(accounts[1]['pk'])
    # get asset_id from tx
    # Get the new asset's information from the creator account
    ptx = algod_client.pending_transaction_info(txid)
    asset_id = ptx["asset-index"]
    print_created_asset(algod_client, accounts[0]["pk"], asset_id)
    print_asset_holding(algod_client, accounts[0]["pk"], asset_id)
except Exception as e:
    print(e)

# CHANGE MANAGER

# The current manager(Account 2) issues an asset configuration transaction that
# assigns Account 1 as the new manager.
# Keep reserve, freeze, and clawback address same as before, i.e. account 2
params = algod_client.suggested_params()

txn = transaction.AssetConfigTxn(
    sender=accounts[1]["pk"],
    sp=params,
    index=asset_id,
    manager=accounts[0]["pk"],
    reserve=accounts[1]["pk"],
    freeze=accounts[1]["pk"],
    clawback=accounts[1]["pk"],
)
# sign by the current manager - Account 2
stxn = txn.sign(accounts[1]["sk"])

# Wait for the transaction to be confirmed
# Send the transaction to the network and retrieve the txid.
try:
    txid = algod_client.send_transaction(stxn)
    print("Signed transaction with txID: {}".format(txid))
    # Wait for the transaction to be confirmed
    confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4)
    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn["confirmed-round"]))

except Exception as err:
    print(err)
# Check asset info to view change in management. manager should now be account 1
print_created_asset(algod_client, accounts[0]["pk"], asset_id)

# OPT-IN

# Check if asset_id is in account 3's asset holdings prior
# to opt-in
params = algod_client.suggested_params()

account_info = algod_client.account_info(accounts[2]["pk"])
holding = None
idx = 0
for my_account_info in account_info["assets"]:
    scrutinized_asset = account_info["assets"][idx]
    idx = idx + 1
    if scrutinized_asset["asset-id"] == asset_id:
        holding = True
        break

if not holding:
    # Use the AssetTransferTxn class to transfer assets and opt-in
    txn = transaction.AssetTransferTxn(
        sender=accounts[2]["pk"],
        sp=params,
        receiver=accounts[2]["pk"],
        amt=0,
        index=asset_id,
    )
    stxn = txn.sign(accounts[2]["sk"])
    # Send the transaction to the network and retrieve the txid.
    try:
        txid = algod_client.send_transaction(stxn)
        print("Signed transaction with txID: {}".format(txid))
        # Wait for the transaction to be confirmed
        confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4)
        print("TXID: ", txid)
        print("Result confirmed in round: {}".format(confirmed_txn["confirmed-round"]))

    except Exception as err:
        print(err)
    # Now check the asset holding for that account.
    # This should now show a holding with a balance of 0.
    print_asset_holding(algod_client, accounts[2]["pk"], asset_id)


# TRANSFER ASSET

# transfer asset of 10 from account 1 to account 3
params = algod_client.suggested_params()
txn = transaction.AssetTransferTxn(
    sender=accounts[0]["pk"],
    sp=params,
    receiver=accounts[2]["pk"],
    amt=10,
    index=asset_id,
)
stxn = txn.sign(accounts[0]["sk"])
# Send the transaction to the network and retrieve the txid.
try:
    txid = algod_client.send_transaction(stxn)
    print("Signed transaction with txID: {}".format(txid))
    # Wait for the transaction to be confirmed
    confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4)
    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn["confirmed-round"]))

except Exception as err:
    print(err)
# The balance should now be 10.
print_asset_holding(algod_client, accounts[2]["pk"], asset_id)


# FREEZE ASSET

params = algod_client.suggested_params()

# The freeze address (Account 2) freezes Account 3's latinum holdings.
txn = transaction.AssetFreezeTxn(
    sender=accounts[1]["pk"],
    sp=params,
    index=asset_id,
    target=accounts[2]["pk"],
    new_freeze_state=True,
)
stxn = txn.sign(accounts[1]["sk"])
# Send the transaction to the network and retrieve the txid.
try:
    txid = algod_client.send_transaction(stxn)
    print("Signed transaction with txID: {}".format(txid))
    # Wait for the transaction to be confirmed
    confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4)
    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn["confirmed-round"]))
except Exception as err:
    print(err)
# The balance should now be 10 with frozen set to true.
print_asset_holding(algod_client, accounts[2]["pk"], asset_id)


# REVOKE ASSET

# The clawback address (Account 2) revokes 10 latinum from Account 3 and places it back with Account 1.
params = algod_client.suggested_params()

# Must be signed by the account that is the Asset's clawback address
txn = transaction.AssetTransferTxn(
    sender=accounts[1]["pk"],
    sp=params,
    receiver=accounts[0]["pk"],
    amt=10,
    index=asset_id,
    revocation_target=accounts[2]["pk"],
)
stxn = txn.sign(accounts[1]["sk"])
# Send the transaction to the network and retrieve the txid.
try:
    txid = algod_client.send_transaction(stxn)
    print("Signed transaction with txID: {}".format(txid))
    # Wait for the transaction to be confirmed
    confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4)
    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn["confirmed-round"]))
except Exception as err:
    print(err)
# The balance of account 3 should now be 0.
print("Account 3")
print_asset_holding(algod_client, accounts[2]["pk"], asset_id)

# The balance of account 1 should increase by 10 to 1000.
print("Account 1")
print_asset_holding(algod_client, accounts[0]["pk"], asset_id)


# DESTROY ASSET
# With all assets back in the creator's account,
# the manager (Account 1) destroys the asset.
params = algod_client.suggested_params()

# Asset destroy transaction
txn = transaction.AssetConfigTxn(
    sender=accounts[0]["pk"],
    sp=params,
    index=asset_id,
    strict_empty_address_check=False,
)

# Sign with secret key of creator
stxn = txn.sign(accounts[0]["sk"])
# Send the transaction to the network and retrieve the txid.
# Send the transaction to the network and retrieve the txid.
try:
    txid = algod_client.send_transaction(stxn)
    print("Signed transaction with txID: {}".format(txid))
    # Wait for the transaction to be confirmed
    confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4)
    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn["confirmed-round"]))
except Exception as err:
    print(err)

# Asset was deleted.
try:
    print("Account 3 must do a transaction for an amount of 0, ")
    print(
        "with a close_assets_to to the creator account, to clear it from its accountholdings"
    )
    print(
        "For Account 1, nothing should print after this as the asset is destroyed on the creator account"
    )

    print_asset_holding(algod_client, accounts[0]["pk"], asset_id)
    print_created_asset(algod_client, accounts[0]["pk"], asset_id)
except Exception as e:
    print(e)
