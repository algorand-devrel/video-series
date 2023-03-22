from typing import Final
from beaker import (
    Application,
    ApplicationStateValue,
    create,
    external,
    sandbox,
    client,
)
from pyteal import abi, TealType, Bytes

class AppState(Application):

    my_description: Final[ApplicationStateValue] = ApplicationStateValue(
        stack_type=TealType.bytes,
        default=Bytes(
            "Chris is the best!"
        ),
        static=True,
    )

    @create
    def create(self):
        return self.initialize_application_state()

    @external
    def set_app_state_val(self, v: abi.String):
        return self.my_description.set(v.get())

    @external(read_only=True)
    def get_app_state_val(self, *, output: abi.String):
        return output.set(self.my_description)


def demo():

    app = AppState()

    account = sandbox.get_accounts().pop()
    algod_client = sandbox.get_algod_client()

    app_client = client.ApplicationClient(client=algod_client, app=app,signer=account.signer)

    app_id, app_addr, txid = app_client.create()
    print("App ID: ", app_id)

    try:
        app_client.call(app.set_app_state_val, v="Chris is the worst!")
    except:
        print("Failed as expected since this state is static")
    
    result = app_client.call(app.get_app_state_val)
    print("App State: ", result.return_value)


if __name__ == "__main__":
    demo()
    AppState().dump("./artifacts")