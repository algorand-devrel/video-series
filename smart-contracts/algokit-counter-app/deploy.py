from counter_app import app, increment
from beaker import localnet, client


app.build().export("./src/artifacts")

accounts = localnet.kmd.get_accounts()
sender = accounts[0]

app_client = client.ApplicationClient(
    client=localnet.get_algod_client(),
    app=app,
    sender=sender.address,
    signer=sender.signer,
)

app_id, app_addr, txid = app_client.create()
print(f"app id: {app_id}")
print(f"app address: {app_addr}")
print(f"txn id: {txid}")

output = app_client.call(increment)
print(output.return_value)

output = app_client.call(increment)
print(output.return_value)

last_caller = app_client.get_global_state()["last_caller_address"]
print(f"Last Caller: {last_caller}")

app_client2 = app_client.prepare(signer=accounts[1].signer)

output = app_client2.call(increment)
print(output.return_value)

last_caller = app_client.get_global_state()["last_caller_address"]
print(f"Last Caller: {last_caller}")
