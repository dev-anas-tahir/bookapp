from piccolo.columns import Date, Varchar
from piccolo.columns.readable import Readable

from .base import BaseTable


class User(BaseTable):
    """
    User model representing application users.
    """

    email = Varchar(length=255, unique=True, null=False)
    first_name = Varchar(length=100, null=False)
    last_name = Varchar(length=100, null=False)
    date_of_birth = Date(
        null=False,
        help_text="User's date of birth (YYYY-MM-DD format)",
    )

    @classmethod
    def readable(cls):
        return Readable(
            template="%s %s <%s>", columns=[cls.first_name, cls.last_name, cls.email]
        )

    class Meta:
        tablename = "users"
