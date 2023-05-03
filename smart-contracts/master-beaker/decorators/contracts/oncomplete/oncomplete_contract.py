from beaker import (
    Application,
    Authorize,
)
from pyteal import Approve, Expr, Global, Reject

app = Application("OnComplete App")


@app.opt_in
def opt_in() -> Expr:
    return Approve()


@app.close_out
def close_out() -> Expr:
    return Reject()


@app.clear_state
def clear_state() -> Expr:
    return Approve()


@app.update
def update() -> Expr:
    return Approve()


@app.delete(authorize=Authorize.only(Global.creator_address()))
def delete() -> Expr:
    return Approve()
