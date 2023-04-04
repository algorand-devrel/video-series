from beaker import (
    Application,
    create,
    delete,
    update,
    opt_in,
    close_out,
    clear_state,
    sandbox,
    client,
    Authorize,
)
from pyteal import Approve, Reject, Global


class OncompleteDemo(Application):
    @create
    def create(self):
        return Approve()

    @update
    def update(self):
        return Approve()

    @opt_in
    def opt_in(self):
        return Approve()

    @close_out
    def close_out(self):
        return Reject()

    @clear_state
    def clear_state(self):
        return Approve()

    @delete(authorize=Authorize.only(Global.creator_address()))
    def delete(self):
        return Approve()


def demo():
    app = OncompleteDemo()

    account = sandbox.get_accounts().pop()
    algod_client = sandbox.get_algod_client()

    app_client = client.ApplicationClient(
        client=algod_client, app=app, signer=account.signer
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

    app_client.delete()
    print("The contract is deleted.")


if __name__ == "__main__":
    demo()
