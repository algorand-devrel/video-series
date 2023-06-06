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

### Add Grocery with Boxes ###

@router.method
def addGrocery(item_name: abi.String, amount: abi.Uint8) -> Expr:
    return Seq(
            (purchased := abi.Bool()).set(Int(0)),
            (grocery_tuple := GroceryItem()).set(item_name, amount, purchased),
            App.box_put(item_name.get(), grocery_tuple.encode())
        )

### Update Grocery Item ###

@router.method
def updateAmount(item_name: abi.String, new_amount:abi.Uint8, *, output: GroceryItem) -> Expr:
    return Seq(
            contents := App.box_get(item_name.get()), # box_get returns a maybeValue with Boolean and box Content.
            Assert(contents.hasValue()),
            (new_grocery := GroceryItem()).decode(contents.value()),
            (amount := abi.Uint8()).set(new_amount.get()),
            (item := abi.String()).set(new_grocery.item),
            (purchased := abi.Bool()).set(new_grocery.purchased),
            # We've gotta set all of the fields at the same time, but we can
            # borrow the item we already know about
            new_grocery.set(item, amount, purchased),
            Assert(App.box_delete(item_name.get())),
            App.box_put(item_name.get(), new_grocery.encode()),
            output.decode(new_grocery.encode())
        )

@router.method
def updatePurchased(item_name: abi.String, *, output: GroceryItem) -> Expr:
    return Seq(
            contents := App.box_get(item_name.get()), # box_get returns a maybeValue with Boolean and box Content.
            Assert(contents.hasValue()),
            (new_grocery := GroceryItem()).decode(contents.value()),
            (item := abi.String()).set(new_grocery.item),
            (amount := abi.Uint8()).set(new_grocery.amount),
            (purchased := abi.Bool()).set(Int(1)),
            # We've gotta set all of the fields at the same time, but we can
            # borrow the item we already know about
            new_grocery.set(item, amount, purchased),
            Assert(App.box_delete(item_name.get())),
            App.box_put(item_name.get(), new_grocery.encode()),
            output.decode(new_grocery.encode())
        )

### Read Groceries ###

@router.method
def readAll(item_name: abi.String, *, output: GroceryItem) -> Expr:
    return Seq(
            contents := App.box_get(item_name.get()), # box_get returns a maybeValue with Boolean and box Content.
            Assert(contents.hasValue()),
            output.decode(contents.value()), ### TODO
        ) 

@router.method
def readItem(item_name: abi.String, *, output: abi.String) -> Expr:
    return Seq(
            contents := App.box_get(item_name.get()), # box_get returns a maybeValue with Boolean and box Content.
            Assert(contents.hasValue()),
            (val := GroceryItem()).decode(contents.value()),
            output.set(val.item),
        )  

@router.method
def readPurchased(item_name: abi.String, *, output: abi.Bool) -> Expr:
    return Seq(
            contents := App.box_get(item_name.get()), # box_get returns a maybeValue with Boolean and box Content.
            Assert(contents.hasValue()),
            (val := GroceryItem()).decode(contents.value()),
            output.set(val.purchased),
        )  

@router.method
def readAmount(item_name: abi.String, *, output: abi.Uint8) -> Expr:
    return Seq(
            contents := App.box_get(item_name.get()), # box_get returns a maybeValue with Boolean and box Content.
            Assert(contents.hasValue()),
            (val := GroceryItem()).decode(contents.value()),
            output.set(val.amount),
        )  

### delete ###

@router.method
def deleteGrocery(item_name: abi.String) -> Expr:
    return Assert(App.box_delete(item_name.get()))


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




