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

    dynamic_account_value: Final[ReservedAccountStateValue] = ReservedAccountStateValue(
        stack_type=TealType.bytes,
        max_keys=8,
        descr="A dynamic state value, allowing 8 keys to be reserved, in this case byte type",
    )

    @opt_in
    def opt_in(self):
        return self.initialize_account_state()

    @external
    def set_dynamic_account_state_val(self, k: abi.Uint8, v: abi.String):
        return self.dynamic_account_value[k][Txn.sender()].set(v.get())

    @external(read_only=True)
    def get_dynamic_account_state_val(self, k: abi.Uint8, *, output: abi.String):
        return output.set(self.dynamic_account_value[k][Txn.sender()])


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

    app_client.call(app.set_dynamic_account_state_val, k=1, v="Chris")
    app_client.call(app.set_dynamic_account_state_val, k=2, v="Ben")

    result1 = app_client.call(app.get_dynamic_account_state_val, k=1)
    result2 = app_client.call(app.get_dynamic_account_state_val, k=2)
    print("State with Key 1: ", result1.return_value)
    print("State with Key 2: ", result2.return_value)


if __name__ == "__main__":
    demo()
