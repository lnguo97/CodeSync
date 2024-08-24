import time
from typing import Iterable

import streamlit as st


def add_progress_bar(prog_txt):
    def inner(func):
        def wrapper(iter_obj: Iterable):
            result_list = []
            progress_bar = st.progress(0, prog_txt)
            for i, result in enumerate(func(iter_obj)):
                progress = (i + 1) / len(iter_obj)
                progress_bar.progress(
                    value=progress,
                    text=f'{prog_txt}: {progress * 100:.2f}%'
                )
                result_list.append(result)
            return result_list
        return wrapper
    return inner


@add_progress_bar('Running Query')
def process_data(iter_obj: Iterable):
    for item in iter_obj:
        time.sleep(1)
        yield item * 3


data = range(20)
results = process_data(data)
st.write(results)
