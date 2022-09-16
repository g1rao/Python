# Progress Bar 
import functools
from time import sleep
from tqdm import tqdm
from concurrent import futures


class ProgressBar:
    """ Generates progress bar """
    @staticmethod
    def progress_bar(scale=100):
        def _decorator_func(func):
            def create_progress_bar(pool_job, duration, scale=100):
                """ Create progress bar """
                interval = duration / scale
                with tqdm(total=scale) as pbar:
                    for i in range(scale - 1):
                        if pool_job.done():
                            pbar.update(scale - i)
                            return
                        else:
                            sleep(interval)
                            pbar.update()
                    pool_job.result()
                    pbar.update()
            @functools.wraps(func)
            def _func(*args, **kwargs):
                with futures.ThreadPoolExecutor(max_workers=1) as _pool:
                    pool_job = _pool.submit(func, *args, **kwargs)
                    create_progress_bar(pool_job, args[0].replicas, scale)
                return pool_job.result()

            return _func
        return _decorator_func