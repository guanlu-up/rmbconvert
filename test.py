from rmbconvert import Traditional


def test_traditional(values: list):
    for value in values:
        rmb = Traditional(value)
        integer = rmb.to_number()
        normal = rmb.to_normal()
        message = """原始金额: {:25s} to normal: {:25s} to number: {:20s}  """
        print(message.format(value, normal, str(integer)))


upper_values = [
    "伍佰叁拾玖万零贰拾壹元叁角伍分",
    "柒仟陆佰零捌万玖仟贰佰叁拾壹元零贰分",
    "叁拾贰万伍仟玖佰玖拾壹元整",
    "壹仟零壹拾万壹仟零壹拾元陆角柒分",
    "壹仟壹佰壹拾壹万壹仟壹佰壹拾壹元壹角壹分",
]

line = "*" * 30
print(line, "大写转小写", line)
test_traditional(upper_values)
print("\n")
