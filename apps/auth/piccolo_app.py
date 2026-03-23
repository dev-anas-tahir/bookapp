"""Piccolo app configuration for auth domain."""

import os

from piccolo.conf.apps import AppConfig

from apps.auth.models import (
    AuditLogs,
    FeatureFlag,
    Module,
    Permission,
    Role,
    RolePermission,
    User,
    UserPermission,
    UserRole,
)

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

APP_CONFIG = AppConfig(
    app_name="auth",
    migrations_folder_path=os.path.join(CURRENT_DIRECTORY, "piccolo_migrations"),
    table_classes=[
        User,
        Role,
        Permission,
        Module,
        UserRole,
        RolePermission,
        UserPermission,
        AuditLogs,
        FeatureFlag,
    ],
)
