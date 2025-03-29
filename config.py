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
    API_ID_M: str
    API_HASH_M: str
    MOB_NUMBER: str
    BOT_TOKEN: str
    ALLOWED_USERS: str


env = Env()
env.read_env(override=True)

settings = Config(
    DB_PATH_M=env('DB_PATH_M'),
    API_ID_M=env('API_ID_M'),
    API_HASH_M=env('API_HASH_M'),
    MOB_NUMBER=env('MOB_NUMBER'),
    BOT_TOKEN=env('BOT_TOKEN'),
    ALLOWED_USERS=[int(uid.strip()) for uid in env('ADMIN_IDS').split(",")]

)
