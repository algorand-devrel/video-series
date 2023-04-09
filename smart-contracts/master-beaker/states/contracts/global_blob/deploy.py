from global_blob_contract import app, write_app_blob, read_app_blob
from beaker import sandbox, client

app.build().export(
    "./smart-contracts/master-beaker/states/contracts/global_blob/artifacts"
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

app_client.call(write_app_blob, start=0, v="Chris likes icecream.")

result = app_client.call(read_app_blob)
print("App Blob: ", result.return_value)
