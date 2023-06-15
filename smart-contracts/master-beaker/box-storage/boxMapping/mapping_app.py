from beaker import *
from pyteal import *

from beaker.lib.storage import BoxMapping


# Our custom Struct
class GroceryItem(abi.NamedTuple):
    item: abi.Field[abi.String]
    purchased: abi.Field[abi.Bool]


class GroceryStates:
    grocery_item = BoxMapping(abi.String, GroceryItem)


app = Application("Grocery CheckList with Beaker", state=GroceryStates())


### Add Grocery with Boxes ###
@app.external
def addGrocery(item_name: abi.String) -> Expr:
    purchased = abi.Bool()
    grocery_tuple = GroceryItem()

    return Seq(
        purchased.set(Int(0)),
        grocery_tuple.set(item_name, purchased),
        app.state.grocery_item[item_name.get()].set(grocery_tuple),
    )


### Update Grocery Item ###
@app.external
def updatePurchased(item_name: abi.String, *, output: GroceryItem) -> Expr:
    existing_grocery_item = GroceryItem()
    new_purchased = abi.Bool()

    return Seq(
        existing_grocery_item.decode(app.state.grocery_item[item_name.get()].get()),
        new_purchased.set(Int(1)),
        existing_grocery_item.set(item_name, new_purchased),
        app.state.grocery_item[item_name.get()].set(existing_grocery_item),
        app.state.grocery_item[item_name.get()].store_into(output),
    )


### Read Grocery Item ###
@app.external
def readItem(item_name: abi.String, *, output: GroceryItem) -> Expr:
    return app.state.grocery_item[item_name.get()].store_into(output)


### delete ###
@app.external
def deleteGrocery(item_name: abi.String) -> Expr:
    return Pop(app.state.grocery_item[item_name.get()].delete())
