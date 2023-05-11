from pyteal import *

# Our custom Struct
class GroceryItem(abi.NamedTuple):
    item: abi.Field[abi.String]
    amount: abi.Field[abi.Uint8]
    purchased: abi.Field[abi.Bool]

router = Router(
    "Grocery List App",
    BareCallActions(
        no_op=OnCompleteAction.create_only(Approve()),
    ),
)

### Create ###

@router.method
def addGrocery(item_name: abi.String, grocery_item: GroceryItem):
    return App.box_put(item_name.get(), grocery_item.encode())

### Write ###

# @router.method
# def replaceBox(box_name: abi.String, new_name: abi.String):
#     return App.box_replace(box_name.get(), Int(0), new_name.get())

# @router.method
# def writeBox(box_name: abi.String, new_name: abi.String):
#     return App.box_put(box_name.get(), new_name.get())

### Read ###
@router.method
def getBoxItem(item_name: abi.String, *, output: abi.String):
    return Seq(
            contents := App.box_get(item_name.get()), # box_get returns a maybeValue with Boolean and box Content.
            Assert(contents.hasValue()),
            (grocery_tuple := GroceryItem()).decode(contents.value()),
            output.set(grocery_tuple.item),
        )  

@router.method
def getAmount(item_name: abi.String, *, output: abi.Uint8):
    return Seq(
            contents := App.box_get(item_name.get()), # box_get returns a maybeValue with Boolean and box Content.
            Assert(contents.hasValue()),
            (grocery_tuple := GroceryItem()).decode(contents.value()),
            output.set(grocery_tuple.amount),
        ) 

@router.method
def getPurchased(item_name: abi.String, *, output: abi.Bool):
    return Seq(
            contents := App.box_get(item_name.get()), # box_get returns a maybeValue with Boolean and box Content.
            Assert(contents.hasValue()),
            (grocery_tuple := GroceryItem()).decode(contents.value()),
            output.set(grocery_tuple.purchased),
        )  

### delete ###

@router.method
def deleteBox(box_name: abi.String):
    return Assert(App.box_delete(box_name.get()))

### box size ###

@router.method
def getBoxSize(item_name: abi.String, *, output:abi.Uint64):
    return Seq(
            length := App.box_length(item_name.get()), # box_length returns a maybeValue with Boolean and box length.
            Assert(length.hasValue()),
            output.set(length.value())
        )


if __name__ == "__main__":
    import os
    import json

    path = os.path.dirname(os.path.abspath(__file__))
    approval, clear, contract = router.compile_program(version=8)

    # Dump out the contract as json that can be read in by any of the SDKs
    with open(os.path.join(path, "grocery_artifacts/contract.json"), "w") as f:
        f.write(json.dumps(contract.dictify(), indent=2))

    # Write out the approval and clear programs
    with open(os.path.join(path, "grocery_artifacts/approval.teal"), "w") as f:
        f.write(approval)

    with open(os.path.join(path, "grocery_artifacts/clear.teal"), "w") as f:
        f.write(clear)




