def text_progress_bar(capacity: int, used: int):
    bar_length = 20
    filled_length = int(bar_length * used // capacity)
    bar = '█' * filled_length + '░' * (bar_length - filled_length)
    return bar
