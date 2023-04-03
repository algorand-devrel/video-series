   # algod_address = "http://hackathon.algodev.network:9100"
   # algod_token = "ef920e2e7e002953f4b29a8af720efe8e4ecc75ff102b165e0472834b25832c1"
import json
from algosdk import mnemonic
from algosdk.v2client import algod
from algosdk.transaction import *


def getting_started_example():
    algod_address = "http://localhost:4001"
    algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    algod_client = algod.AlgodClient(algod_token, algod_address)

# Part 1
# rekey Account 3 to allow it to sign from Account 1

# Part 2
# send from account 3 to account 2 and sign from Account 1
# to run: change all three account passphrases - no need to fund account 1 and 2
# never use mnemonics in production code, replace for demo purposes only

    account1_passphrase = "resource immune vintage come distance learn best merge defy roof inflict gift believe seek pull multiply unit credit mammal field essay useful problem abandon level"
    account2_passphrase = "joke click surge skate grocery treat juice consider thrive ship record fault cotton safe remind wasp bomb maid february couple fix dune route abandon tackle"
    account3_passphrase = "sphere million erupt curious around earth client name question loyal client tree dentist reform wheat tattoo patch bounce hockey spy because opinion nest abstract aware"
    
    #  no need to fund account 1 and 2   
    account1 = mnemonic.to_public_key(account1_passphrase)
    account2 = mnemonic.to_public_key(account2_passphrase)    
    #  account 3 needs to be funded
    account3 = mnemonic.to_public_key(account3_passphrase)
    print("Starting account balances")
    print_accounts(algod_client, account1, account2, account3)
    # Part 1
    # build transaction
    params = algod_client.suggested_params()

    # opt-in send tx to same address as sender and use 0 for amount w rekey account
    # set to account 1
    amount = int(0)   
    rekeyaccount = account1
    sender = account3
    receiver = account3    
    unsigned_txn = PaymentTxn(
    	sender, params, receiver, amount, None, None, None, rekeyaccount)

    # sign transaction with account 3
    signed_txn = unsigned_txn.sign(
    	mnemonic.to_private_key(account3_passphrase))
    txid = algod_client.send_transaction(signed_txn)
    print("Signed transaction with txID: {}".format(txid))

    # wait for confirmation

    confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))

    # read transction
    try:
        confirmed_txn = algod_client.pending_transaction_info(txid)
        
    except Exception as err:
        print(err)
    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
    print("After Opt-in account balances")
    print_accounts(algod_client, account1, account2, account3)


    #  Part 2
    #  send payment from account 3
    #  to acct 2 and signed by account 1


    amount = int(100000)
    receiver = account2
    closeto= "HZ57J3K46JIJXILONBBZOHX6BKPXEM2VVXNRFSUED6DKFD5ZD24PMJ3MVA"
    unsigned_txn = PaymentTxn(
    	account3, params, receiver, amount, closeto, None, None, account1)
    # sign transaction
    signed_txn = unsigned_txn.sign(
    	mnemonic.to_private_key(account1_passphrase))
    txid = algod_client.send_transaction(signed_txn)
    print("Signed transaction with txID: {}".format(txid))

    # wait for confirmation

    confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))
    print("Transaction information signed by rekey account: {}".format(
    json.dumps(confirmed_txn, indent=4)))
    print("Final account balances")
    print_accounts(algod_client, account1, account2, account3)

def print_accounts(algod_client, account1, account2, account3):
    account_info = algod_client.account_info(account1)
    print("Account 1 : {}".format(account1))    
    print("Balance: {} microAlgos".format(account_info.get('amount')) )
  
    account_info = algod_client.account_info(account2)
    print("Account 2 : {}".format(account2))  
    print("Balance: {} microAlgos".format(account_info.get('amount')) )  

    account_info = algod_client.account_info(account3)
    print("Account 3 : {}".format(account3))   
    print("Balance: {} microAlgos".format(account_info.get('amount')) )

getting_started_example()
