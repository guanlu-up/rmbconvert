from rmbconvert import Traditional, Number


def test_traditional(values: list):
    for value in values:
        rmb = Traditional(value)
        integer = rmb.to_number()
        normal = rmb.to_normal()
        message = """原始金额: {:25s} to normal: {:25s} to number: {:20s}  """
        print(message.format(value, normal, str(integer)))


def test_number(values: list):
    for value in values:
        rmb = Number(value)
        traditional = rmb.to_traditional()
        message = """原始金额: {:25s} to traditional: {:25s}"""
        print(message.format(str(value), traditional))


upper_values = [
    "伍佰叁拾玖万零贰拾壹元叁角伍分",
    "柒仟陆佰零捌万玖仟贰佰叁拾壹元零贰分",
    "叁拾贰万伍仟玖佰玖拾壹元整",
    "壹仟零壹拾万壹仟零壹拾元陆角柒分",
    "壹仟壹佰壹拾壹万壹仟壹佰壹拾壹元壹角壹分",
]

number_values = [
    5390021.35,
    76089231.02,
    325991,
    10101010.67,
    11111111.11,
    4022999303,
]


def main():
    line = "*" * 30
    print(line, "大写转小写", line)
    test_traditional(upper_values)
    print(line, "小写转大写", line)
    test_number(number_values)


if __name__ == '__main__':
    main()

