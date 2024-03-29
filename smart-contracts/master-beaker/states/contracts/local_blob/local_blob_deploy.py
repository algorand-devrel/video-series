from beaker import client, sandbox
from local_blob_contract import app, read_local_blob, write_local_blob

app.build().export("./artifacts")

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
