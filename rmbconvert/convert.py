from typing import Union

from rmbconvert import constants


__all__ = ["Traditional", "Number"]


class RMBUpper(object):
    """人民币大写的字符类, 用于数字单位和进位的比较

    > RMBUpper("佰") < RMBUpper("仟")
    > RMBUpper("叁") > RMBUpper("贰")
    > RMBUpper("伍") == RMBUpper("伍")
    """

    def __init__(self, unit: str):
        if not isinstance(unit, str) or len(unit) != 1:
            raise ValueError(f"invalid params: {unit}")

        units = dict(**constants.UNIT_UPPER, **constants.DIGIT_UPPER)
        sort = sorted(units.items(), key=lambda x: x[1])
        self.units = [group[0] for group in sort]
        self.value = unit
        self.number = units.get(self.value)

    def __str__(self):
        return f"<RMBUpper({self.value})>"

    def __repr__(self):
        return f"<RMBUpper({self.value})>"

    def __gt__(self, other):
        if other not in self.units:
            return False
        return self.units.index(self.value) > self.units.index(other)

    def __lt__(self, other):
        if other not in self.units:
            return False
        return self.units.index(self.value) < self.units.index(other)

    def __eq__(self, other):
        return self.value == other


class Traditional(object):
    """ 人民币标准大写金额的相关转换

    example:
        rmb = Traditional("伍佰叁拾玖万零贰拾壹元叁角伍分")
        print(rmb.to_number())

    """

    def __init__(self, amount: str):
        self.value = amount

    def to_normal(self):
        """返回转换后的正常大写金额"""

        strings = []
        upper_units = dict(**constants.UNIT_UPPER, **constants.DIGIT_UPPER)
        normal_units = dict(**constants.UNIT_NORMAL, **constants.DIGIT_NORMAL)
        mapping = dict(zip(upper_units.keys(), normal_units.keys()))

        for unit in self.value:
            strings.append(mapping.get(unit, unit))
        return "".join(strings)

    def to_number(self):
        """返回转换后的数字金额

        实现思路:
            >: 叁拾贰亿伍仟零捌拾万壹仟叁佰玖拾元整
            >: [(叁 * 拾) (贰) (亿) (伍  * 仟) (捌 * 拾) (万) (壹 * 仟) (叁 * 佰) (玖 * 拾)]
            >: [30, 2, 100000000, 5000, 80, 10000, 1000, 300, 90]
            >: [((30 + 2) * 100000000) + ((5000 + 80) * 10000) + 1000 + 300 + 90]
            >: [3200000000 + 50800000 + 1000 + 300 + 90]
            >: [3250801390]
        """

        positive_number, fraction = self.value, None
        if "元" in self.value:
            positive_number, fraction = self.value.split("元")

        positive_number = positive_number.replace("零", "")

        integer = self._convert_integer(positive_number)
        decimal = self._convert_decimal(fraction)

        return integer + decimal

    @staticmethod
    def _convert_integer(amount: str):
        """转换整数部分"""
        instances = [RMBUpper(unit) for unit in amount]
        groups = []

        for index, instance in enumerate(instances):
            if not groups or len(groups[-1]) >= 2:
                groups.append([instance])
                continue

            if not groups[-1]:
                groups[-1].append(instance)
                continue

            # 当前字符单位为进位大写时
            if instance in list(constants.UNIT_UPPER.keys()):
                # 当groups中的组合小于2 或 上一个进位符比当前进位符大的时候
                if len(groups) < 2 or groups[-2][-1] > instance:
                    groups[-1].append(instance)
                # 当上一个进位符比当前进位符小的时候
                elif groups[-2][-1] < instance:
                    groups.append([instance])

            # 当前字符单位为数字大写时
            elif instance in list(constants.DIGIT_UPPER.keys()):
                # 当最后一组中的第一个值为进位符时就不能组合在一起
                if groups[-1][0] in list(constants.UNIT_UPPER.keys()):
                    groups.append([instance])
                else:
                    groups[-1].append(instance)

        # 将RMBUpper()转换为number
        for index in range(len(groups)):
            units = groups[index]
            if len(units) == 1:
                _numbers = units[0].number
            else:
                _numbers = units[0].number * units[1].number
            groups[index] = _numbers

        # 从最大进位开始乘法运算
        mul = []
        start_index = 0
        while True:
            surplus = groups[start_index:]
            max_index = surplus.index(max(surplus))
            add = sum(surplus[:max_index])
            if add != 0:
                mul.append(add * surplus[max_index])
            else:
                mul.append(surplus[max_index])
            if (len(groups) - 1) <= start_index:
                break
            start_index += max_index + 1

        return sum(mul)

    @staticmethod
    def _convert_decimal(amount: str):
        """转换小数部分"""
        result = 0
        mul = None

        for unit in amount:
            # 当前字符单位为数字大写时
            if unit in constants.DIGIT_UPPER.keys():
                mul = constants.DIGIT_UPPER.get(unit)
            # 当前字符单位为进位大写时
            elif unit in constants.UNIT_UPPER.keys():
                carry = constants.UNIT_UPPER.get(unit)
                result += (mul * carry)

        return result


class Number(object):
    """数字金额的相关转换

    example:
        rmb = Number(5390021.35)
        print(rmb.to_traditional())
    """

    def __init__(self, amount: Union[int, float]):
        self.value = amount
        self._digits = {value: key for key, value in constants.DIGIT_UPPER.items()}
        self._digits.update({0: '零'})

    def to_traditional(self):
        """返回转换后的标准人民币大写金额

        实现思路:
            利用函数的递归调用动态的解析数值

            >: 12345678
            >: [12340000, 5000, 600, 70, 8]
            >: [((1000 + 200 + 30 + 4) * (10000)) + (5000) + (600) + (70) + (8)]
            >: [((壹仟 + 贰佰 + 叁拾 + 肆) * (壹万)) + (伍仟) + (陆佰) + (柒拾) + (捌)]
            >: [壹仟贰佰叁拾肆万伍仟陆佰柒拾捌]
        """

        amount = str(int(self.value))

        _integer = self._analysis_integer(amount)
        if isinstance(self.value, int) or self.value.is_integer():
            return _integer + "整"
        _decimal = self._analysis_decimal(str(self.value).split(".")[-1])
        return _integer + _decimal

    def to_normal(self):
        traditional = self.to_traditional()
        rmb = Traditional(traditional)
        return rmb.to_normal()

    def _analysis_integer(self, value: str):
        strings = []
        max_unit_key = 1

        if int(value) == 0:
            return "零元"
        if value.startswith("0"):
            value = value.lstrip("0")
            strings.append(self._digits.get(0))

        # 获取amount的最大进位符
        for _len in reversed(sorted(constants.LENGTH.keys())):
            if len(value) >= _len:
                max_unit_key = _len
                break

        if not value[:-max_unit_key]:
            # 当最大的进位符前面没有更多的数值时, 增加进位符本身
            strings.append(self._digits.get(int(value[-max_unit_key])))
            if strings[-1] != self._digits.get(0):
                strings.append(constants.LENGTH.get(max_unit_key))
        else:
            # 当最大的进位符前面仍有数值时, 将数值取出并再次调用函数本身, 并把结果插入到最前面
            prefix = self._analysis_integer(value[:-max_unit_key + 1])
            strings.insert(0, prefix.replace("元", ""))
            strings.append(constants.LENGTH.get(max_unit_key))

        # 如果进位符单位为`元`或子级数值全部为0时则直接返回
        if max_unit_key == 1 or value[-max_unit_key + 1:] == "".zfill(len(value[-max_unit_key + 1:])):
            if strings[-1] != "元":
                strings.append("元")
            return "".join(strings)

        value = value[-max_unit_key + 1:]
        suffix = self._analysis_integer(value)
        strings.append(suffix)

        return "".join(strings)

    def _analysis_decimal(self, value: str):
        strings = []
        if value[0] == "0":
            strings.append(self._digits.get(0))
        else:
            strings.append(self._digits.get(int(value[0])))
            strings.append("角")
        if len(value) < 2:
            return "".join(strings)
        strings.append(self._digits.get(int(value[1])))
        strings.append("分")
        return "".join(strings)
