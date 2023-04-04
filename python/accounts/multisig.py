import json
from algosdk.v2client import algod
from algosdk import encoding, mnemonic, account, transaction

# sandbox
algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
# Initialize an algod client
algod_client = algod.AlgodClient(algod_token, algod_address)

# never use mnemonics in production code, this is for demo purposes only
mnemonic1 = "patrol target joy dial ethics flip usual fatigue bulb security prosper brand coast arch casino burger inch cricket scissors shoe evolve eternal calm absorb school"
mnemonic2 = "genius inside turtle lock alone blame parent civil depend dinosaur tag fiction fun skill chief use damp daughter expose pioneer today weasel box about silly"
mnemonic3 = "off canyon mystery cable pluck emotion manual legal journey grit lunch include friend social monkey approve lava steel school mango auto cactus huge ability basket"

# For ease of reference, add account public and private keys to
# an accounts dict.

private_key_1 = mnemonic.to_private_key(mnemonic1)
account_1 = account.address_from_private_key(private_key=private_key_1)

private_key_2 = mnemonic.to_private_key(mnemonic2)
account_2 = account.address_from_private_key(private_key=private_key_2)

private_key_3 = mnemonic.to_private_key(mnemonic3)
account_3 = account.address_from_private_key(private_key=private_key_3)

print("Account 1 Address: ", account_1)
print("Account 2 Address: ", account_2)
print("Account 3 Address: ", account_3)

# create a multisig account
version = 1  # multisig version
threshold = 2  # how many signatures are necessary
msig = transaction.Multisig(version, threshold, [account_1, account_2])

print("Multisig Address: ", msig.address())


# get suggested parameters
params = algod_client.suggested_params()
# create a transaction
sender = msig.address()
recipient = account_3
amount = 10000
note = "Hello Multisig".encode()
txn = transaction.PaymentTxn(sender, params, recipient, amount, None, note, None)

# create a SignedTransaction object
mtx = transaction.MultisigTransaction(txn, msig)

# sign the transaction
mtx.sign(private_key_1)
mtx.sign(private_key_2)

try:
    txid = algod_client.send_raw_transaction(encoding.msgpack_encode(mtx))
    print("TXID: ", txid)
    confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 6)
    print("Result confirmed in round: {}".format(confirmed_txn["confirmed-round"]))
    print("Transaction information: {}".format(json.dumps(confirmed_txn, indent=4)))

except Exception as err:
    print(err)
