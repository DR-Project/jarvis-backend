from nonebot import get_driver

from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())


def is_permission_valid(user_id: int) -> bool:
    managers = config.managers
    return user_id in (managers['owner'] + managers['admin'])
