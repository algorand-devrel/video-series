from pyteal import *

router = Router(
    "datatype-example", BareCallActions(no_op=OnCompleteAction.create_only(Approve()))
)


@router.method
def store_in_bytes(number: abi.Uint64):
    return App.globalPut(Bytes("num_in_bytes"), Itob(number.get()))


@router.method
def read_in_int(*, output: abi.Uint64):
    return output.set(Btoi(App.globalGet(Bytes("num_in_bytes"))))


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
