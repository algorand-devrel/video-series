from pyteal import *

router = Router(
    "pyteal-expression-example",
    BareCallActions(
        no_op=OnCompleteAction.create_only(Approve())
    )
)

@router.method
def create_count():
    return Seq(
        App.globalPut(Bytes("count"), Int(1)),
        Approve()
    )

if __name__ == "__main__":

    try:
        approval, clear, contract = router.compile_program(version=8)
        print("App is successfully compiled!")
    except AttributeError as e:
        print(e)