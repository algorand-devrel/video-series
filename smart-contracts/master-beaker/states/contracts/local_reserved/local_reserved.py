from beaker import Application, ReservedLocalStateValue, unconditional_opt_in_approval
from pyteal import abi, TealType, Txn


class ReservedLocalState:
    favorite_food = ReservedLocalStateValue(
        stack_type=TealType.bytes,
        max_keys=8,
        descr="8 key-value pairs of favorite foods Ranked from 1 to 8.",
    )


app = Application("Reserved Local App", state=ReservedLocalState()).apply(
    unconditional_opt_in_approval, initialize_local_state=True
)


@app.external
def set_reserved_local_state_val(k: abi.Uint8, v: abi.String):
    return app.state.favorite_food[k][Txn.sender()].set(v.get())


@app.external(read_only=True)
def get_reserved_local_state_val(k: abi.Uint8, *, output: abi.String):
    return output.set(app.state.favorite_food[k][Txn.sender()])
