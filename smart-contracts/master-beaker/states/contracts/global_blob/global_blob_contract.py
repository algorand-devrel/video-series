from beaker import Application, GlobalStateBlob, unconditional_create_approval
from pyteal import Int, abi


class AppState:
    global_blob = GlobalStateBlob(
        keys=2,
    )


app = Application("Global Blob App", state=AppState).apply(
    unconditional_create_approval, initialize_global_state=True
)


@app.external
def write_app_blob(start: abi.Uint64, v: abi.String):
    return app.state.global_blob.write(start.get(), v.get())


@app.external
def read_app_blob(*, output: abi.String):
    return output.set(
        app.state.global_blob.read(
            Int(0), app.state.global_blob.blob.max_bytes - Int(1)
        )
    )
