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