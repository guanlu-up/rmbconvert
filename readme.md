## 人民币大小写转换

### - 快速使用 -
```python
from rmbconvert import Traditional, Number

rmb = Traditional("伍佰叁拾玖万零贰拾壹元叁角伍分")
# 转换为小写金额
print(rmb.to_number())  
# 转换为正常的大写金额
print(rmb.to_normal())

rmb = Number(5390021.35)
# 转换为标准大写金额
print(rmb.to_traditional())
```
###  - 测试一下 - 
```commandline
python.exe ./test.py
```
```python
import test
test.main()
```

### - 实现思路 -

- 标准大写金额转为数字
```text
>: 叁拾贰亿伍仟零捌拾万壹仟叁佰玖拾元整
>: [(叁 * 拾) (贰) (亿) (伍  * 仟) (捌 * 拾) (万) (壹 * 仟) (叁 * 佰) (玖 * 拾)]
>: [30, 2, 100000000, 5000, 80, 10000, 1000, 300, 90]
>: [((30 + 2) * 100000000) + ((5000 + 80) * 10000) + 1000 + 300 + 90]
>: [3200000000 + 50800000 + 1000 + 300 + 90]
>: [3250801390]
```
