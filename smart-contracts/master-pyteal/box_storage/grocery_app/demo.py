import os

from algosdk.v2client.algod import *
from algosdk.atomic_transaction_composer import *
from algosdk.abi import *
from algosdk.mnemonic import *
from algosdk.account import *
from algosdk.transaction import *
from algosdk.logic import get_application_address

from sandbox import get_accounts

# Need to define helper function
def create_app(
    client,
    sender,
    private_key,
    approval_program,
    clear_program,
    global_schema,
    local_schema,
):

    # declare on_complete as NoOp
    on_complete = transaction.OnComplete.NoOpOC.real

    # get node suggested parameters
    params = client.suggested_params()
    # comment out the next two (2) lines to use suggested fees
    # params.flat_fee = True
    # params.fee = 1000

    # create unsigned transaction
    txn = transaction.ApplicationCreateTxn(
        sender,
        params,
        on_complete,
        approval_program,
        clear_program,
        global_schema,
        local_schema,
    )

    # sign transaction
    signed_txn = txn.sign(private_key)
    tx_id = signed_txn.transaction.get_txid()

    # send transaction
    client.send_transactions([signed_txn])

    # await confirmation

    confirmed_txn = transaction.wait_for_confirmation(client, tx_id, 4)
    print("TXID: ", tx_id)
    print("Result confirmed in round: {}".format(confirmed_txn["confirmed-round"]))

    # display results
    transaction_response = client.pending_transaction_info(tx_id)
    app_id = transaction_response["application-index"]
    print("Created new app-id: ", app_id)

    return app_id


def compile_program(client, source_code):
    compile_response = client.compile(source_code)
    return base64.b64decode(compile_response["result"])


# Manually setup Algod Client
client = AlgodClient("a" * 64, "http://localhost:4001")

addr, sk = get_accounts()[0]

path = os.path.dirname(os.path.abspath(__file__))

# Read in approval and clear TEAL programs
with open(os.path.join(path, "artifacts/approval.teal")) as f:
    approval_source = f.read()

with open(os.path.join(path, "artifacts/clear.teal")) as f:
    clear_source = f.read()

# Compile approval and clear TEAL programs
approval_program = compile_program(client, approval_source)
clear_program = compile_program(client, clear_source)

# declare application state storage (immutable)
local_ints = 0
local_bytes = 0
global_ints = 0
global_bytes = 0

# define schema
global_schema = transaction.StateSchema(global_ints, global_bytes)
local_schema = transaction.StateSchema(local_ints, local_bytes)

# create new application
app_id = create_app(
    client,
    addr,
    sk,
    approval_program,
    clear_program,
    global_schema,
    local_schema,
)

# read json and create ABI Contract description
with open(os.path.join(path, "artifacts/contract.json")) as f:
    js = f.read()
c = Contract.from_json(js)

signer = AccountTransactionSigner(sk)

comp = AtomicTransactionComposer()

app_addr = get_application_address(app_id)

sp = client.suggested_params()
ptxn = PaymentTxn(addr, sp, app_addr, 10000000)

ptxn_signer = TransactionWithSigner(ptxn, signer)
comp.add_transaction(ptxn_signer)

comp.add_method_call(
    app_id, c.get_method_by_name("addGrocery"), addr, sp, signer, method_args=["apple", 10], boxes=[(app_id, b"apple")]
)

comp.add_method_call(
    app_id, c.get_method_by_name("readAll"), addr, sp, signer, method_args=["apple"], boxes=[(app_id, b"apple")]
)

comp.add_method_call(
    app_id, c.get_method_by_name("readItem"), addr, sp, signer, method_args=["apple"], boxes=[(app_id, b"apple")]
)

comp.add_method_call(
    app_id, c.get_method_by_name("readAmount"), addr, sp, signer, method_args=["apple"], boxes=[(app_id, b"apple")]
)

comp.add_method_call(
    app_id, c.get_method_by_name("readPurchased"), addr, sp, signer, method_args=["apple"], boxes=[(app_id, b"apple")]
)

comp.add_method_call(
    app_id, c.get_method_by_name("updateAmount"), addr, sp, signer, method_args=["apple", 20], boxes=[(app_id, b"apple")]
)

comp.add_method_call(
    app_id, c.get_method_by_name("updatePurchased"), addr, sp, signer, method_args=["apple"], boxes=[(app_id, b"apple")]
)

comp.add_method_call(
    app_id, c.get_method_by_name("deleteGrocery"), addr, sp, signer, method_args=["apple"], boxes=[(app_id, b"apple")]
)

resp = comp.execute(client, 2)
for result in resp.abi_results:
    print(f"{result.method.name} => {result.return_value}")
