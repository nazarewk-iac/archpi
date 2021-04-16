import contextlib
import logging
import os
import shutil
from pathlib import Path

from . import cmd

logger = logging.getLogger(__name__)


@contextlib.contextmanager
def in_chroot(path: Path):
    """
    see https://wiki.archlinux.org/index.php/chroot#Using_chroot
    """
    # TODO: arch-chroot replica
    # store reference to the opened DIRECTORY which can be rolled back to
    root_fd = os.open('/', os.O_RDONLY)
    cwd_fd = os.open(Path.cwd(), os.O_RDONLY)

    mounts = []

    def mnt(p: str):
        mounts.append(p)
        return p

    try:
        cmd.run('mount', '-t', 'proc', '/proc', mnt(f'{path}/proc/'))
        cmd.run('mount', '-t', 'sysfs', '/sys', mnt(f'{path}/sys/'))
        cmd.run('mount', '--rbind', '/dev', mnt(f'{path}/dev/'))
        cmd.run('mount', '--rbind', '/run', mnt(f'{path}/run/'))
        mounted_resolve = path / 'etc/resolv.conf'
        mounted_resolve_bkp = None
        if mounted_resolve.exists() or mounted_resolve.is_symlink():
            mounted_resolve_bkp = Path(f'{mounted_resolve}.bkp')
            if mounted_resolve.is_symlink():
                mounted_resolve.rename(mounted_resolve_bkp)
            else:
                shutil.move(mounted_resolve, mounted_resolve_bkp)
        shutil.copy('/etc/resolv.conf', mounted_resolve)

        logger.info(f'chroot {path}')
        os.chroot(path)
        try:
            logger.debug('chdir /')
            os.chdir('/')
            yield Path('/')
        finally:
            logger.debug('fchdir back')
            os.chdir(root_fd)
            logger.info('chroot back')
            os.chroot('.')
            logger.debug('cwd back')
            os.chdir(cwd_fd)

            if mounted_resolve_bkp:
                mounted_resolve.unlink(missing_ok=True)
                mounted_resolve_bkp.rename(mounted_resolve)
            for p in mounts:
                cmd.run('umount', p, check=False)
    finally:
        os.close(cwd_fd)
        os.close(root_fd)
