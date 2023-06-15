from mapping_app import (
    app,
    addGrocery,
    updatePurchased,
    readItem,
    deleteGrocery,
)
from beaker import localnet, client
from beaker.consts import algo
from algokit_utils.logic_error import LogicError

app.build().export("./artifacts")

accounts = localnet.kmd.get_accounts()
sender = accounts[0]

app_client = client.ApplicationClient(
    client=localnet.get_algod_client(),
    app=app,
    sender=sender.address,
    signer=sender.signer,
)

app_client.create()

app_client.fund(1 * algo)

app_client.call(
    addGrocery,
    item_name="Apple",
    boxes=[(app_client.app_id, "Apple")],
)

value = app_client.call(
    readItem, item_name="Apple", boxes=[(app_client.app_id, "Apple")]
)
print(value.return_value)


value = app_client.call(
    updatePurchased, item_name="Apple", boxes=[(app_client.app_id, "Apple")]
)
print(value.return_value)


app_client.call(deleteGrocery, item_name="Apple", boxes=[(app_client.app_id, "Apple")])

try:
    value = app_client.call(
        readItem, item_name="Apple", boxes=[(app_client.app_id, "Apple")]
    )
    print(value.return_value)
except LogicError as e:
    print("Apple box no longer exists")
