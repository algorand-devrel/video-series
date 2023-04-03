from pyteal import *
from beaker import *


class Calculator(Application):
    @external
    def add(self, a: abi.Uint64, b: abi.Uint64, *, output: abi.Uint64):
        """Add a and b, return the result"""
        return output.set(a.get() + b.get())


def demo():
    app_client = sandbox.get_algod_client()

    acct = sandbox.get_accounts().pop()

    # Create an Application client containing both an algod client and app
    app_client = client.ApplicationClient(
        client=app_client, app=Calculator(), signer=acct.signer
    )

    # Create the application on chain, set the app id for the app client
    app_id, app_addr, txid = app_client.create()
    print(f"Created App with id: {app_id} and address addr: {app_addr} in tx: {txid}")

    result = app_client.call(Calculator.add, a=2, b=2)
    print(f"add result: {result.return_value}")


if __name__ == "__main__":
    Calculator().dump("./beaker_artifacts")
    demo()
