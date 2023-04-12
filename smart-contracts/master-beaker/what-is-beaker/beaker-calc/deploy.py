from bkr_contract import app, add
from beaker import sandbox, client

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
print(
    f"""Deployed app in txid {txid}
    App ID: {app_id}
    Address: {addr}
    """
)

return_value = app_client.call(add, a=10, b=5).return_value
print(return_value)
