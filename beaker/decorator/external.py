from beaker import (
    Application,
    external,
    sandbox,
    client
)
from pyteal import abi


class ExternalDemo(Application):

    @external
    def add(self, a: abi.Uint8, b: abi.Uint8, *, output: abi.Uint8):
        return output.set(a.get() + b.get())


def demo():
    app = ExternalDemo()

    account = sandbox.get_accounts().pop()
    algod_client = sandbox.get_algod_client()

    app_client = client.ApplicationClient(
        client=algod_client, app=app, signer=account.signer
    )

    app_id, app_addr, txid = app_client.create()
    print("App ID: ", app_id)

    result = app_client.call(app.add, a=1, b=2)

    print("Result: ", result.return_value)


if __name__ == "__main__":
    demo()
