import json
import base64
import hashlib
from algosdk import mnemonic
from algosdk.v2client import algod
from algosdk.future.transaction import AssetConfigTxn, AssetTransferTxn, PaymentTxn, wait_for_confirmation
from create_account import create_account
from closeout_account import closeout_account
from create_asset import create_asset

# Using Rand Labs Developer API
# see https://github.com/algorand/py-algorand-sdk/issues/169
# Change algod_token and algod_address to connect to a different client
algod_token = "2f3203f21e738a1de6110eba6984f9d03e5a95d7a577b34616854064cf2c0e7b"
algod_address = "https://academy-algod.dev.aws.algodev.network/"
algod_client = algod.AlgodClient(algod_token, algod_address)

def create_fund_accounts():
  # For ease of reference, add account public and private keys to an accounts dict.
  print("--------------------------------------------")
  print("Creating Alice and Bob's accounts...")
  mnemonics = []
  mnemonics.append(create_account())
  mnemonics.append(create_account(False))
  
  accounts = {}
  counter = 0
  for m in mnemonics:
    accounts[counter] = {}
    accounts[counter]['pk'] = mnemonic.to_public_key(m)
    accounts[counter]['sk'] = mnemonic.to_private_key(m)
    counter += 1
  
  return accounts

def transferAlgosToBob(algod_client, bob, alice):
  print("--------------------------------------------")
  print("Transfering Algos to Bob....")
  account_info = algod_client.account_info(bob["pk"])
  print("Account balance: {} microAlgos".format(account_info.get('amount')) + "\n")

  # build transaction 
  params = algod_client.suggested_params()
  # comment out the next two (2) lines to use suggested fees
  # params.flat_fee = True
  # params.fee = 1000

  # minimum balance 100000, plus 100000 for asset optin,
  # plus 3000 for 3 tx (optin, transfer, algo closeout) = 203000 microalgos
  # amount = 203000;
  unsigned_txn = PaymentTxn(alice["pk"], params, bob["pk"], 203000)    

  # sign transaction
  signed_txn = unsigned_txn.sign(alice['sk'])

  #submit transaction
  txid = algod_client.send_transaction(signed_txn)
  print("Successfully sent transaction with txID: {}".format(txid))

  # wait for confirmation 
  try:
      confirmed_txn = wait_for_confirmation(algod_client, txid, 4)  
      print("TXID: ", txid)
      print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))
      
  except Exception as err:
      print(err)
      return

  print("Transaction information: {}".format(
      json.dumps(confirmed_txn, indent=4)))
  
  account_info = algod_client.account_info(bob["pk"])
  print("Account balance: {} microAlgos".format(account_info.get('amount')) + "\n")

def optIn(algod_client, bob, asset_id):
  print("--------------------------------------------")
  print("Opt-in for Alice's token......")
  # Check if asset_id is in Bob's asset holdings prior
  # to opt-in
  params = algod_client.suggested_params()
  # comment these two lines if you want to use suggested params
  # params.fee = 1000
  # params.flat_fee = True

  account_info = algod_client.account_info(bob['pk'])
  holding = None
  idx = 0
  for my_account_info in account_info['assets']:
      scrutinized_asset = account_info['assets'][idx]
      idx = idx + 1    
      if (scrutinized_asset['asset-id'] == asset_id):
          holding = True
          break

  if not holding:
    # Use the AssetTransferTxn class to transfer assets and opt-in
    txn = AssetTransferTxn(
        sender=bob['pk'],
        sp=params,
        receiver=bob["pk"],
        amt=0,
        index=asset_id)
    stxn = txn.sign(bob['sk'])
    txid = algod_client.send_transaction(stxn)
    print(txid)
    # Wait for the transaction to be confirmed
    confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))
    # Now check the asset holding for that account.
    # This should now show a holding with a balance of 0.
    print_asset_holding(algod_client, bob['pk'], asset_id)

def transferAssets(algod_client, alice, bob, asset_id):
  print("--------------------------------------------")
  print("Transfering Alice's token to Bob......")
  params = algod_client.suggested_params()
  # comment these two lines if you want to use suggested params
  # params.fee = 1000
  # params.flat_fee = True
  txn = AssetTransferTxn(
      sender=alice['pk'],
      sp=params,
      receiver=bob["pk"],
      amt=100,
      index=asset_id)
  stxn = txn.sign(alice['sk'])
  txid = algod_client.send_transaction(stxn)
  print(txid)
  # Wait for the transaction to be confirmed
  confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
  print("TXID: ", txid)
  print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))
  # The balance should now be 10.
  print_asset_holding(algod_client, bob['pk'], asset_id)

def transferAssetsBack(algod_client, bob, alice, asset_id):
  print("--------------------------------------------")
  print("Transfering Alice's token back to Alice......")
  params = algod_client.suggested_params()
  # comment these two lines if you want to use suggested params
  # params.fee = 1000
  # params.flat_fee = True
  txn = AssetTransferTxn(
      sender=bob['pk'],
      sp=params,
      receiver=alice["pk"],
      amt=100,
      close_assets_to=alice["pk"],
      index=asset_id)
  stxn = txn.sign(bob['sk'])
  txid = algod_client.send_transaction(stxn)
  print(txid)
  # Wait for the transaction to be confirmed
  confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
  print("TXID: ", txid)
  print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))
  # The balance should now be 10.
  print_asset_holding(algod_client, alice['pk'], asset_id)

def destroyAsset(algod_client, alice, asset_id):
  print("--------------------------------------------")
  print("Destroying Alice's token......")
  params = algod_client.suggested_params()
  # comment these two lines if you want to use suggested params
  # params.fee = 1000
  # params.flat_fee = True

  # Asset destroy transaction
  txn = AssetConfigTxn(
      sender=alice['pk'],
      sp=params,
      index=asset_id,
      strict_empty_address_check=False
      )

  # Sign with secret key of creator
  stxn = txn.sign(alice['sk'])
  # Send the transaction to the network and retrieve the txid.
  txid = algod_client.send_transaction(stxn)
  print(txid)
  # Wait for the transaction to be confirmed
  confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
  print("TXID: ", txid)
  print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))
  print("Alice's Token is destroyed.")



#   Utility function used to print created asset for account and assetid
def print_created_asset(algodclient, account, assetid):
  # note: if you have an indexer instance available it is easier to just use this
  # response = myindexer.accounts(asset_id = assetid)
  # then use 'account_info['created-assets'][0] to get info on the created asset
  account_info = algodclient.account_info(account)
  idx = 0;
  for my_account_info in account_info['created-assets']:
    scrutinized_asset = account_info['created-assets'][idx]
    idx = idx + 1       
    if (scrutinized_asset['index'] == assetid):
      print("Asset ID: {}".format(scrutinized_asset['index']))
      print(json.dumps(my_account_info['params'], indent=4))
      break

#   Utility function used to print asset holding for account and assetid
def print_asset_holding(algodclient, account, assetid):
    # note: if you have an indexer instance available it is easier to just use this
    # response = myindexer.accounts(asset_id = assetid)
    # then loop thru the accounts returned and match the account you are looking for
    account_info = algodclient.account_info(account)
    idx = 0
    for my_account_info in account_info['assets']:
        scrutinized_asset = account_info['assets'][idx]
        idx = idx + 1        
        if (scrutinized_asset['asset-id'] == assetid):
            print("Asset ID: {}".format(scrutinized_asset['asset-id']))
            print(json.dumps(scrutinized_asset, indent=4))
            break

# accounts[0] = Alice, accounts[1] = Bob
accounts = create_fund_accounts()
alice = accounts[0]
bob = accounts[1]

# Alice creates Asset - AssetConfigTxn
asset_id = create_asset(alice)  

# Alice transfers Algos to Bob - PaymentTxn     
transferAlgosToBob(algod_client, bob, alice)

# Bob Opts in order to receive Asset - AssetTransferTxn
optIn(algod_client, bob, asset_id)

# Alice transfers Asset to Bob - AssetTransferTxn
transferAssets(algod_client, alice, bob, asset_id)

# Bob transfers Asset back to Alice - AssetTransferTxn
transferAssetsBack(algod_client, bob, alice, asset_id)

# Alice Destroys Asset - AssetConfigTxn
destroyAsset(algod_client, alice, asset_id)

# Alice Closes account using closeout parameter - PaymentTxn
closeout_account(algod_client, alice)

# Bob Closes account using closeout parameter - PaymentTxn
closeout_account(algod_client, bob)

