import logging
from dataclasses import dataclass
from environs import Env


logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] #%(levelname)-6s %(filename)-15s: %(lineno)-3s - %(message)s'
)

logger = logging.getLogger(__name__)


@dataclass
class Config:
    DB_PATH_M: str


def load_configs() -> Config:
    env = Env()
    env.read_env()

    return Config(
        DB_PATH_M=env('DB_PATH_M')
    )
