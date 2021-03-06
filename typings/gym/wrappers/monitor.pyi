"""
This type stub file was generated by pyright.
"""

from gym import Wrapper

FILE_PREFIX = ...
MANIFEST_PREFIX = ...

class Monitor(Wrapper):
    def __init__(
        self,
        env,
        directory,
        video_callable=...,
        force=...,
        resume=...,
        write_upon_reset=...,
        uid=...,
        mode=...,
    ) -> None: ...
    def step(self, action): ...
    def reset(self, **kwargs): ...
    def set_monitor_mode(self, mode): ...
    def close(self):  # -> None:
        """Flush all monitor data to disk and close any open rending windows."""
        ...
    def reset_video_recorder(self): ...
    def __del__(self): ...
    def get_total_steps(self): ...
    def get_episode_rewards(self): ...
    def get_episode_lengths(self): ...

def detect_training_manifests(training_dir, files=...): ...
def detect_monitor_files(training_dir): ...
def clear_monitor_files(training_dir): ...
def capped_cubic_video_schedule(episode_id): ...
def disable_videos(episode_id): ...

monitor_closer = ...

def load_env_info_from_manifests(manifests, training_dir): ...
def load_results(training_dir): ...
def merge_stats_files(stats_files): ...
def collapse_env_infos(env_infos, training_dir): ...
