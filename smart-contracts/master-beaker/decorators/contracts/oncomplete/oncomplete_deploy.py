from oncomplete_contract import app
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

app_id, app_addr, txid = app_client.create()
print("App ID: ", app_id)

app_client.opt_in()
print("Opted into the contract.")

try:
    app_client.close_out()
except Exception as e:
    print(e)

app_client.clear_state()
print("forcefully opted out with clear state transaction.")

app_client.delete()
print("The contract is deleted.")
