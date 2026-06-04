"""
执行器的基础标准。

为了灵活性，暂时作为模板定义，根据具体工具具体设计。
"""

from __future__ import annotations
from abc import ABC, abstractmethod
import asyncio

import subprocess

from typing import TYPE_CHECKING
# if TYPE_CHECKING:


class CommandResult:
    stdout: str
    stderr: str
    returncode: int
    success: bool
    data: dict


class CommandWrapper(ABC):
    @abstractmethod
    def run(self, *args, **kwargs):
        """统一运行。"""

    @abstractmethod
    async def async_run(self, *args, **kwargs):
        """异步版本。"""

    @abstractmethod
    def dry_run(self, *args, **kwargs):
        """试运行，打印输入命令。"""

    @abstractmethod
    def validate(self):
        """验证命令是否可用。"""

