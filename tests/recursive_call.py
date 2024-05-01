from template.MinecraftSupport.builtin import tprint
from template.MinecraftSupport.scoreboard import get_score
from template.MinecraftSupport.EnvBuild import build_scoreboard


build_scoreboard(
    "num",
    {"value": 5}
)


def factorial(n):
    if n == 0:
        return 1
    else:
        value = n - 1
        tprint(value)
        ret = factorial(value)
        tprint(n, ret)
        return n * ret


# 测试
num = get_score("value", "num")
ret = factorial(num)
tprint(num, "的阶乘是: ", ret, sep='')
