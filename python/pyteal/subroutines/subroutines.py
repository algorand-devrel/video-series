from pyteal import *

my_router = Router(
    "subroutine example",
    BareCallActions(
        no_op=OnCompleteAction.create_only(Approve())
    )
)

### Internal Subroutines ###

@Subroutine(TealType.uint64)
def add(a:abi.Uint64, b:abi.Uint64):
    return a.get() + b.get()

@Subroutine(TealType.uint64)
def subtract(a:abi.Uint64, b:abi.Uint64):
    return a.get() - b.get()

### External Subroutine ###

@my_router.method
def call_internal(action: abi.String, a:abi.Uint64, b:abi.Uint64, *, output: abi.Uint64):
    return Seq(
        If(action.get() == Bytes("add"))
        .Then(output.set(add(a, b)))
        .ElseIf(action.get() == Bytes("subtract"))
        .Then(output.set(subtract(a, b)))
    )


if __name__ == "__main__":
    import os
    import json

    path = os.path.dirname(os.path.abspath(__file__))
    approval, clear, contract = my_router.compile_program(version=8)

    # Dump out the contract as json that can be read in by any of the SDKs
    with open(os.path.join(path, "artifacts/contract.json"), "w") as f:
        f.write(json.dumps(contract.dictify(), indent=2))

    # Write out the approval and clear programs
    with open(os.path.join(path, "artifacts/approval.teal"), "w") as f:
        f.write(approval)

    with open(os.path.join(path, "artifacts/clear.teal"), "w") as f:
        f.write(clear)