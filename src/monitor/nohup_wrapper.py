"""
Sources:
    https://github.com/yuliu625/Yu-CLI-Wrapper/blob/main/src/monitor/nohup_wrapper.py

References:
    - https://www.gnu.org/software/coreutils/manual/html_node/nohup-invocation.html
    - https://man7.org/linux/man-pages/man1/nohup.1.html

Synopsis:
    nohup 命令的参数转义和运行封装。

Notes:
    nohup 使用频率较高，但是其参数和符号可读性很差。我转义和封装了所有 nohup 的所有可选配置参数。

    更优选择:
        - subprocess.Popen: nohup 的本质本身就已经是一个 wrapper :
            nohup 进行:
                - 信号处理: 拦截 SIGHUP (Signal Hang Up) 。
                - 重定向: 输出脱离终端，指向目标文件。
            这使得:
                - 这 2 个系统调用不如 python 原生系统调用更加干净可控。
                - wrapper 上的 wrapper 很奇怪。
        - screen / tmux: 仅 shell 条件下，linux 其他命令。更易进行检查和控制。

    停止维护说明:
        在可以运行 python 的机器上，该方法完全被纯 python 系统控制取代。当前方法仅进行存档，不再维护。
"""

from __future__ import annotations
from loguru import logger

import subprocess

from typing import TYPE_CHECKING, Sequence
# if TYPE_CHECKING:


class NoHupWrapper:
    """
    nohup 参数转义，运行封装工具。

    对照拆解:
        - > | >> : shell重定向指令。这是 shell 的功能。
        - 2>&1 : 文件描述符绑定。
        - & : 任务控制符。
    """
    @staticmethod
    def run(
        command_args: Sequence[str],
        log_file_path: str,
        is_log_append: bool,
        is_dry_run: bool,
    ) -> str | subprocess.Popen[bytes]:
        """
        使用 nohup 运行原始的 shell 命令。

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
        # 由于 nohup 的特殊符号，命令启动需要以 str 进行。
        command_str = "nohup " + " ".join(command_args)
        # 选择追加模式或覆盖模式。
        redirect_operator = '>>' if is_log_append else '>'
        # 命令拼接。
        command_str = f"{command_str} {redirect_operator}{log_file_path} 2>&1 &"
        if is_dry_run:
            print(f"Shell Command: \n{command_str}")
            return command_str
        else:
            # 非阻塞运行。
            return subprocess.Popen(
                command_str,
                shell=True,
            )


if __name__ == '__main__':
    # 运行示例。
    ## dry run test
    NoHupWrapper.run(
        command_args=['python', "./program_path", '--config', 'args', ],
        log_file_path="/path/to/log_file.log",
        is_log_append=True,
        is_dry_run=True,
    )
    ## run with nohup
    NoHupWrapper.run(
        command_args=['python', "./program_path", '--config', 'args', ],
        log_file_path="/path/to/log_file.log",
        is_log_append=True,
        is_dry_run=False,
    )

