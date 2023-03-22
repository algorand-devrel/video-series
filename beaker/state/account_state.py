from typing import Final
from beaker import (
    Application,
    AccountStateValue,
    opt_in,
    external,
    sandbox,
    client
)
from pyteal import abi, TealType, Int, Txn

class AccountState(Application):

    count: Final[AccountStateValue] = AccountStateValue(
        stack_type=TealType.uint64,
        default=Int(1),
        descr="A counter that keeps track of counts.",
    )

    @opt_in
    def opt_in(self):
        return self.initialize_account_state()

    @external
    def incr_account_state(self, v: abi.Uint64):
        return self.count.increment(v.get())

    @external(read_only=True)
    def get_account_state(self, *, output: abi.Uint64):
        return output.set(self.count[Txn.sender()])


def demo():

    app = AccountState()

    account = sandbox.get_accounts().pop()
    algod_client = sandbox.get_algod_client()

    app_client = client.ApplicationClient(client=algod_client, app=app,signer=account.signer)

    app_id, app_addr, txid = app_client.create()
    print("App ID: ", app_id)

    app_client.opt_in()

    result1 = app_client.call(app.get_account_state)
    print("1st Account State: ", result1.return_value)

    app_client.call(app.incr_account_state, v = 2)

    result2 = app_client.call(app.get_account_state)
    print("2nd Account State: ", result2.return_value)


if __name__ == "__main__":
    demo()