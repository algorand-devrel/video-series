from beaker import Application, LocalStateValue, unconditional_opt_in_approval
from pyteal import Int, TealType, Txn, abi


class LocalState:
    count = LocalStateValue(
        stack_type=TealType.uint64,
        default=Int(1),
        descr="A counter that keeps track of counts.",
    )


app = Application("Local State App", state=LocalState()).apply(
    unconditional_opt_in_approval, initialize_local_state=True
)


@app.external
def incr_local_state(v: abi.Uint64):
    return app.state.count.increment(v.get())


@app.external(read_only=True)
def get_local_state(*, output: abi.Uint64):
    return output.set(app.state.count[Txn.sender()])
