#!/usr/bin/env python3
from pyteal import *
from beaker import *
from beaker.lib.storage import Mapping
from common import Vote, submit_votes
import os


class BoxVote(Vote):
    votes = Mapping(abi.Address, abi.Bool)

    @external
    def submit_vote(self, vote: abi.Bool):
        return Seq(self.votes[Txn.sender()].set(Itob(vote.get())), Approve())


if __name__ == "__main__":
    if os.path.exists("box.teal"):
        os.remove("box.teal")

    app = BoxVote(version=8)

    with open("box.teal", "w") as f:
        f.write(app.approval_program)

    submit_votes(BoxVote(version=8))
