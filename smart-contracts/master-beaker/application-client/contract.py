from beaker import (
    Application,
    Authorize,
    LocalStateValue,
)
from pyteal import Approve, Expr, Global, Int, Seq, TealType, abi


class UserCounter:
    user = LocalStateValue(
        stack_type=TealType.bytes,
        descr="Username",
    )

    count = LocalStateValue(
        stack_type=TealType.uint64,
        default=Int(0),
        descr="number of counts",
    )


app = Application("User Counter Example App", state=UserCounter())


@app.opt_in
def opt_in(username: abi.String) -> Expr:
    return Seq(app.initialize_local_state(), app.state.user.set(username.get()))


@app.external(authorize=Authorize.opted_in())
def increment() -> Expr:
    return app.state.count.increment()


@app.close_out(bare=True)
def close_out() -> Expr:
    return Approve()


@app.delete(bare=True, authorize=Authorize.only(Global.creator_address()))
def delete() -> Expr:
    return Approve()
