import random


def generate_color():
    return "#" + "".join([random.choice("0123456789ABCDEF") for _ in range(6)])
