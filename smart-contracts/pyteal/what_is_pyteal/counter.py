from pyteal import *

handle_creation = Seq(App.globalPut(Bytes("Count"), Int(0)), Approve())

router = Router(
    "Simple Counter",
    BareCallActions(
        no_op=OnCompleteAction.create_only(handle_creation),
    ),
)


@router.method
def increment():
    scratchCount = ScratchVar(TealType.uint64)
    return Seq(
        scratchCount.store(App.globalGet(Bytes("Count"))),
        App.globalPut(Bytes("Count"), scratchCount.load() + Int(1)),
    )


@router.method
def read_count(*, output: abi.Uint64):
    return output.set(App.globalGet(Bytes("Count")))


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
