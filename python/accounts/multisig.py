# algod_address = "http://localhost:8080"
# algod_token = "8024065d94521d253181cff008c44fa4ae4bdf44f028834cd4b4769a26282de1"
# algod_address = "http://hackathon.algodev.network:9100"
# algod_token = "ef920e2e7e002953f4b29a8af720efe8e4ecc75ff102b165e0472834b25832c1"
import json
from algosdk.v2client import algod
from algosdk import account, encoding, mnemonic
from algosdk.future.transaction import Multisig, PaymentTxn, MultisigTransaction
import base64
from algosdk.future.transaction import *

# Change these values with mnemonics
# mnemonic1 = "PASTE phrase for account 1"
# mnemonic2 = "PASTE phrase for account 2"
# mnemonic3 = "PASTE phrase for account 3"

# never use mnemonics in production code, this is for demo purposes only

mnemonic1 = "patrol target joy dial ethics flip usual fatigue bulb security prosper brand coast arch casino burger inch cricket scissors shoe evolve eternal calm absorb school"
mnemonic2 = "genius inside turtle lock alone blame parent civil depend dinosaur tag fiction fun skill chief use damp daughter expose pioneer today weasel box about silly"
mnemonic3 = "off canyon mystery cable pluck emotion manual legal journey grit lunch include friend social monkey approve lava steel school mango auto cactus huge ability basket"

# For ease of reference, add account public and private keys to
# an accounts dict.

private_key_1 = mnemonic.to_private_key(mnemonic1)
account_1 = mnemonic.to_public_key(mnemonic1)

private_key_2 = mnemonic.to_private_key(mnemonic2)
account_2 = mnemonic.to_public_key(mnemonic2)

private_key_3 = mnemonic.to_private_key(mnemonic3)
account_3 = mnemonic.to_public_key(mnemonic3)
print("Account 1 Address: ", account_1)
print("Account 2 Address: ", account_2)
print("Account 3 Address: ", account_3)

# create a multisig account
version = 1  # multisig version
threshold = 2  # how many signatures are necessary
msig = Multisig(version, threshold, [account_1, account_2])

print("Multisig Address: ", msig.address())
print('Go to the below link to fund the created account using testnet faucet: \n https://dispenser.testnet.aws.algodev.network/?account={}'.format(msig.address())) 

input("Press Enter to continue...")

# Specify your node address and token. This must be updated.
# algod_address = ""  # ADD ADDRESS
# algod_token = ""  # ADD TOKEN

# sandbox
algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"


# Initialize an algod client
algod_client = algod.AlgodClient(algod_token, algod_address)

# get suggested parameters
params = algod_client.suggested_params()
# create a transaction
sender = msig.address()
recipient = account_3
amount = 10000
note = "Hello Multisig".encode()
txn = PaymentTxn(sender, params, recipient, amount, None, note, None)

# create a SignedTransaction object
mtx = MultisigTransaction(txn, msig)

# sign the transaction
mtx.sign(private_key_1)
mtx.sign(private_key_2)

# print encoded transaction
# print(encoding.msgpack_encode(mtx))


    # wait for confirmation	
try:
# send the transaction
    txid = algod_client.send_raw_transaction(
    encoding.msgpack_encode(mtx))    
    print("TXID: ", txid)   
    confirmed_txn = wait_for_confirmation(algod_client, txid, 6)  
    print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))
    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))

except Exception as err:
    print(err)



