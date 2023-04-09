from local_state import app, incr_local_state, get_local_state
from beaker import sandbox, client

app.build().export(
    "./smart-contracts/master-beaker/states/contracts/local_state/artifacts"
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

result1 = app_client.call(get_local_state)
print("1st Account State: ", result1.return_value)

app_client.call(incr_local_state, v=2)

result2 = app_client.call(get_local_state)
print("2nd Account State: ", result2.return_value)
