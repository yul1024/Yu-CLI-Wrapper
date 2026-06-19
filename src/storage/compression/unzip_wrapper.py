"""

"""

from __future__ import annotations
from loguru import logger

import subprocess

from typing import TYPE_CHECKING
# if TYPE_CHECKING:


class UnzipWrapper:
    @staticmethod
    def unzip_file(
        file_path: str,
        target_dir: str | None = None,
    ) -> None:
        ...

    @staticmethod
    def check_files(
        file_path: str,
    ) -> None:
        ...

