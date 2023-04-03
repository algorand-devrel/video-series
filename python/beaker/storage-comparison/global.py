#!/usr/bin/env python3
from pyteal import *
from beaker import *
from common import Vote, submit_votes
import os


class GlobalVote(Vote):
    votes = ReservedApplicationStateValue(stack_type=TealType.uint64, max_keys=63)

    @external
    def submit_vote(self, vote: abi.Bool):
        return Seq(self.votes[Txn.sender()].set(vote.get()), Approve())


if __name__ == "__main__":
    if os.path.exists("global.teal"):
        os.remove("global.teal")

    app = GlobalVote(version=8)

    with open("global.teal", "w") as f:
        f.write(app.approval_program)

    submit_votes(GlobalVote(version=8))
