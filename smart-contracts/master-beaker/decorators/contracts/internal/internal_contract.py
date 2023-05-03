from beaker import Application
from pyteal import Expr, Subroutine, TealType, abi

app = Application("Internal Subroutine Example App")


@app.external
def add(a: abi.Uint8, b: abi.Uint8, *, output: abi.Uint8) -> Expr:
    return output.set(internal_add(a, b))


@Subroutine(TealType.uint64)
def internal_add(a: abi.Uint8, b: abi.Uint8) -> Expr:
    return a.get() + b.get()
