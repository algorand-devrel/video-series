from beaker import client, sandbox
from local_reserved_contract import (
    app,
    get_reserved_local_state_val,
    set_reserved_local_state_val,
)

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

app_client.call(set_reserved_local_state_val, k=1, v="Sushi")
app_client.call(set_reserved_local_state_val, k=2, v="Steak")

result1 = app_client.call(get_reserved_local_state_val, k=1)
result2 = app_client.call(get_reserved_local_state_val, k=2)
print("Most favorite food: ", result1.return_value)
print("Second favorite food: ", result2.return_value)
