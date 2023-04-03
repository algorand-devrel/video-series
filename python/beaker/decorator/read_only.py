from typing import Final
from beaker import (
    Application,
    ApplicationStateValue,
    external,
    sandbox,
    client,
    create
)
from pyteal import abi, TealType, Int, Seq


class ReadOnlyDemo(Application):

    number: Final[ApplicationStateValue] = ApplicationStateValue(
        stack_type=TealType.uint64,
        default=Int(7)
    )

    @create
    def create(self):
        return self.initialize_application_state()

    @external(read_only=True)
    def set_number(self, v: abi.Uint8, *, output: abi.Uint64):
        return Seq(
            self.number.set(v.get()),
            output.set(self.number)
        ) 

    @external(read_only=True)
    def get_number(self, *, output: abi.Uint64):
        return output.set(self.number)


def demo():
    app = ReadOnlyDemo()

    account = sandbox.get_accounts().pop()
    algod_client = sandbox.get_algod_client()

    app_client = client.ApplicationClient(
        client=algod_client, app=app, signer=account.signer
    )

    app_id, app_addr, txid = app_client.create()
    print("App ID: ", app_id)

    result = app_client.call(app.set_number, v=1)
    print("The number value changed to: ", result.return_value)
    
    result = app_client.call(app.get_number)
    print("The number recorded on the blockchain is still: ", result.return_value)

if __name__ == "__main__":
    demo()
