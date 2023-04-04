from typing import Final
from beaker import (
    Application,
    ReservedApplicationStateValue,
    external,
    sandbox,
    client,
)
from pyteal import abi, TealType


class ReservedAppState(Application):
    names: Final[ReservedApplicationStateValue] = ReservedApplicationStateValue(
        stack_type=TealType.bytes,
        max_keys=32,
        descr="dictionary of names with 32 possible keys",
    )

    @external
    def set_reserved_app_state_val(self, k: abi.Uint64, v: abi.String):
        return self.names[k].set(v.get())

    @external(read_only=True)
    def get_reserved_app_state_val(self, k: abi.Uint64, *, output: abi.String):
        return output.set(self.names[k])


def demo():
    app = ReservedAppState()

    account = sandbox.get_accounts().pop()
    algod_client = sandbox.get_algod_client()

    app_client = client.ApplicationClient(
        client=algod_client, app=app, signer=account.signer
    )

    app_id, app_addr, txid = app_client.create()
    print("App ID: ", app_id)

    app_client.call(app.set_reserved_app_state_val, k=1, v="Chris")
    app_client.call(app.set_reserved_app_state_val, k=2, v="Ben")

    result1 = app_client.call(app.get_reserved_app_state_val, k=1)
    result2 = app_client.call(app.get_reserved_app_state_val, k=2)
    print("State with Key 1: ", result1.return_value)
    print("State with Key 2: ", result2.return_value)


if __name__ == "__main__":
    demo()
