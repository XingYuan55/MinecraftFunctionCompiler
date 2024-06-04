# -*- coding: utf-8 -*-
# cython: language_level = 3
"""
替换源码中的占位符
"""
import json
import os
from typing import Generator

from Configuration import GlobalConfiguration
from jinja2 import Environment, Undefined
from jinja2 import FileSystemLoader


def _has_value(value) -> bool:
    is_none = value is None
    is_undefined = isinstance(value, Undefined)
    return not (is_none or is_undefined)


def _translate(
        translate: str,
        fallback: str = None,
        *,
        click_event: str = None,
        hover_event: str = None,
        color: str = None,
):
    translate = f"python_interpreter.{translate}"

    if not _has_value(fallback):
        fallback = "§4§lTranslation missing: §e§o{}".format(translate)

    data = {"type": "translatable", "translate": translate, "fallback": fallback}

    if _has_value(click_event):
        data["clickEvent"] = json.loads(click_event)

    if _has_value(hover_event):
        data["hoverEvent"] = json.loads(hover_event)

    if _has_value(color):
        data["color"] = color

    return json.dumps(data)


def _nbt(
        source: str,
        nbt: str = "",
        *,
        storage: str = None,
        interpret: bool = None,
        click_event: str = None,
        hover_event: str = None,
        color: str = None,
):
    data = {"type": "nbt", "nbt": nbt, "source": source}

    if source == "storage":
        if not _has_value(storage):
            raise ValueError("storage is required when source is storage")
        data["storage"] = storage

    if _has_value(interpret):
        data["interpret"] = interpret

    if _has_value(click_event):
        data["clickEvent"] = json.loads(click_event)

    if _has_value(hover_event):
        data["hoverEvent"] = json.loads(hover_event)

    if _has_value(color):
        data["color"] = color

    return json.dumps(data)


def _run_command(command: str):
    if not command.startswith("/"):
        command = f"/{command}"
    return json.dumps({"action": "run_command", "value": command})


def _suggest_command(command: str):
    return json.dumps({"action": "suggest_command", "value": command})


def _show_text(text: str):
    raw_json = json.loads(text)
    return json.dumps({"action": "show_text", "contents": raw_json})


help_funcs = {
    "TextC": {
        "translate": _translate,
        "nbt": _nbt,
        "clickEvent": {
            "run_command": _run_command,
            "suggest_command": _suggest_command,
        },
        "hoverEvent": {
            "show_text": _show_text,
        },
    }
}


env = Environment(
    loader=FileSystemLoader("PythonInterpreter/jinja2"),
    trim_blocks=True,
)


def replace_placeholders(code: str, data: dict) -> str:
    """
    替换代码中的占位符

    :param code: 源码
    :type code: str
    :param data: 数据
    :type data: dict
    :return: 替换后的代码
    :rtype: str
    """
    template = env.from_string(code)

    # 渲染模板
    code = template.render(data)

    return code


def get_relative_path(a: str, b: str) -> str:
    """
    计算路径A相对于路径B的相对路径

    :param a: 路径A
    :type a: str
    :param b: 路径B
    :type b: str
    :return: 相对路径
    :rtype: str
    """
    # 获取路径A和B的绝对路径
    a = os.path.abspath(a)
    b = os.path.abspath(b)

    # 获取路径A和B的公共路径
    common_path = os.path.commonpath([a, b])

    # 计算路径A相对于公共路径的相对路径
    relative_a = os.path.relpath(a, common_path)

    # 计算路径B相对于公共路径的相对路径
    relative_b = os.path.relpath(b, common_path)

    # 如果路径A比路径B长,则返回路径A的相对路径
    if len(relative_a) > len(relative_b):
        return relative_a

    # 如果路径A和路径B一样长,则返回路径A的相对路径
    elif len(relative_a) == len(relative_b):
        return relative_a

    # 如果路径B比路径A长,则返回路径B的相对路径
    else:
        return relative_b


def get_files(base_path: str, root_dir: str) -> Generator[tuple[str, str, str], None, None]:
    """
    获取指定目录下的所有文件路径的生成器

    :param base_path: 基础路径
    :type base_path: str
    :param root_dir: 根目录
    :type root_dir: str
    :return: 文件路径
    :rtype: str
    """
    for root, dirs, files in os.walk(os.path.join(base_path, root_dir)):
        for file in files:
            relative_path = get_relative_path(os.path.join(base_path, root_dir), root)
            relative_path = os.path.normpath(os.path.join(root_dir, relative_path))

            yield os.path.normpath(os.path.join(root, file)), relative_path, file


def main():
    file_extensions = [".mcfunction", ".mcmeta"]
    save_path = r"D:\game\Minecraft\.minecraft\versions\1.20.6-MCFC\saves\函数\datapacks"
    # save_path = r".\.output"
    read_path = r".\PythonInterpreter"

    placeholder_map = GlobalConfiguration().__placeholder__()
    placeholder_map.update(help_funcs)

    for file_path, relative_path, file in get_files(r"", read_path):

        print(file_path, relative_path, file)
        print("-" * 50)
        print("Reading", file_path)

        with open(file_path, encoding="UTF-8", mode='r') as f:
            code = f.read()

        if file.lower().endswith(".mcfunction.jinja2"):
            print("Renaming", file, "To", file[:-len(".jinja2")])
            file = file[:-len(".jinja2")]

        ext = os.path.splitext(file)[1]
        if ext in file_extensions:
            print("Processing", file_path)
            new_code = replace_placeholders(code, placeholder_map)
        else:
            print("No Processing", file_path)
            new_code = code

        print("Saving", file_path, "To", os.path.join(save_path, relative_path, file))

        os.makedirs(os.path.join(save_path, relative_path), exist_ok=True)
        with open(os.path.join(save_path, relative_path, file), encoding="UTF-8", mode='w') as f:
            f.write(new_code)

        print("Done.", file_path)
        print("-" * 50)
        print()
        print()


if __name__ == "__main__":
    main()

__all__ = ("main",)
