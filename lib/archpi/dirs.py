import contextlib
import os
import tempfile
from pathlib import Path


@contextlib.contextmanager
def in_tmpdir(*args, **kwargs):
    with tempfile.TemporaryDirectory(*args, **kwargs) as tmp:
        path = Path(tmp)
        old_dir = Path.cwd()
        os.chdir(path)
        try:
            yield path
        finally:
            os.chdir(old_dir)
