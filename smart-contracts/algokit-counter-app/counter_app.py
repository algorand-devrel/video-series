from beaker import *
from pyteal import *


class CounterState:
    counter = GlobalStateValue(
        stack_type=TealType.uint64,
        default=Int(0),
        descr="Counter",
    )

    last_caller_address = GlobalStateValue(
        stack_type=TealType.bytes,
        default=Global.creator_address(),
        descr="Last caller address",
    )


app = Application("Counter", state=CounterState).apply(
    unconditional_create_approval, initialize_global_state=True
)


@app.external
def increment(*, output: abi.Uint64) -> Expr:
    return Seq(
        # Increment the counter
        app.state.counter.set(app.state.counter + Int(1)),
        # Save caller address
        app.state.last_caller_address.set(Txn.sender()),
        output.set(app.state.counter),
    )
