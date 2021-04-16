import functools
import io

from tqdm import tqdm
from urllib3 import HTTPResponse


def file_progress(self: io.BufferedReader, desc='', total: int = 0):
    def read(size, **kwargs):
        progress.update(size)
        return original_read(size, **kwargs)

    self.seek(0)
    progress = tqdm(total=total, desc=desc,
                    unit='B', unit_scale=True, unit_divisor=1024)
    original_read = self.read
    self.read = read
    return self


def stream_response(self: HTTPResponse, desc=''):
    # see https://stackoverflow.com/a/3668977
    def read(size, **kwargs):
        progress.update(size)
        return original_read(size, **kwargs)

    progress = tqdm(total=self.length_remaining, desc=desc,
                    unit='B', unit_scale=True, unit_divisor=1024)
    original_read = self.read
    self.read = functools.partial(read)
    return self
