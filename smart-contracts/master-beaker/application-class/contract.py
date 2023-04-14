from beaker import *
from pyteal import *


class MyState:
    app_state = GlobalStateValue(
        stack_type=TealType.uint64,
        default=Int(10),
    )


app = Application("SimpleApp", state=MyState()).apply(
    unconditional_create_approval, initialize_global_state=True
)


@app.external
def read_state(*, output: abi.Uint64) -> Expr:
    return output.set(app.state.app_state)
