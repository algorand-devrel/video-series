from beaker import Application
from pyteal import abi

app = Application("External Example App")


@app.external
def add(a: abi.Uint8, b: abi.Uint8, *, output: abi.Uint8):
    return output.set(a.get() + b.get())
