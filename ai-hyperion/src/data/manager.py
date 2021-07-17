manager = {
    "owner": [
        "***",
        "***"
    ],
    "admin": [
        "***"
    ]
}


def is_permission_valid(user_id: str) -> bool:
    return user_id in (manager['owner'] + manager['admin'])
