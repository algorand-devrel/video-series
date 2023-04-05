import base64
import datetime
import json

from algosdk import account, mnemonic, transaction
from algosdk.v2client import algod

from sandbox import get_accounts

algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

# declare application state storage (immutable)
local_ints = 1
local_bytes = 1
global_ints = 1
global_bytes = 0
global_schema = transaction.StateSchema(global_ints, global_bytes)
local_schema = transaction.StateSchema(local_ints, local_bytes)


# user declared approval program (initial)
def get_approval_program_initial(creator: str) -> str:
    return f"""#pragma version 6
// Handle each possible OnCompletion type. We don't have to worry about
// handling ClearState, because the ClearStateProgram will execute in that
// case, not the ApprovalProgram.

txn OnCompletion
int NoOp
==
bnz handle_noop

txn OnCompletion
int OptIn
==
bnz handle_optin

txn OnCompletion
int CloseOut
==
bnz handle_closeout

txn OnCompletion
int UpdateApplication
==
bnz handle_updateapp

txn OnCompletion
int DeleteApplication
==
bnz handle_deleteapp

// Unexpected OnCompletion value. Should be unreachable.
err

handle_noop:
// Handle NoOp
// Check for creator
addr {creator} 
txn Sender
==
bnz handle_optin

// read global state
byte "counter"
dup
app_global_get

// increment the value
int 1
+

// store to scratch space
dup
store 0

// update global state
app_global_put

// read local state for sender
int 0
byte "counter"
app_local_get

// increment the value
int 1
+
store 1

// update local state for sender
int 0
byte "counter"
load 1
app_local_put

// load return value as approval
load 0
return

handle_optin:
// Handle OptIn
// approval
int 1
return

handle_closeout:
// Handle CloseOut
//approval
int 1
return

handle_deleteapp:
// Check for creator
addr {creator} 
txn Sender
==
return

handle_updateapp:
// Check for creator
addr {creator} 
txn Sender
==
return

"""


# user declared approval program (refactored)
def get_approval_program_refactored(creator: str) -> str:
    return f"""#pragma version 6
// Handle each possible OnCompletion type. We don't have to worry about
// handling ClearState, because the ClearStateProgram will execute in that
// case, not the ApprovalProgram.

txn OnCompletion
int NoOp
==
bnz handle_noop

txn OnCompletion
int OptIn
==
bnz handle_optin

txn OnCompletion
int CloseOut
==
bnz handle_closeout

txn OnCompletion
int UpdateApplication
==
bnz handle_updateapp

txn OnCompletion
int DeleteApplication
==
bnz handle_deleteapp

// Unexpected OnCompletion value. Should be unreachable.
err

handle_noop:
// Handle NoOp
// Check for creator
addr {creator} 
txn Sender
==
bnz handle_optin

// read global state
byte "counter"
dup
app_global_get

// increment the value
int 1
+

// store to scratch space
dup
store 0

// update global state
app_global_put

// read local state for sender
int 0
byte "counter"
app_local_get

// increment the value
int 1
+
store 1

// update local state for sender
// update "counter"
int 0
byte "counter"
load 1
app_local_put

// update "timestamp"
int 0
byte "timestamp"
txn ApplicationArgs 0
app_local_put

// load return value as approval
load 0
return

handle_optin:
// Handle OptIn
// approval
int 1
return

handle_closeout:
// Handle CloseOut
//approval
int 1
return

handle_deleteapp:
// Check for creator
addr {creator} 
txn Sender
==
return

handle_updateapp:
// Check for creator
addr {creator} 
txn Sender
==
return
"""


# declare clear state program source
clear_program_source = """#pragma version 6
int 1
"""


# helper function to compile program source
def compile_program(client, source_code):
    compile_response = client.compile(source_code)
    return base64.b64decode(compile_response["result"])


# helper function that converts a mnemonic passphrase into a private signing key
def get_private_key_from_mnemonic(mn):
    private_key = mnemonic.to_private_key(mn)
    return private_key


# create new application
def create_app(
    client, private_key, approval_program, clear_program, global_schema, local_schema
):
    # define sender as creator
    sender = account.address_from_private_key(private_key)

    # declare on_complete as NoOp
    # https://developer.algorand.org/docs/get-details/dapps/avm/teal/specification/#oncomplete
    on_complete = transaction.OnComplete.NoOpOC.real

    # get node suggested parameters
    params = client.suggested_params()

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


# opt-in to application
def opt_in_app(client, private_key, index):
    # declare sender
    sender = account.address_from_private_key(private_key)
    print("OptIn from account: ", sender)

    # get node suggested parameters
    params = client.suggested_params()

    # create unsigned transaction
    txn = transaction.ApplicationOptInTxn(sender, params, index)

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
    print("OptIn to app-id: ")
    print(json.dumps(transaction_response["txn"]["txn"]["apid"], indent=2))


# call application
def call_app(client, private_key, index, app_args):
    # declare sender
    sender = account.address_from_private_key(private_key)
    print("Call from account: ", sender)

    # get node suggested parameters
    params = client.suggested_params()
    # comment out the next two (2) lines to use suggested fees
    # params.flat_fee = True
    # params.fee = 1000

    # create unsigned transaction
    txn = transaction.ApplicationNoOpTxn(sender, params, index, app_args)

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
    print("Called app-id: ", transaction_response["txn"]["txn"]["apid"])
    if "global-state-delta" in transaction_response:
        print("Global State updated :\n")
        print(json.dumps(transaction_response["global-state-delta"], indent=2))
    if "local-state-delta" in transaction_response:
        print("Local State updated :\n")
        print(json.dumps(transaction_response["local-state-delta"], indent=2))


# read user local state
def read_local_state(client, addr, app_id):
    results = client.account_info(addr)
    local_state = results["apps-local-state"][0]
    for index in local_state:
        if local_state[index] == app_id:
            print(f"local_state of account {addr} for app_id {app_id}: ")


# read app global state
def read_global_state(client, addr, app_id):
    results = client.account_info(addr)
    apps_created = results["created-apps"]
    for app in apps_created:
        if app["id"] == app_id:
            print(f"global_state for app_id {app_id}: ")
            print(json.dumps(app["params"]["global-state"], indent=2))


# update existing application
def update_app(client, private_key, app_id, approval_program, clear_program):
    # declare sender
    sender = account.address_from_private_key(private_key)

    # define initial value for key "timestamp"
    app_args = [b"initial value"]

    # get node suggested parameters
    params = client.suggested_params()

    # create unsigned transaction
    txn = transaction.ApplicationUpdateTxn(
        sender, params, app_id, approval_program, clear_program, app_args
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
    app_id = transaction_response["txn"]["txn"]["apid"]
    print("Updated existing app-id: ", app_id)


# delete application
def delete_app(client, private_key, index):
    # declare sender
    sender = account.address_from_private_key(private_key)

    # get node suggested parameters
    params = client.suggested_params()

    # create unsigned transaction
    txn = transaction.ApplicationDeleteTxn(sender, params, index)

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
    print("Deleted app-id: ", transaction_response["txn"]["txn"]["apid"])


# close out from application
def close_out_app(client, private_key, index):
    # declare sender
    sender = account.address_from_private_key(private_key)

    # get node suggested parameters
    params = client.suggested_params()

    # create unsigned transaction
    txn = transaction.ApplicationCloseOutTxn(sender, params, index)

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
    print("Closed out from app-id: ")
    print(json.dumps(transaction_response["txn"]["txn"]["apid"], indent=2))


# clear application
def clear_app(client, private_key, index):
    # declare sender
    sender = account.address_from_private_key(private_key)

    # get node suggested parameters
    params = client.suggested_params()

    # create unsigned transaction
    txn = transaction.ApplicationClearStateTxn(sender, params, index)

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
    print("Cleared app-id: ")
    print(json.dumps(transaction_response["txn"]["txn"]["apid"], indent=2))


def main():
    accts = get_accounts()

    creator_address, creator_sk = accts.pop()
    user_address, user_sk = accts.pop()
    print("Creator Address :", creator_address)
    print("User Address :", user_address)

    # initialize an algodClient
    algod_client = algod.AlgodClient(algod_token, algod_address)

    approval_program = compile_program(
        algod_client, get_approval_program_initial(creator_address)
    )
    clear_program = compile_program(algod_client, clear_program_source)

    # create new application
    # limit 10 appid's per account - ApplicationCreateTxn
    app_id = create_app(
        algod_client,
        creator_sk,
        approval_program,
        clear_program,
        global_schema,
        local_schema,
    )

    # opt-in to application - ApplicationOptInTxn
    opt_in_app(algod_client, user_sk, app_id)

    # call application without arguments - ApplicationNoOpTxn
    call_app(algod_client, user_sk, app_id, None)

    # read local state of application from user account
    read_local_state(algod_client, account.address_from_private_key(user_sk), app_id)

    # read global state of application
    read_global_state(
        algod_client, account.address_from_private_key(creator_sk), app_id
    )

    # update application - ApplicationUpdateTxn
    approval_program = compile_program(
        algod_client, get_approval_program_refactored(creator_address)
    )
    update_app(algod_client, creator_sk, app_id, approval_program, clear_program)

    # call application with arguments -
    now = datetime.datetime.now().strftime("%H:%M:%S")
    app_args = [now.encode("utf-8")]
    call_app(algod_client, user_sk, app_id, app_args)

    # read local state of application from user account
    read_local_state(algod_client, account.address_from_private_key(user_sk), app_id)

    # close-out from application - ApplicationCloseOutTxn
    close_out_app(algod_client, user_sk, app_id)

    # opt-in again to application - ApplicationOptInTxn
    opt_in_app(algod_client, user_sk, app_id)

    # call application with arguments - ApplicationNoOpTxn
    call_app(algod_client, user_sk, app_id, app_args)

    # read local state of application from user account
    read_local_state(algod_client, account.address_from_private_key(user_sk), app_id)

    # delete application - ApplicationDeleteTxn
    # clears global storage only
    # user must clear local
    delete_app(algod_client, creator_sk, app_id)

    # clear application from user account - ApplicationClearStateTxn
    # clears local storage
    clear_app(algod_client, user_sk, app_id)


main()
