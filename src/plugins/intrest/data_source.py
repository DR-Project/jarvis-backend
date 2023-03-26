def to_be_or_not_be(probability: int) -> bool:
    """

    :param probability: 概率
    :return: bool
    """
    if probability >= 100:
        return True
    if probability < 0:
        return False

    import random

    ret = random.randint(0, 100)

    return ret <= probability


if __name__ == '__main__':
    # test code
    p = []
    for i in range(100):
        p.append(to_be_or_not_be(99))

    print(False in p)