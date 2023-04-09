from beaker import client, consts, sandbox

from app import app, increment

app.build().export("./artifacts")

accounts = sandbox.kmd.get_accounts()
sender = accounts[0]
acct2 = accounts[1]

app_client1 = client.ApplicationClient(
    client=sandbox.get_algod_client(),
    app=app,
    sender=sender.address,
    signer=sender.signer,
)

app_id, address, txid = app_client1.create()
print("App ID: ", app_id)
print(f"app state: {app_client1.get_application_account_info()} \n")

app_client1.fund(1 * consts.algo)
print(f"app account state: {app_client1.get_application_account_info()} \n")

app_client1.opt_in()
# app_client1.opt_in(username="Chris")
print("Chris opted in \n")

app_client2 = app_client1.prepare(signer=acct2.signer)

app_client2.opt_in(username="Ben")
print("Ben opted in \n")

app_client1.call(increment)
print("Chris incremented his counter. \n")

app_client2.call(increment)
print("Ben incremented his counter. \n")
app_client2.call(increment)
print("Ben incremented his counter. \n")

print(f"account 1 account state: {app_client1.get_local_state()} \n")
print(f"account 2 account state: {app_client2.get_local_state()} \n")

try:
    app_client1.close_out()
    app_client2.close_out()
    app_client1.delete()
    print("successfully closed out and deleted the app.")
except Exception as e:
    print(e)
