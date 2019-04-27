#!/usr/bin/env python3

__package__ = 'archivebox.cli'
__command__ = 'archivebox manage'
__description__ = 'Run an ArchiveBox Django management command'

import sys

from typing import Optional, List, IO

from ..main import manage
from ..config import OUTPUT_DIR


def main(args: Optional[List[str]]=None, stdin: Optional[IO]=None, pwd: Optional[str]=None) -> None:
    manage(
        args=args,
        out_dir=pwd or OUTPUT_DIR,
    )


if __name__ == '__main__':
    main(args=sys.argv[1:], stdin=sys.stdin)
