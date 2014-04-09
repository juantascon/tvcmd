import logging
def log(): return logging.getLogger(__name__)

def msg(*args, **kwargs):
    return print(*args, **kwargs)

def ask_yn(question):
    answer = ""
    while True:
        answer = input(question + " [y/n]: ").lower()
        if answer in ["y", "yes"]: return True
        elif answer in ["n", "no"]: return False
