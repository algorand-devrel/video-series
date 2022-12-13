from typing import Final
from beaker import (
    Application,
    AccountStateValue,
    opt_in,
    external,
)
from pyteal import abi, TealType, Int, Txn



class AccountStateExample(Application):

    declared_account_value: Final[AccountStateValue] = AccountStateValue(
        stack_type=TealType.uint64,
        default=Int(1),
        descr="An int stored for each account that opts in",
    )

    @opt_in
    def opt_in(self):
        return self.initialize_account_state()

    @external
    def set_account_state_val(self, v: abi.Uint64):
        # Accessing with `[Txn.sender()]` is redundant but
        # more clear what is happening
        return self.declared_account_value[Txn.sender()].set(v.get())

    @external
    def incr_account_state_val(self, v: abi.Uint64):
        # Omitting [Txn.sender()] just for demo purposes
        return self.declared_account_value.increment(v.get())

    @external(read_only=True)
    def get_account_state_val(self, *, output: abi.Uint64):
        return output.set(self.declared_account_value[Txn.sender()])


if __name__ == "__main__":
    se = AccountStateExample()