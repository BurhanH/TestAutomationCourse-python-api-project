"""Yellow text on red background"""


def yellow_on_red_back(text):
    return f'\033[33m\033[41m\033[6m\033[1m >>> {text} <<< \033[0m'
