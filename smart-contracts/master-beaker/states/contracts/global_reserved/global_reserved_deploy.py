from global_reserved_contract import (
    app,
    set_reserved_app_state_val,
    get_reserved_app_state_val,
)
from beaker import sandbox, client

app.build().export(
    "./smart-contracts/master-beaker/states/contracts/global_reserved/artifacts"
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

app_client.call(set_reserved_app_state_val, k=1, v="Chris")
app_client.call(set_reserved_app_state_val, k=2, v="Ben")

result1 = app_client.call(get_reserved_app_state_val, k=1)
result2 = app_client.call(get_reserved_app_state_val, k=2)
print("State with Key 1: ", result1.return_value)
print("State with Key 2: ", result2.return_value)
