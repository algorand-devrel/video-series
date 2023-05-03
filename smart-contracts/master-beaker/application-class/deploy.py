from contract import app, read_state
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

return_value = app_client.call(read_state).return_value
print(f"The default state is: {return_value}")
