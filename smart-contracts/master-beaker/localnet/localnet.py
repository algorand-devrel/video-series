import json

from beaker import localnet

localnet_accounts = localnet.get_accounts()
print(*localnet_accounts, sep="\n\n")

account1 = localnet_accounts.pop()
print("\naccount1 info \n")
print("account1 address: ", account1.address, "\n")
print("account1 private key: ", account1.private_key, "\n")
print("account1 signer: ", account1.signer, "\n")

algod_client = localnet.get_algod_client()

sp = algod_client.suggested_params()
print("suggested minimum fee is: ", sp.min_fee, "\n")

indexer_client = localnet.get_indexer_client()

block_info = indexer_client.block_info(1)
print("Block 1 information using the indexer client: \n")
print(json.dumps(block_info, indent=2))
