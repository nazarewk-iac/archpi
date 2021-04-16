import contextlib
import logging
from pathlib import Path

from archpi import cmd

logger = logging.getLogger(__name__)


@contextlib.contextmanager
def losetup_img(img: Path) -> Path:
    proc = cmd.run('losetup', '-f', capture_stdout=True)
    lo = Path(proc.stdout.strip())
    cmd.run('losetup', '-P', lo, img)
    try:
        yield lo
    finally:
        cmd.run('losetup', '-d', lo)


@contextlib.contextmanager
def mount_disks(lo: Path, *mount_points):
    mnt = Path('/mnt')
    paths = sorted(enumerate(mount_points, start=1), key=lambda e: e[1])
    for partnum, path in paths:
        at = mnt / path.lstrip('/')
        logger.info(f'Mounting {path} at {at}')
        at.mkdir(parents=True, exist_ok=True)
        cmd.run('mount', f'{lo}p{partnum}', at)
    try:
        yield mnt
    finally:
        cmd.run('df', '-h')
        cmd.run('umount', '--recursive', mnt)
