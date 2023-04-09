from beaker import Application, LocalStateBlob, unconditional_opt_in_approval
from pyteal import abi, Int


class LocalBlob:
    local_blob = LocalStateBlob(keys=2)


app = Application("Local Blob App", state=LocalBlob()).apply(
    unconditional_opt_in_approval, initialize_local_state=True
)


@app.external
def write_local_blob(v: abi.String):
    return app.state.local_blob.write(Int(0), v.get())


@app.external
def read_local_blob(*, output: abi.String):
    return output.set(
        app.state.local_blob.read(Int(0), app.state.local_blob.blob.max_bytes - Int(1))
    )
