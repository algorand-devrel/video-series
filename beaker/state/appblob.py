from typing import Final
from beaker import Application, external, create, sandbox, client
from pyteal import abi, Int

from beaker.state import ApplicationStateBlob


class AppStateBlob(Application):

    application_blob: Final[ApplicationStateBlob] = ApplicationStateBlob(
        keys=2,
    )

    @create
    def create(self):
        return self.initialize_application_state()

    @external
    def write_app_blob(self, start: abi.Uint64, v: abi.String):
        return self.application_blob.write(start.get(), v.get())

    @external
    def read_app_blob(self, *, output: abi.String):
        return output.set(
            self.application_blob.read(
                Int(0), self.application_blob.blob.max_bytes - Int(1)
            )
        )


def demo():
    app = AppStateBlob()

    account = sandbox.get_accounts().pop()
    algod_client = sandbox.get_algod_client()

    app_client = client.ApplicationClient(
        client=algod_client, app=app, signer=account.signer
    )

    app_id, app_addr, txid = app_client.create()
    print("App ID: ", app_id)

    app_client.call(app.write_app_blob, start=0, v="Chris likes icecream.")

    result = app_client.call(app.read_app_blob)
    print("App Blob: ", result.return_value)


if __name__ == "__main__":
    demo()
