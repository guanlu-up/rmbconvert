from rmbconvert import Traditional


def test_traditional(values: list):
    for value in values:
        rmb = Traditional(value)
        integer = rmb.to_number()
        print("原始大写金额: [{}]  转换后的小写金额: [{}]".format(value, integer))


upper_values = [
    "伍佰叁拾玖万零贰拾壹元叁角伍分",
    "柒仟陆佰零捌万玖仟贰佰叁拾壹元零贰分",
    "叁拾贰万伍仟玖佰玖拾壹元整",
    "壹仟零壹拾万壹仟零壹拾元陆角柒分",
    "壹仟壹佰壹拾壹万壹仟壹佰壹拾壹元壹角壹分",
]

line = "*" * 20
print(line, "大写转小写", line)
test_traditional(upper_values)
print("\n")
