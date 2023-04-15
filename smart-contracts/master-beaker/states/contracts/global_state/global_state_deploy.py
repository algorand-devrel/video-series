from beaker import client, sandbox
from global_state_deploy import app, get_app_state_val, set_app_state_val

app.build().export(
    "./smart-contracts/master-beaker/states/contracts/global_state/artifacts"
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

try:
    app_client.call(set_app_state_val, v="Chris is the worst!")
except:
    print("Failed as expected since this state is static")

result = app_client.call(get_app_state_val)
print("App State: ", result.return_value)
