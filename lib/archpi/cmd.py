import logging
import subprocess
import sys
from pathlib import Path

logger = logging.getLogger(__name__)


def run_as(*args, user: str, login=False, **kwargs):
    sudo_args = kwargs.pop('sudo_args', [])
    if login:
        sudo_args.append('--login')
    else:
        sudo_args.append('--preserve-env')
    return run('sudo', '-Hu', user, *sudo_args, '--', *args, **kwargs)


def run(*args, capture_stdout=False, capture_stderr=False, stdout_to_sys_stderr=False, **kwargs):
    kwargs.setdefault('encoding', 'utf8')
    kwargs.setdefault('check', True)
    kwargs['cwd'] = kwargs.pop('path', kwargs.pop('cwd', Path.cwd()))
    assert not (capture_stdout and stdout_to_sys_stderr)
    if capture_stdout:
        assert 'stdout' not in kwargs
        kwargs['stdout'] = subprocess.PIPE
    if stdout_to_sys_stderr:
        assert 'stdout' not in kwargs
        kwargs['stdout'] = sys.stderr
    if capture_stderr:
        assert 'stderr' not in kwargs
        kwargs['stderr'] = subprocess.PIPE
    # don't show some arguments in kwargs
    env = kwargs.pop('env', None)
    input = kwargs.pop('input', None)

    args = list(map(str, args))
    logger.debug(f'executing {args} with {kwargs=}')
    return subprocess.run(args, env=env, input=input, **kwargs)


def bash(script: str, **kwargs):
    return run('bash', '-eEuo', 'pipefail', '-c', script, **kwargs)
