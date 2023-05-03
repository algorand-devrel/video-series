from pyteal import *

# Create a simple Expression to use later
is_creator = Txn.sender() == Global.creator_address()

# Main router class
router = Router(
    # Name of the contract
    "PyTeal Calculator",
    BareCallActions(
        no_op=OnCompleteAction.create_only(Approve()),
        update_application=OnCompleteAction.always(Return(is_creator)),
        delete_application=OnCompleteAction.always(Return(is_creator)),
        close_out=OnCompleteAction.never(),
    ),
)


@router.method
def add(a: abi.Uint64, b: abi.Uint64, *, output: abi.Uint64) -> Expr:
    """sum a and b, return the result"""
    return output.set(a.get() + b.get())


if __name__ == "__main__":
    import os
    import json

    path = os.path.dirname(os.path.abspath(__file__))
    approval, clear, contract = router.compile_program(
        version=8, optimize=OptimizeOptions(scratch_slots=True)
    )

    # Dump out the contract as json that can be read in by any of the SDKs
    with open(os.path.join(path, "artifacts/contract.json"), "w") as f:
        f.write(json.dumps(contract.dictify(), indent=2))

    # Write out the approval and clear programs
    with open(os.path.join(path, "artifacts/approval.teal"), "w") as f:
        f.write(approval)

    with open(os.path.join(path, "artifacts/clear.teal"), "w") as f:
        f.write(clear)
