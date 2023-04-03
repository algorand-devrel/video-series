from algosdk import mnemonic
from algosdk import account

#  never use mnemonics in code, for demo purposes only
mymnemonic = "price clap dilemma swim genius fame lucky crack torch hunt maid palace ladder unlock symptom rubber scale load acoustic drop oval cabbage review abstract embark"

# utility function to restore account
def restore_account():
    # restore private key from mnemonic
    pk_account = mnemonic.to_private_key(mymnemonic)
    # restore account address from private key
    address = account.address_from_private_key(pk_account)
    print("Address :", address)

restore_account()
