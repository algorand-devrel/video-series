
from typing import Final
from beaker import (
    Application,
    opt_in,
    external,
    sandbox,
    client
)
from pyteal import abi, Int

from beaker.state import AccountStateBlob


class AccountBlobState(Application):

    account_blob: Final[AccountStateBlob] = AccountStateBlob(keys=2)

    @opt_in
    def opt_in(self):
        return self.initialize_account_state()

    @external
    def write_acct_blob(self, v: abi.String):
        return self.account_blob.write(Int(0), v.get())

    @external
    def read_acct_blob(self, *, output: abi.String):
        return output.set(
            self.account_blob.read(Int(0), self.account_blob.blob.max_bytes - Int(1))
        )


def demo():
    app = AccountBlobState()

    account = sandbox.get_accounts().pop()
    algod_client = sandbox.get_algod_client()

    app_client = client.ApplicationClient(
        client=algod_client, app=app, signer=account.signer
    )

    app_id, app_addr, txid = app_client.create()
    print("App ID: ", app_id)

    app_client.opt_in()

    app_client.call(app.write_acct_blob, v="Chris likes popcorn.")

    result = app_client.call(app.read_acct_blob)
    print("App Blob: ", result.return_value)


if __name__ == "__main__":
    demo()