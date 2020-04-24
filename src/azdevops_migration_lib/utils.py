# from typing import List, Dict


def toCamelCase(snakeStr: str) -> str:
    components = snakeStr.split('_')
    return components[0] + ''.join(c.title() for c in components[1:])
