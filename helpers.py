"""
General helper methods
"""


def percentage_formatted(per):
    # Takes percentage 0-1, returns formatted percentage
    # 0-100, 2 decimal points, format: "xx.xx%"

    return "{:0.2f}%".format(per * 100)


def print_dict(d: dict) -> str:
    # returns items in "key: value" format, separated by lines

    return "".join(["{}: {}\n".format(k, v) for k, v in d.items()])
