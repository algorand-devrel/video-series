from typing import Final

from beaker import *
from pyteal import *


class UserCounter(Application):
    user: Final[AccountStateValue] = AccountStateValue(
        stack_type=TealType.bytes,
        descr="Username",
    )

    count: Final[AccountStateValue] = AccountStateValue(
        stack_type=TealType.uint64,
        default=Int(0),
        descr="number of counts",
    )

    @opt_in
    def opt_in(self, username: abi.String):
        return Seq(self.initialize_account_state(), self.user.set(username.get()))

    @external(authorize=Authorize.opted_in())
    def increment(self):
        return self.count.increment()

    @close_out
    def close_out(self):
        return Approve()

    @delete(authorize=Authorize.only(Global.creator_address()))
    def delete(self):
        return Approve()


def demo():
    algod_client = sandbox.get_algod_client()

    accounts = sandbox.get_accounts()

    acct1 = accounts.pop()
    acct2 = accounts.pop()

    counter_app = UserCounter()

    app_client1 = client.ApplicationClient(
        client=algod_client, app=counter_app, signer=acct1.signer
    )

    app_id, address, txid = app_client1.create()
    print("App ID: ", app_id)
    print(f"app state: {app_client1.get_application_state()} \n")

    app_client1.fund(1 * consts.algo)
    print(f"app account state: {app_client1.get_application_account_info()} \n")

    app_client1.opt_in(username="Chris")
    print("Chris opted in \n")

    app_client2 = app_client1.prepare(signer=acct2.signer)

    app_client2.opt_in(username="Ben")
    print("Ben opted in \n")

    app_client1.call(counter_app.increment)
    print("Chris incremented his counter. \n")

    app_client2.call(counter_app.increment)
    print("Ben incremented his counter. \n")
    app_client2.call(counter_app.increment)
    print("Ben incremented his counter. \n")

    print(f"account 1 account state: {app_client1.get_account_state()} \n")
    print(f"account 2 account state: {app_client2.get_account_state()} \n")

    try:
        app_client1.close_out()
        app_client2.close_out()
        app_client1.delete()
        print("successfully closed out and deleted the app.")
    except Exception as e:
        print(e)


demo()
