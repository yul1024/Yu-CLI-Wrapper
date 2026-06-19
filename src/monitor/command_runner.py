"""
Sources:
    https://github.com/yuliu625/Yu-CLI-Wrapper/blob/main/src/monitor/run_background.py

References:
    https://github.com/yuliu625/Yu-CLI-Wrapper/blob/main/src/monitor/command_runner.py

Synopsis:
    python 原生启动程序方法。

Notes:
    这个方法并不是该仓库的目标构造。
    只是基于 nohup 实现的 wrapper 不够优秀，我基于 python 原生的 subprocess 构造了一个实现。
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from typing import TYPE_CHECKING, Sequence
# if TYPE_CHECKING:


class CommandRunner:
    """
    python 原生运行命令方法。
    """
    @staticmethod
    def run_background(
        command_args: Sequence[str],
        log_file_path: str,
        is_log_append: bool,
        is_dry_run: bool,
    ) -> str | subprocess.Popen[str]:
        """
        使用 subprocess.Popen 在后台启动命令。

        Args:
            command_args (Sequence[str]): 原始的子命令。
            log_file_path (str): 日志路径。
            is_log_append (bool): 日志打开模式:
                - True: 追加模式。
                - False: 覆盖模式。
            is_dry_run (bool): 是否 dry run 以预览命令。

        Returns:
            Union[str | subprocess.Popen[bytes]]:
                - str: dry run下的 shell command 字符串。
                - subprocess.Popen[bytes]: subprocess.Popen 控制对象。
        """
        if is_dry_run:
            command_str = ' '.join(command_args)
            print(command_str)
            return command_str
        # 路径处理
        log_file_path = Path(log_file_path)
        # before
        CommandRunner.make_log_file_path(log_file_path=log_file_path)
        # 选择追加模式或覆盖模式。
        log_mode = 'a' if is_log_append else 'w'
        with log_file_path.open(log_mode) as log_file_handle:
            process = subprocess.Popen(
                command_args,
                stdout=log_file_handle,
                stderr=subprocess.STDOUT,  # 合并错误流，不然烦死了。
                text=True,
                # 具体需求再添加参数。
            )
            return process

    # ==== 工具方法。 ====
    @staticmethod
    def make_log_file_path(
        log_file_path: str | Path,
    ) -> None:
        # 路径处理。
        log_file_path = Path(log_file_path)
        log_file_path.parent.mkdir(parents=True, exist_ok=True)


if __name__ == '__main__':
    # 后台启动命令。
    ## dry run test
    CommandRunner.run_background(
        command_args=['python', "./program_path", '--config', 'args', ],
        log_file_path="/path/to/log_file.log",
        is_log_append=True,
        is_dry_run=True,
    )
    ## run
    CommandRunner.run_background(
        command_args=['python', "./program_path", '--config', 'args', ],
        log_file_path='./log_file_path',
        is_log_append=True,
        is_dry_run=False,
    )

