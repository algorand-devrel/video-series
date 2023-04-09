from beaker import Application, unconditional_create_approval, GlobalStateBlob
from pyteal import abi, Int


class GlobalStateBlob:
    application_blob = GlobalStateBlob(
        keys=2,
    )


app = Application("Global Blob App", state=GlobalStateBlob).apply(
    unconditional_create_approval, initialize_global_state=True
)


@app.external
def write_app_blob(start: abi.Uint64, v: abi.String):
    return app.state.application_blob.write(start.get(), v.get())


@app.external
def read_app_blob(*, output: abi.String):
    return output.set(
        app.state.application_blob.read(
            Int(0), app.state.application_blob.blob.max_bytes - Int(1)
        )
    )