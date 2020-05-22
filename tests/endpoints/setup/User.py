from django.contrib.auth.models import Permission, User


def create_user_with_permissions(*, username: str, permissions: list) -> User:
    user = User.objects.create_user(username=username, password=username)

    for permission in permissions:
        app_label, codename = permission.split(".")
        user.user_permissions.add(Permission.objects.get(content_type__app_label=app_label, codename=codename))

    return user
