from typing import Optional

import reflex as rx
from LAHACKS.db_model import User

class State(rx.State):
    """The base state for the app."""

    user: Optional[User] = None

    def logout(self):
        """Log out a user."""
        self.reset()
        return rx.redirect("/login")

    def check_login(self):
        """Check if a user is logged in."""
        if not self.signed_in:
            return rx.redirect("/login")

    @rx.var
    def signed_in(self):
        """Check if a user is logged in."""
        return self.user is not None
