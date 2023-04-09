from local_blob import app, write_local_blob, read_local_blob
from beaker import sandbox, client

app.build().export(
    "./smart-contracts/master-beaker/states/contracts/local_blob/artifacts"
)

accounts = sandbox.kmd.get_accounts()
sender = accounts[0]

app_client = client.ApplicationClient(
    client=sandbox.get_algod_client(),
    app=app,
    sender=sender.address,
    signer=sender.signer,
)

app_id, addr, txid = app_client.create()

print("App ID: ", app_id)

app_client.opt_in()

app_client.call(write_local_blob, v="Chris likes popcorn.")

result = app_client.call(read_local_blob)
print("App Blob: ", result.return_value)
