from beaker import Application, ReservedGlobalStateValue
from pyteal import Expr, TealType, abi


class ReservedGlobalState:
    names = ReservedGlobalStateValue(
        stack_type=TealType.bytes,
        max_keys=32,
        descr="dictionary of names with 32 possible keys",
    )


app = Application("ReservedGlobalStateApp", state=ReservedGlobalState())


@app.external
def set_reserved_app_state_val(k: abi.Uint64, v: abi.String) -> Expr:
    return app.state.names[k].set(v.get())


@app.external(read_only=True)
def get_reserved_app_state_val(k: abi.Uint64, *, output: abi.String) -> Expr:
    return output.set(app.state.names[k])
