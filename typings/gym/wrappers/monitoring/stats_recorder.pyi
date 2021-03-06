"""
This type stub file was generated by pyright.
"""

class StatsRecorder:
    def __init__(self, directory, file_prefix, autoreset=..., env_id=...) -> None: ...
    @property
    def type(self): ...
    @type.setter
    def type(self, type): ...
    def before_step(self, action): ...
    def after_step(self, observation, reward, done, info): ...
    def before_reset(self): ...
    def after_reset(self, observation): ...
    def save_complete(self): ...
    def close(self): ...
    def flush(self): ...
