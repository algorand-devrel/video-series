from list_app import app, bootstrap, subscribe, readSubscriber, deleteBox
from beaker import localnet, client
from beaker.consts import algo

app.build().export("./artifacts")

accounts = localnet.kmd.get_accounts()
sender = accounts[0]

print(f"Account 2: {accounts[1].address}")
print(f"Account 3: {accounts[2].address}")

app_client = client.ApplicationClient(
    client=localnet.get_algod_client(),
    app=app,
    sender=sender.address,
    signer=sender.signer,
)

app_client.create()

app_client.fund(1 * algo)

app_client.call(
    bootstrap,
    boxes=[(app_client.app_id, "addr_list")],
)

### Create App Client for Account 2 and 3 ###
app_client2 = app_client.prepare(signer=accounts[1].signer)
app_client3 = app_client.prepare(signer=accounts[2].signer)

### Subscribe ###
app_client2.call(
    subscribe, addr=accounts[1].address, boxes=[(app_client2.app_id, "addr_list")]
)

app_client3.call(
    subscribe, addr=accounts[2].address, boxes=[(app_client3.app_id, "addr_list")]
)

### Read Subscribers ###
global_state = app_client.get_global_state()
idx = int(global_state["idx"])

print("Algorand Developers Youtube Subscribers:")

for i in range(idx):
    value = app_client.call(
        readSubscriber,
        idx=i,
        boxes=[(app_client.app_id, "addr_list")],
    )
    print("  - ", value.return_value)


### Delete the Box ###
app_client.call(deleteBox, boxes=[(app_client.app_id, "addr_list")])
print("Box is deleted.")
