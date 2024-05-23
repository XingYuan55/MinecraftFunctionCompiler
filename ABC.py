# -*- coding: utf-8 -*-
# cython: language_level = 3
"""
定义了一些抽象类
"""

from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import OrderedDict

from Configuration import CompileConfiguration
from Configuration import GlobalConfiguration
from NamespaceTools import Namespace
from NamespaceTools import FileNamespace
from ParameterTypes import ABCParameter


class ABCEnvironment(ABC):
    """
    Environment的抽象类，用于定义环境的基本行为和属性。
    """
    def __init__(self, c_conf: CompileConfiguration, g_conf: GlobalConfiguration = None) -> None:
        """
        初始化

        :param c_conf: 编译器配置
        :type c_conf: CompileConfiguration
        :param g_conf: 全局配置
        :type g_conf: GlobalConfiguration
        :return: None
        :rtype: None
        """
        if g_conf is None:
            g_conf = GlobalConfiguration()
        self.c_conf: CompileConfiguration = c_conf
        self.g_conf: GlobalConfiguration = g_conf
        self.namespace = Namespace(self.c_conf.base_namespace)
        self.file_namespace = FileNamespace()

        self.func_args: dict[str, OrderedDict[str, ABCParameter]] = {}

    @abstractmethod
    def generate_code(self, node: Any, namespace: str, file_namespace: str) -> str:
        """
        为给定的节点生成MCF

        :param node: 节点
        :type node: Any
        :param namespace: 命名空间
        :type namespace: str
        :param file_namespace: 文件命名空间
        :return: 生成的MCF
        :rtype: str
        """

    @abstractmethod
    def ns_split_base(self, namespace: str) -> tuple[str, str]:
        """
        分割命名空间的基础命名空间

        :param namespace: 命名空间
        :type namespace: str
        :return: 基础命名空间和其余部分
        :rtype: tuple[str, str]
        """

    @abstractmethod
    def ns_join_base(self, name: str) -> str:
        """
        连接基础命名空间和名称

        :param name: 名称
        :type name: str
        :return: 连接后的命名空间
        :rtype: str
        """

    @abstractmethod
    def ns_from_node(
            self,
            node: Any,
            namespace: str,
            *,
            not_exists_ok: bool = False,
            ns_type: str | None = None
    ) -> tuple[str, str, str]:
        """
        从节点中获取命名空间

        :param node: 节点
        :type node: ast.Name | ast.Attribute
        :param namespace: 当前命名空间
        :type namespace: str
        :param not_exists_ok: 名称不存在时在当前命名空间下生成
        :type not_exists_ok: bool
        :param ns_type: 不存在时生成填入的命名空间类型
        :type ns_type: str | None
        :return: (name, full_namespace, root_namespace)
        :rtype: tuple[str, str, str]
        """

    @abstractmethod
    def ns_init(self, namespace: str, ns_type: str) -> None:
        """
        初始化根命名空间

        :param namespace: 命名空间
        :type namespace: str
        :param ns_type: 命名空间类型
        :type ns_type: str
        :return: None
        :rtype: None
        """

    @abstractmethod
    def ns_setter(self, name: str, targe_namespace: str, namespace: str, ns_type: str) -> None:
        """
        在指定的命名空间下创建一个名称指向目标命名空间

        :param name: 名称
        :type name: str
        :param targe_namespace: 指向的命名空间
        :type targe_namespace: str
        :param namespace: 设置的命名空间
        :type namespace: str
        :param ns_type: 命名空间类型
        :type ns_type: str
        :return: None
        :rtype: None
        """

    @abstractmethod
    def ns_getter(self, name, namespace: str, ret_raw: bool = False) -> tuple[str | dict, str]:
        """
        在指定的命名空间下寻找名称，并返回所找到的值

        :param name: 寻找的名称
        :type name: str
        :param namespace: 寻找的命名空间
        :type namespace: str
        :param ret_raw: 是否直接返回源字典
        :type ret_raw: bool
        :returns: (完整命名空间 | 命名空间字典, 基础命名空间)
        :rtype: tuple[str | dict, str]
        """

    @abstractmethod
    def ns_store_local(self, namespace: str) -> tuple[str, str]:
        """
        将当前命名空间下的所有变量和临时变量存储到data storage

        :param namespace: 目标命名空间
        :type namespace: str
        :returns: (保存用命令, 加载用命令)
        :rtype: tuple[str, str]
        """

    @abstractmethod
    def temp_ns_init(self, namespace: str) -> None:
        """
        初始化编译时临时命名空间存储

        :param namespace: 需要初始化的命名空间
        :type namespace: str
        :return: None
        :rtype: None
        """

    @abstractmethod
    def temp_ns_append(self, namespace: str, name: str) -> None:
        """
        添加MCF运行时临时命名空间

        :param namespace: 存储目标命名空间
        :type namespace: str
        :param name: MCF运行时临时命名空间
        :type name: str
        :return: None
        :rtype: None
        """

    @abstractmethod
    def temp_ns_remove(self, namespace: str, name: str) -> None:
        """
        移除MCF运行时临时命名空间

        :param namespace: 存储目标命名空间
        :type namespace: str
        :param name: MCF运行时临时命名空间
        :type name: str
        :return: None
        :rtype: None
        """

    @abstractmethod
    def file_ns_init(self, file_namespace: str, level: str | None, file_ns_type: str, ns: str) -> None:
        """
        初始化根文件命名空间

        :param file_namespace: 文件命名空间
        :type file_namespace: str
        :param level: 文件层级名
        :type level: str | None
        :param file_ns_type: 文件命名空间类型
        :type file_ns_type: str
        :param ns: 文件命名空间所对应的普通命名空间
        :type ns: str
        :return: None
        :rtype: None
        """

    @abstractmethod
    def file_ns_setter(
            self,
            name: str,
            targe_file_namespace: str,
            file_namespace: str,
            level: str | None,
            file_ns_type: str, ns: str
    ) -> None:
        """
        在指定的文件命名空间下创建一个名称指向目标文件命名空间

        :param name: 名称
        :type name: str
        :param targe_file_namespace: 指向的文件命名空间
        :type targe_file_namespace: str
        :param file_namespace: 设置的文件命名空间
        :type file_namespace: str
        :param level: 文件层级名
        :type level: str | None
        :param file_ns_type: 文件命名空间类型
        :type file_ns_type: str
        :param ns: 文件命名空间所对应的普通命名空间
        :type ns: str
        :return: None
        :rtype: None
        """

    @abstractmethod
    def file_ns_getter(self, name, file_namespace: str, ret_raw: bool = False) -> tuple[str | dict, str]:
        """
        在指定的文件命名空间下寻找名称，并返回所找到的值

        :param name: 寻找的名称
        :type name: str
        :param file_namespace: 寻找的文件命名空间
        :type file_namespace: str
        :param ret_raw: 是否返回源字典
        :type ret_raw: bool
        :returns: (完整文件命名空间 | 文件命名空间字典, 基础文件命名空间)
        :rtype: tuple[str | dict, str]
        """

    @abstractmethod
    def file_ns2path(self, path: str, *args: str) -> str:
        """
        将文件命名空间转换为路径

        :param path: 文件命名空间
        :type path: str
        :param args: 需要拼接的路径
        :type args: str
        :return: 拼接后的路径
        :rtype: str
        """

    @abstractmethod
    def mkdirs_file_ns(self, file_namespace: str, *args) -> None:
        """
        为文件命名空间创建目录

        :param file_namespace: 文件命名空间
        :type file_namespace: str
        :param args: 文件命名空间
        :type args: str
        :return: None
        :rtype: None
        """

    @abstractmethod
    def writeable_file_namespace(self, file_namespace: str, namespace: str):
        """
        将文件命名空间转换为支持上下文管理器的可写对象

        :param file_namespace: 目标文件命名空间
        :type file_namespace: str
        :param namespace: 文件命名空间对应的命名空间
        :type namespace: str
        :return: 可写对象
        :rtype: Any
        """
