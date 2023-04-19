from beaker import (
    Application,
    Authorize,
)
from pyteal import Approve, Reject, Global

app = Application("OnComplete App")

@app.opt_in
def opt_in():
    return Approve()

@app.close_out
def close_out():
    return Reject()

@app.clear_state
def clear_state(): 
    return Approve()

@app.update
def update():
    return Approve()

@app.delete(authorize=Authorize.only(Global.creator_address()))
def delete():
    return Approve()
