import contextlib
import subprocess
from pathlib import Path


@contextlib.contextmanager
def losetup_img(img: Path) -> Path:
    lo = Path(subprocess.check_output(['losetup', '-f'], encoding='utf8').strip())
    subprocess.check_call(['losetup', '-P', lo, img])
    try:
        yield lo
    finally:
        subprocess.check_call(['losetup', '-d', lo])


@contextlib.contextmanager
def mount_disks(lo: Path, *mount_points):
    mnt = Path('/mnt')
    paths = sorted(enumerate(mount_points, start=1), key=lambda e: e[1])
    for partnum, path in paths:
        at = mnt / path.lstrip('/')
        at.mkdir(parents=True, exist_ok=True)
        subprocess.check_call(['mount', f'{lo}p{partnum}', mnt])
    try:
        yield mnt
    finally:
        subprocess.check_call(['df', '-h'])
        subprocess.check_call(['umount', '-R', mnt])
