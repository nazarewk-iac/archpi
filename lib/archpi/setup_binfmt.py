# base on https://github.com/Robertof/nixos-docker-sd-image-builder/blob/master/docker/setup-qemu/scripts/update-binfmt.sh
import contextlib
import logging
import os
import subprocess
import sys
from pathlib import Path

from archpi import cmd

AARCH64_MAGIC = '\x7fELF\x02\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\xb7\x00'
AARCH64_MASK = '\xff\xff\xff\xff\xff\xff\xff\x00\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xff\xff\xff'
logger = logging.getLogger(__name__)


@contextlib.contextmanager
def registered_binfmt(binary=Path('/usr/bin/qemu-aarch64-static')):
    uname = os.uname()
    if uname.machine.startswith('arm') or uname.machine == 'aarch64':
        logger.info('Already on the ARM box, skipping binfmt setup.')
        return
    misc = Path('/proc/sys/fs/binfmt_misc')
    if not misc.is_dir():
        cmd.run('modprobe', 'binfmt_misc')
    register = misc / 'register'
    if not register.is_file():
        cmd.run('mount', '-t', 'binfmt_misc', 'binfmt_misc', misc)

    if not os.access(register, os.W_OK):
        logger.error(f'{register} is not writable, must run in --privileged container!')
        sys.exit(1)

    interpreter = misc / f'nazarewk-iac-archpi-{binary.name}'
    # unregister interpreter
    if interpreter.exists():
        interpreter.write_text('-1')

    register.write_text(f':{interpreter}:M::{AARCH64_MAGIC}:{AARCH64_MASK}:{binary}:F')
    try:
        yield
    finally:
        interpreter.write_text('-1')
