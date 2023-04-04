from pyteal import *

"""
Simple Charity application that does the following:
- accepts funding more or equal to 2 ALGOs and records the funder
- pay out 1 ALGO to an account
- retrieve who the funder is
"""

router = Router(
    "abi-type-example",
    BareCallActions(
        no_op=OnCompleteAction.create_only(Approve()),
    ),
)

PAYMENT_AMT = Int(1000000)  # 1 million microAlgos = 1 Algo


@router.method
def pay(receiver: abi.Account, *, output: abi.Address):
    return Seq(
        InnerTxnBuilder.Execute(
            {
                TxnField.type_enum: TxnType.Payment,
                TxnField.amount: PAYMENT_AMT,
                TxnField.receiver: receiver.address(),
            }
        ),
        output.set(receiver.address()),
    )


@router.method
def fund(payment: abi.PaymentTransaction):
    return Seq(
        Assert(payment.get().receiver() == Global.current_application_address()),
        Assert(payment.get().amount() >= (PAYMENT_AMT * Int(2))),  # cover txn cost
        App.globalPut(Bytes("funder"), payment.get().sender()),
    )


@router.method
def get_funder(*, output: abi.Address):
    return output.set(App.globalGet(Bytes("funder")))


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
