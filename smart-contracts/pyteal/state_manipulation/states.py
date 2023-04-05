from pyteal import *

router = Router(
    "state manipulation",
    BareCallActions(
        no_op=OnCompleteAction.create_only(Approve()),
        opt_in=OnCompleteAction.call_only(Approve()),
        close_out=OnCompleteAction.call_only(Approve()),
    ),
    clear_state=Approve(),
)


### Global State Operations ###
@router.method
def writeGlobal(quote: abi.String):
    return App.globalPut(Bytes("quote"), quote.get())


@router.method
def readGlobal(*, output: abi.String):
    return output.set(App.globalGet(Bytes("quote")))


@router.method
def deleteGlobal():
    return App.globalDel(Bytes("quote"))


### Local State Operations ###


@router.method
def writeLocal(name: abi.String):
    return App.localPut(Txn.sender(), Bytes("name"), name.get())


@router.method
def readLocal(*, output: abi.String):
    return output.set(App.localGet(Txn.sender(), Bytes("name")))


@router.method
def deleteLocal():
    return App.localDel(Txn.sender(), Bytes("name"))


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
