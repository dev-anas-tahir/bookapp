"""Database seeding script for Piccolo ORM."""

import sys
from pathlib import Path

import structlog

# Add the workspace root to Python path to enable 'app' imports
workspace_root = Path(__file__).parent.parent
if str(workspace_root) not in sys.path:
    sys.path.insert(0, str(workspace_root))

from apps.auth.models import Permission, Role, RolePermission  # noqa: E402

logger = structlog.get_logger()


async def get_or_create_role(name: str) -> Role:
    """Get existing role or create a new one."""
    # Check if role already exists
    existing = await Role.select().where(Role.name == name).first()
    if existing:
        logger.info(f"Role already exists: {name}")
        return Role(existing)

    # Create new role
    role = Role(name=name)
    await role.save()
    logger.info(f"Created role: {name}")
    return role


async def get_or_create_permission(name: str) -> Permission:
    """Get existing permission or create a new one."""
    # Check if permission already exists
    existing = await Permission.select().where(Permission.name == name).first()
    if existing:
        logger.info(f"Permission already exists: {name}")
        return Permission(existing)

    # Create new permission
    permission = Permission(name=name)
    await permission.save()
    logger.info(f"Created permission: {name}")
    return permission


async def assign_permission_to_role(role: Role, permission: Permission) -> None:
    """Assign permission to role if not already assigned."""
    # Check if assignment already exists
    existing = (
        await RolePermission.select()
        .where(
            (RolePermission.role == role.id)
            & (RolePermission.permission == permission.id)
        )
        .first()
    )

    if existing:
        return  # Already assigned

    # Create assignment
    role_permission = RolePermission(role=role.id, permission=permission.id)
    await role_permission.save()
    logger.info(f"Assigned {permission.name} → {role.name}")


async def seed() -> None:
    """Seed database with initial roles and permissions."""
    # Get the db
    db = Role._meta.db

    async with db.transaction():
        # ──────────── ROLES ──────────── #
        viewer = await get_or_create_role("viewer")
        admin = await get_or_create_role("admin")

        # ──────────── PERMISSIONS ──────────── #
        permission_names = [
            "user_view",
            "user_create",
            "user_update",
            "user_delete",
            "role_view",
            "role_create",
            "role_delete",
            "audit_view",
        ]

        created_permissions = []
        for name in permission_names:
            perm = await get_or_create_permission(name)
            created_permissions.append(perm)

        # ──────────── ASSIGN PERMISSIONS TO ROLES ──────────── #
        # viewer gets read-only permissions
        viewer_permissions = {"user_view", "role_view", "audit_view"}
        for perm in created_permissions:
            if perm.name in viewer_permissions:
                await assign_permission_to_role(viewer, perm)

        # admin gets everything
        for perm in created_permissions:
            await assign_permission_to_role(admin, perm)

    logger.info("Seed completed successfully")


async def main():
    """Entry point for seed script."""
    try:
        await seed()
    except Exception as e:
        logger.error(f"Seed failed: {e}")
        raise


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
