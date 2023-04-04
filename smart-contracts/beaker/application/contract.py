from beaker import *
from pyteal import *


class SimpleApp(Application):
    app_state = ApplicationStateValue(
        stack_type=TealType.uint64,
        default=Int(1),
    )

    @create
    def create(self):
        return self.initialize_application_state()


if __name__ == "__main__":
    SimpleApp().dump()
