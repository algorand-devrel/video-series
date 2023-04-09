from internal_contract import app, add, internal_add
from beaker import sandbox, client

app.build().export(
    "./smart-contracts/master-beaker/decorators/contracts/internal/artifacts"
)

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

try:
    app_client.call(internal_add, a=1, b=2)
except:
    print("You cannot call internal Subroutine methods!")

result = app_client.call(add, a=1, b=2)

print("Result: ", result.return_value)
