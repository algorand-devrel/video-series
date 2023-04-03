import base64
import json

from algosdk import account, mnemonic, transaction
from algosdk.v2client import algod

# # This is a complete code example that:
# #   1. Creates a new test account
# #   2. Ask to fund your created account

def create_account():
    # Change algod_token and algod_address to connect to a different client
	algod_address = "http://localhost:4001"
	algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
	algod_client = algod.AlgodClient(algod_token, algod_address)

    # Generate new account for this transaction
	secret_key, my_address = account.generate_account()
    
	print("My address: {}".format(my_address))
	print("My private key: {}".format(secret_key))
	print("My mnemonic: {}".format(mnemonic.from_private_key(secret_key)))
    # Check your balance. It should be 0 microAlgos


	account_info = algod_client.account_info(my_address)
	print("Account balance: {} microAlgos".format(account_info.get('amount')) + "\n")

    # Fund the created account
	print('Fund the created account using testnet faucet: \n https://dispenser.testnet.aws.algodev.network/?account=' + format(my_address))

	completed = ""

	while completed.lower() != 'yes':
		completed = input("Type 'yes' once you funded the account: ");
    
	print('Fund transferred!')
    # Check your balance. It should be 5000000 microAlgos
	account_info = algod_client.account_info(my_address)
	print("Account balance: {} microAlgos".format(account_info.get('amount')) + "\n")
    # build transaction
	print("Building transaction")
	params = algod_client.suggested_params()
    # comment out the next two (2) lines to use suggested fees
	# params.flat_fee = True
	# params.fee = 1000
	receiver = "HZ57J3K46JIJXILONBBZOHX6BKPXEM2VVXNRFSUED6DKFD5ZD24PMJ3MVA"
	note = "Hello World".encode()
	amount = 100000
	closeto= "HZ57J3K46JIJXILONBBZOHX6BKPXEM2VVXNRFSUED6DKFD5ZD24PMJ3MVA"
    # Fifth argument is a close_remainder_to parameter that creates a payment txn that sends all of the remaining funds to the specified address. If you want to learn more, go to: https://developer.algorand.org/docs/reference/transactions/#payment-transaction
	unsigned_txn = transaction.PaymentTxn(my_address, params, receiver, amount, closeto, note)

    # sign transaction
	print("Signing transaction")
	signed_txn = unsigned_txn.sign(secret_key)
	print("Sending transaction")
	txid = algod_client.send_transaction(signed_txn)
	print('Transaction Info:')
	print("Signed transaction with txID: {}".format(txid))

    # wait for confirmation	
	try:
		print("Waiting for confirmation")
		confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4)  
	except Exception as err:
		print(err)
		return
	print("txID: {}".format(txid), " confirmed in round: {}".format(confirmed_txn.get("confirmed-round", 0))) 
	print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
	print("Decoded note: {}".format(base64.b64decode(
        confirmed_txn["txn"]["txn"]["note"]).decode()))
	print("Starting Account balance: {} microAlgos".format(account_info.get('amount')) )
	print("Amount transfered: {} microAlgos".format(amount) )    
	print("Fee: {} microAlgos".format(params.min_fee) ) 
	closetoamt = account_info.get('amount') - (params.min_fee + amount)
	print("Close to Amount: {} microAlgos".format(closetoamt) + "\n")

	account_info = algod_client.account_info(my_address)
	print("Final Account balance: {} microAlgos".format(account_info.get('amount')) + "\n")

create_account()
