from typing import Final
from beaker import (
    Application,
    ReservedAccountStateValue,
    opt_in,
    external,
)
from pyteal import abi, TealType, Txn


class DynamicAccountState(Application):

    dynamic_account_value: Final[ReservedAccountStateValue] = ReservedAccountStateValue(
        stack_type=TealType.bytes,
        max_keys=8,
        descr="A dynamic state value, allowing 8 keys to be reserved, in this case byte type",
    )

    @opt_in
    def opt_in(self):
        return self.initialize_account_state()

    @external
    def set_dynamic_account_state_val(self, k: abi.Uint8, v: abi.String):
        return self.dynamic_account_value[k][Txn.sender()].set(v.get())

    @external(read_only=True)
    def get_dynamic_account_state_val(self, k: abi.Uint8, *, output: abi.String):
        return output.set(self.dynamic_account_value[k][Txn.sender()])


if __name__ == "__main__":
    se = DynamicAccountState()