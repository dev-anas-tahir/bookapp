from piccolo.columns import Boolean, Date, ForeignKey, Varchar
from piccolo.columns.readable import Readable

from apps.shared.models.base import BaseTable


class User(BaseTable):
    """
    User model representing application users.
    """

    email = Varchar(length=255, unique=True, null=False)
    first_name = Varchar(length=100, null=False)
    last_name = Varchar(length=100, null=False)
    password = Varchar(length=255, null=False)
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


class Role(BaseTable):
    """
    Role model representing application roles.
    """

    name = Varchar(length=100, unique=True, null=False)

    class Meta:
        tablename = "roles"


class Permission(BaseTable):
    """
    Permission model representing application permissions.
    """

    name = Varchar(length=100, unique=True, null=False)

    class Meta:
        tablename = "permissions"


class Module(BaseTable):
    """
    Module model representing application modules.
    """

    name = Varchar(length=100, unique=True, null=False)

    class Meta:
        tablename = "modules"


class UserRole(BaseTable):
    """
    User-Role association model.
    """

    user = ForeignKey(User)
    role = ForeignKey(Role)

    class Meta:
        tablename = "user_roles"


class RolePermission(BaseTable):
    """
    Role-Permission association model.
    """

    role = ForeignKey(Role)
    permission = ForeignKey(Permission)

    class Meta:
        tablename = "role_permissions"


class UserPermission(BaseTable):
    """
    User-Permission association model.
    """

    user = ForeignKey(User)
    permission = ForeignKey(Permission)

    class Meta:
        tablename = "user_permissions"


class AuditLogs(BaseTable):
    """
    Audit logs model.
    """

    user = ForeignKey(User)
    action = Varchar(length=100, null=False)
    timestamp = Date(null=False)
    model_type = Varchar(length=100, null=False)
    model_id = Varchar(length=100, null=False)

    class Meta:
        tablename = "audit_logs"


class FeatureFlag(BaseTable):
    """
    Feature flag model.
    """

    name = Varchar(length=100, unique=True, null=False)
    enabled = Boolean(default=False, null=False)

    class Meta:
        tablename = "feature_flags"
