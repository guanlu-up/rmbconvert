from rmbconvert import constants


__all__ = ["Traditional"]


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
    """ 人民币标准的大写金额

    example:
        rmb = Traditional("伍佰叁拾玖万零贰拾壹元叁角伍分")
        print(rmb.to_number())

    """

    def __init__(self, amount: str):
        self.value = amount

    def to_number(self):
        """
        --------------实现方式--------------
        >: 叁拾贰亿伍仟零捌拾万壹仟叁佰玖拾元整
        >: [(叁 * 拾) (贰) (亿) (伍  * 仟) (捌 * 拾) (万) (壹 * 仟) (叁 * 佰) (玖 * 拾)]
        >: [30, 2, 100000000, 5000, 80, 10000, 1000, 300, 90]
        >: [((30 + 2) * 100000000) + ((5000 + 80) * 10000) + 1000 + 300 + 90]
        >: [3200000000 + 50800000 + 1000 + 300 + 90]
        >: 3250801390
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
            max_index = groups.index(max(groups[start_index:]))
            add = sum(groups[start_index:max_index])
            if add != 0:
                mul.append(add * groups[max_index])
            else:
                mul.append(groups[max_index])
            if (len(groups) - 1) == max_index:
                break
            start_index = max_index + 1

        return sum(mul)

    @staticmethod
    def _convert_decimal(amount: str):
        """转换小数部分"""
        result = 0.0
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
