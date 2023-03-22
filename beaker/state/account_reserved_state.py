from typing import Final
from beaker import (
    Application,
    ReservedAccountStateValue,
    opt_in,
    external,
    sandbox,
    client
)
from pyteal import abi, TealType, Txn


class ReservedAccountState(Application):

    favorite_food: Final[ReservedAccountStateValue] = ReservedAccountStateValue(
        stack_type=TealType.bytes,
        max_keys=8,
        descr="8 key-value pairs of favorite foods Ranked from 1 to 8.",
    )

    @opt_in
    def opt_in(self):
        return self.initialize_account_state()

    @external
    def set_dynamic_account_state_val(self, k: abi.Uint8, v: abi.String):
        return self.favorite_food[k][Txn.sender()].set(v.get())

    @external(read_only=True)
    def get_dynamic_account_state_val(self, k: abi.Uint8, *, output: abi.String):
        return output.set(self.favorite_food[k][Txn.sender()])


def demo():
    app = ReservedAccountState()

    account = sandbox.get_accounts().pop()
    algod_client = sandbox.get_algod_client()

    app_client = client.ApplicationClient(
        client=algod_client, app=app, signer=account.signer
    )

    app_id, app_addr, txid = app_client.create()
    print("App ID: ", app_id)

    app_client.opt_in()

    app_client.call(app.set_dynamic_account_state_val, k=1, v="Sushi")
    app_client.call(app.set_dynamic_account_state_val, k=2, v="Steak")

    result1 = app_client.call(app.get_dynamic_account_state_val, k=1)
    result2 = app_client.call(app.get_dynamic_account_state_val, k=2)
    print("Most favorite food: ", result1.return_value)
    print("Second favorite food: ", result2.return_value)


if __name__ == "__main__":
    demo()
