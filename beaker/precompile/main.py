from typing import Final
from pyteal import (
    abi,
    InnerTxn,
    InnerTxnBuilder,
    Int,
    Seq,
    TealType,
    TxnField,
    TxnType,
    Expr
)
from beaker import *
from beaker.precompile import AppPrecompile
from beaker.application import get_method_signature


class Profile(Application):
    name: Final[ApplicationStateValue] = ApplicationStateValue(
        stack_type=TealType.bytes,
    )

    likes: Final[ApplicationStateValue] = ApplicationStateValue(
        stack_type=TealType.uint64,
        default=Int(0),
    )

    @create
    def create(self, name_arg:abi.String):
        return Seq(
            self.name.set(name_arg.get()),
            self.initialize_application_state(),
        )

    @external
    def increment_likes(self, *, output: abi.Uint64):
        """Increment the counter global state."""
        return Seq(
            self.likes.increment(),
            output.set(self.likes.get()),
        )


class Manager(Application):
    profile: AppPrecompile = AppPrecompile(Profile())

    @external
    def create_profile(self, name: abi.String, *, output: abi.Uint64):
        """Create a new child app."""
        # config = self.profile.get_create_config()
        return Seq(
            InnerTxnBuilder.ExecuteMethodCall(
                method_signature=get_method_signature(Profile().create), 
                args=[name],
            ),
            output.set(InnerTxn.created_application_id()),
        )


def demo():

    algod_client = sandbox.get_algod_client()

    accounts = sandbox.get_accounts()

    account1 = accounts.pop()

    app = Manager()

    manager_client = client.ApplicationClient(client=algod_client, app=app, signer=account1.signer)

    manager_client.create()

    manager_client.fund(1 * consts.algo)

    result = manager_client.call(app.create_profile, name="Chris")

    profile_client = client.ApplicationClient(
        client=algod_client, 
        app=Profile(), 
        app_id=result.return_value, 
        signer=account1.signer
    )

    print(f"Number of likes: {profile_client.get_application_state()}")

    profile_client.call(Profile().increment_likes)

    print(f"Number of likes: {profile_client.get_application_state()}")


if __name__ == "__main__":
    demo()
    # Profile().dump()