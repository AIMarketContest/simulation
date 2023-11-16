from typing import Final


class ErrorCodes:
    DIRECTORY_DOES_NOT_EXIST: Final[int] = 2
    FILE_DOES_NOT_EXIST: Final[int] = 2
    NO_TRAINING_CONFIGS: Final[int] = 1
    NO_AGENTS_ATTRIBUTE: Final[int] = 1
    NO_TRAINED_AGENTS_ATTRIBUTE: Final[int] = 1
    MISSING_INITIAL_HASH: Final[int] = 1
    TIME_ATTRIBUTE_CONTAINS_NON_NUMBER_CHARACTERS: Final[int] = 1
    INVALID_DATE_TIME: Final[int] = 1
    MISSING_TRAINED_AGENT_DATA: Final[int] = 1
    MISSING_TRAINED_AGENT_HASH: Final[int] = 1
