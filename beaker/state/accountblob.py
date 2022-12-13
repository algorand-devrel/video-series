
from typing import Final
from beaker import (
    Application,
    opt_in,
    external,
)
from pyteal import abi, Int

from beaker.state import AccountStateBlob


class AccountBlobState(Application):

    account_blob: Final[AccountStateBlob] = AccountStateBlob(keys=3)

    @opt_in
    def opt_in(self):
        return self.initialize_account_state()

    @external
    def write_acct_blob(self, v: abi.String):
        return self.account_blob.write(Int(0), v.get())

    @external
    def read_acct_blob(self, *, output: abi.DynamicBytes):
        return output.set(
            self.account_blob.read(Int(0), self.account_blob.blob.max_bytes - Int(1))
        )


if __name__ == "__main__":
    se = AccountBlobState()