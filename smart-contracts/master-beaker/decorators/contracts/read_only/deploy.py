from app import app, hello
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

app_client.create()

return_value = app_client.call(hello, name="Beaker").return_value
print(return_value)
