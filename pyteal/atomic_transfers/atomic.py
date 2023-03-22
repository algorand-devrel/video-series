from pyteal import *

router = Router(
    "Atomic Transfers Example",
    BareCallActions(
        no_op=OnCompleteAction.create_only(Approve()),
    ),
)

@router.method
def abi_multiple_pay(a:abi.PaymentTransaction, b:abi.PaymentTransaction):
    return Seq(
        Assert(a.get().receiver() == Global.current_application_address()),
        Assert(b.get().receiver() == Global.current_application_address()),
        Assert(a.get().amount() == Int(100000)),
        Assert(b.get().amount() == Int(200000)),
        Approve()
    )

@router.method
def multiple_pay(a:abi.PaymentTransaction, b:abi.PaymentTransaction):
    return Seq(
        Assert(Gtxn[0].receiver() == Global.current_application_address()),
        Assert(Gtxn[1].receiver() == Global.current_application_address()),
        Assert(Gtxn[0].amount() == Int(100000)),
        Assert(Gtxn[1].amount() == Int(200000)),
        Approve()
    )
            

if __name__ == "__main__":
    import os
    import json

    path = os.path.dirname(os.path.abspath(__file__))
    approval, clear, contract = router.compile_program(version=8)

    # Dump out the contract as json that can be read in by any of the SDKs
    with open(os.path.join(path, "artifacts/contract.json"), "w") as f:
        f.write(json.dumps(contract.dictify(), indent=2))

    # Write out the approval and clear programs
    with open(os.path.join(path, "artifacts/approval.teal"), "w") as f:
        f.write(approval)

    with open(os.path.join(path, "artifacts/clear.teal"), "w") as f:
        f.write(clear)