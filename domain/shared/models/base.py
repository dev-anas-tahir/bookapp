import uuid

from piccolo.columns import UUID, Timestamp
from piccolo.columns.defaults.timestamp import TimestampNow
from piccolo.table import Table


class BaseTable(Table):
    """
    Base columns for all of the tables in the database
    """

    id = UUID(primary_key=True, default=uuid.uuid4)
    created_at = Timestamp(TimestampNow(), null=False)
    updated_at = Timestamp(
        TimestampNow(), auto_update=TimestampNow, null=False
    )
    deleted_at = Timestamp(
        null=True, help_text="When was the record soft deleted (null if not deleted)"
    )

    class Meta:
        abstract = True
