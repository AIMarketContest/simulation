"""
This type stub file was generated by pyright.
"""

from gym import ActionWrapper

class ClipAction(ActionWrapper):
    r"""Clip the continuous action within the valid bound."""
    def __init__(self, env) -> None:
        ...
    
    def action(self, action): # -> Any:
        ...
    


