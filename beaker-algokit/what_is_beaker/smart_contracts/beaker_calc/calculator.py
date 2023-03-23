import pyteal as pt
from beaker.application import Application
from pyteal import abi

app = Application("Beaker Calculator")


@app.external()
def add(a: abi.Uint64, b: abi.Uint64, *, output: abi.Uint64) -> pt.Expr:
    """Add a and b, return the result"""
    return output.set(a.get() + b.get())


@app.external()
def mul(a: abi.Uint64, b: abi.Uint64, *, output: abi.Uint64) -> pt.Expr:
    """Multiply a and b, return the result"""
    return output.set(a.get() * b.get())


@app.external()
def sub(a: abi.Uint64, b: abi.Uint64, *, output: abi.Uint64) -> pt.Expr:
    """Subtract b from a, return the result"""
    return output.set(a.get() - b.get())


@app.external()
def div(a: abi.Uint64, b: abi.Uint64, *, output: abi.Uint64) -> pt.Expr:
    """Divide a by b, return the result"""
    return output.set(a.get() / b.get())
