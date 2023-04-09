from beaker import Application, unconditional_create_approval, GlobalStateValue
from pyteal import abi, TealType, Bytes


class GlobalState:
    my_description = GlobalStateValue(
        stack_type=TealType.bytes,
        default=Bytes("Chris is the best!"),
        static=True,
    )


app = Application("GlobalStateValue", state=GlobalState).apply(
    unconditional_create_approval, initialize_global_state=True
)


@app.external
def set_app_state_val(v: abi.String):
    return app.state.my_description.set(v.get())


@app.external(read_only=True)
def get_app_state_val(*, output: abi.String):
    return output.set(app.state.my_description)
