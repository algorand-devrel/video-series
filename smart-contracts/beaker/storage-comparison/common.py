#!/usr/bin/env python3
from pyteal import *
from beaker import *
from algosdk.atomic_transaction_composer import AccountTransactionSigner
from algosdk.account import generate_account
from algosdk.encoding import decode_address


class Vote(Application):
    proposal = ApplicationStateValue(stack_type=TealType.bytes)

    @create
    def create(self):
        return Seq(self.proposal.set(Bytes("Buy NFTs?")), Approve())

    @opt_in
    def opt_in(self):
        return Approve()

    @external
    def submit_vote(self, vote: abi.Bool):
        return Reject()


def submit_votes(app):
    app_class = app.__class__.__name__
    creator = sandbox.get_accounts()[0]
    app_client = client.ApplicationClient(
        client=sandbox.get_algod_client(),
        app=app,
        sender=creator.address,
        signer=creator.signer,
    )
    app_client.create()

    print(app_client.app_id)

    try:
        addrs = []
        for _ in range(100):
            [sk, addr] = generate_account()
            addrs.append(addr)
            signer = AccountTransactionSigner(sk)

            if app_class == "LocalVote":
                # Fund the account with account MBR, fee, and MBR needed for opting in
                app_client.fund(230_500, addr)

                # Opt into app
                app_client.opt_in(sender=addr, signer=signer)
            elif app_class == "BoxVote":
                # Fund account with account MBR and fee
                app_client.fund(101_000, addr)

                # Fund contract with box MBR
                app_client.fund(118500)
            elif app_class == "GlobalVote":
                # Fund account with account MBR and fee
                app_client.fund(101_000, addr)

            app_client.call(
                method=app.submit_vote,
                vote=True,
                sender=addr,
                signer=signer,
                boxes=[(app_client.app_id, decode_address(addr))],
            )

    finally:
        if app_class == "GlobalVote":
            print(app_client.get_application_state())
        elif app_class == "LocalVote":
            # We must know all of the addresses to get all of the votes
            for a in addrs:
                print(f"{a}: {app_client.get_account_state(addr)}")
        elif app_class == "BoxVote":
            for box in app_client.get_box_names():
                print(f"{box}: {app_client.get_box_contents(box)}")
