#!/usr/bin/env python3
from pyteal import *
from beaker import *
from common import Vote, submit_votes
import os


class LocalVote(Vote):
    votes = AccountStateValue(stack_type=TealType.uint64)

    @external
    def submit_vote(self, vote: abi.Bool):
        return Seq(self.votes[Txn.sender()].set(vote.get()), Approve())


if __name__ == "__main__":
    if os.path.exists("local.teal"):
        os.remove("local.teal")

    app = LocalVote(version=8)

    with open("local.teal", "w") as f:
        f.write(app.approval_program)

    submit_votes(LocalVote(version=8))
