from beaker import *
from pyteal import *

from beaker.lib.storage import BoxList


class SubscriberStates:
    idx = GlobalStateValue(
        stack_type=TealType.uint64, default=Int(0), descr="number of subscribers"
    )

    addr_list = BoxList(abi.Address, 10)


app = Application("Subscriber Count App", state=SubscriberStates())


### Create box List and initialize global state ###
@app.external
def bootstrap() -> Expr:
    return Seq(
        Pop(app.state.addr_list.create()),  # Create a box with name "addr_list"
        app.initialize_global_state(),
    )


### Subscribe ###
@app.external
def subscribe(addr: abi.Address) -> Expr:
    return Seq(app.state.addr_list[app.state.idx].set(addr), app.state.idx.increment())


### Read Subscriber ###
@app.external
def readSubscriber(idx: abi.Uint32, *, output: abi.Address) -> Expr:
    return app.state.addr_list[idx.get()].store_into(output)


### delete ###
@app.external(authorize=Authorize.only(Global.creator_address()))
def deleteBox() -> Expr:
    return Assert(App.box_delete(Bytes("addr_list")))
