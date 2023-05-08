from beaker import client, sandbox
from oncomplete_contract import app

app.build().export("./artifacts")

accounts = sandbox.kmd.get_accounts()
creator = accounts[0]
alice = accounts[1]

app_client = client.ApplicationClient(
    client=sandbox.get_algod_client(),
    app=app,
    sender=creator.address,
    signer=creator.signer,
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

alice_client = app_client.prepare(alice.signer)

try:
    alice_client.delete()
except:
    print("Only the creator can delete the smart contract!")

app_client.delete()
print("The contract is deleted.")
