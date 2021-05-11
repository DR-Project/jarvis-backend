from operator import itemgetter

mem_***s = {}
mem_dicts = {
    '丢***': '***',
    '丢***': '***',
    '丢***': '***',
    '丢***': '***',
    '丢***': '***',
    '丢***': '***',
    '丢***': '***',
    '丢***': '***'
}


async def set_***_to_dict(qq: int, nick: str) -> int:
    if qq not in mem_***s.keys():
        mem_***s[qq] = {
            'count': 1,
            'nick': nick
        }
        return 1
    else:
        mem_***s[qq]['count'] += 1
        return 1


def get_***_report() -> str:
    mem_list = []
    msg = '今日***排行' + '\n\n'
    index = 1
    for qq in mem_***s.values():
        mem_list.append(qq)

    data = sorted(mem_list, key=itemgetter('count'))
    data.reverse()

    for i in data:
        msg += str(index) + '. ' + i['nick'] + ' -> ' + str(i['count']) + '根\n'
        index += 1

    return msg


def to_be_or_not_be(probability: int) -> bool:
    if probability >= 100:
        return True
    if probability < 0:
        return False

    import random

    ret = random.randint(0, 100)

    return ret <= probability


if __name__ == '__main__':
    p = []
    for i in range(100):
        p.append(to_be_or_not_be(99))

    print(False in p)