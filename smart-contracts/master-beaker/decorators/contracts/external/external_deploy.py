from beaker import client, sandbox
from external_contract import add, app

app.build().export("./artifacts")

accounts = sandbox.kmd.get_accounts()
sender = accounts[0]

app_client = client.ApplicationClient(
    client=sandbox.get_algod_client(),
    app=app,
    sender=sender.address,
    signer=sender.signer,
)

app_id, app_addr, txid = app_client.create()
print("App ID: ", app_id)

result = app_client.call(add, a=1, b=2)

print("Result: ", result.return_value)
