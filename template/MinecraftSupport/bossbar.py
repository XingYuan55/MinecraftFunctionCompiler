# -*- coding: utf-8 -*-
# cython: language_level = 3
# MCFC: Template
import json

from Template import NameNode
from Template import register_func
from MinecraftColorString import ColorString
from Constant import DECIMAL_PRECISION
from Constant import ScoreBoards


BossBar_Map = {}


def _CheckId(_id: str) -> str:
    if not isinstance(_id, str):
        raise TypeError("id must be str")
    if '\n' in _id:
        raise ValueError("id must not contain '\\n'")
    if ':' not in _id:
        _id = f"minecraft:{_id}"

    return _id


def _CheckName(name) -> ColorString:
    if isinstance(name, (dict, str)):
        return ColorString.from_dict(name)
    else:
        raise TypeError("name must be dict or str")


def _add(_id: str, name: dict | str):
    _id = _CheckId(_id)

    name = _CheckName(name)
    BossBar_Map[_id] = {"name": json.dumps(name.to_dict())}
    print(name.to_ansi()+"\033[0m")


@register_func(_add)
def add(_id: str, name: dict | str):
    _id = _CheckId(_id)
    json_name = json.dumps(_CheckName(name).to_dict())

    return f"bossbar add {_id} {json_name}\n"


def _remove(_id: str):
    _id = _CheckId(_id)
    try:
        BossBar_Map.pop(_id)
    except KeyError:
        pass


@register_func(_remove)
def remove(_id: str):
    _id = _CheckId(_id)

    return f"bossbar remove {_id}\n"


def _set_players(_id: str, players: str):
    _id = _CheckId(_id)
    BossBar_Map[_id]["players"] = players


@register_func(_set_players)
def set_players(_id: str, players: str):
    _id = _CheckId(_id)

    return f"bossbar set {_id} players {players}\n"


def _CheckValue(value: int | float):
    if isinstance(value, float):
        value = int(value * (10**DECIMAL_PRECISION))

    if not isinstance(value, int):
        raise TypeError("value must be int or float")

    if value < 0:
        raise ValueError("value must be positive")

    return value


def _set_value(_id: str, value: int | float):
    _id = _CheckId(_id)
    value = _CheckValue(value)

    BossBar_Map[_id]["value"] = value


@register_func(_set_value)
def set_value(_id: str, value: int | float | NameNode):
    _id = _CheckId(_id)

    if isinstance(value, NameNode):
        command = (
            f"execute store result bossbar {_id} value "
            f"run scoreboard players get {value.code} {ScoreBoards.Vars}\n"
        )
        return command

    value = _CheckValue(value)

    return f"bossbar set {_id} value {value}\n"


def _set_max(_id: str, _max: int | float):
    _id = _CheckId(_id)
    _max = _CheckValue(_max)

    BossBar_Map[_id]["max"] = _max


@register_func(_set_max)
def set_max(_id: str, _max: int | float | NameNode):
    _id = _CheckId(_id)

    if isinstance(_max, NameNode):
        command = (
            f"execute store result bossbar {_id} max "
            f"run scoreboard players get {_max.code} {ScoreBoards.Vars}\n"
        )
        return command

    _max = _CheckValue(_max)

    return f"bossbar set {_id} max {_max}\n"


def _set_name(_id: str, name: dict | str):
    _id = _CheckId(_id)
    name = _CheckName(name)
    BossBar_Map[_id]["name"] = json.dumps(name.to_dict())
    print(name.to_ansi()+"\033[0m")


@register_func(_set_name)
def set_name(_id: str, name: dict | str):
    _id = _CheckId(_id)

    return f"bossbar set {_id} name {json.dumps(_CheckName(name).to_dict())}\n"


allow_color = "blue|green|pink|purple|red|white|yellow".split("|")


def _CheckColor(color: str):
    if color not in allow_color:
        raise ValueError(f"color must be in {allow_color}")

    return color


def _set_color(_id: str, color: str):
    _id = _CheckId(_id)
    color = _CheckColor(color)
    BossBar_Map[_id]["color"] = color


@register_func(_set_color)
def set_color(_id: str, color: str):
    _id = _CheckId(_id)
    color = _CheckColor(color)
    return f"bossbar set {_id} color {color}\n"


allow_style = "notched_6|notched_10|notched_12|notched_20|progress".split("|")


def _CheckStyle(style: str | int):
    if isinstance(style, int):
        style = f"notched_{style}"

    if style not in allow_style:
        raise ValueError(f"style must be in {allow_style}")

    return style


def _set_style(_id: str, style: str | int):
    _id = _CheckId(_id)
    style = _CheckStyle(style)

    BossBar_Map[_id]["style"] = style


@register_func(_set_style)
def set_style(_id: str, style: str | int):
    _id = _CheckId(_id)
    style = _CheckStyle(style)

    return f"bossbar set {_id} style {style}\n"


def _set_visible(_id: str, visible: bool):
    _id = _CheckId(_id)
    BossBar_Map[_id]["visible"] = visible


@register_func(_set_visible)
def set_visible(_id: str, visible: bool):
    _id = _CheckId(_id)

    return f"bossbar set {_id} visible {visible}\n"


__all__ = (
    "add",
    "remove",

    "set_players",
    "set_value",
    "set_max",
    "set_name",
    "set_color",
    "set_style",
    "set_visible",
)
