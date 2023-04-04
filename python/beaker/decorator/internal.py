from beaker import Application, internal, external, sandbox, client
from pyteal import abi


class InternalDemo(Application):
    @external
    def add(self, a: abi.Uint8, b: abi.Uint8, *, output: abi.Uint8):
        return output.set(self.internal_add(a, b))

    @internal
    def internal_add(self, a: abi.Uint8, b: abi.Uint8):
        return a.get() + b.get()


def demo():
    app = InternalDemo()

    account = sandbox.get_accounts().pop()
    algod_client = sandbox.get_algod_client()

    app_client = client.ApplicationClient(
        client=algod_client, app=app, signer=account.signer
    )

    app_id, app_addr, txid = app_client.create()
    print("App ID: ", app_id)

    try:
        app_client.call(app.internal_add, a=1, b=2)
    except:
        print("You cannot call internal methods!")

    result = app_client.call(app.add, a=1, b=2)

    print("Result: ", result.return_value)


if __name__ == "__main__":
    demo()
