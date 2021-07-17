managers = {
    "owner": [
        "***",
        "***"
    ],
    "admin": [
        "***"
    ]
}


def is_permission_valid(user_id: str) -> bool:
    return user_id in (managers['owner'] + managers['admin'])
