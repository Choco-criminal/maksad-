


from os import getenv

from dotenv import load_dotenv

load_dotenv()


class Config(object):
    LOGGER = True

    API_ID = int(getenv("API_ID", "25475489"))
    API_HASH = getenv("API_HASH", "3fc2b371f4fbb0166758736414d8be92")
    ARQ_API_KEY = "PMPTTD-HOMLMF-SRBHNH-RZMWXL-ARQ"
    SPAMWATCH_API = None
    TOKEN = getenv("TOKEN", "7617090520:AAH6OqlzkAGlJUhtd6O3yd9sRfDo6lxwn00")
    OWNER_ID = int(getenv("OWNER_ID", 1266240012))
    OWNER_USERNAME = getenv("OWNER_USERNAME", "UnknownX_9_11")
    SUPPORT_CHAT = getenv("SUPPORT_CHAT", "ANIME_CHAT_ANG")
    UPDATE_CHAT = getenv("UPDATE_CHAT", "Choco_for_u")
    EVENT_LOG = int(getenv("EVENT_LOG", "-1002122538649"))
    LOGGER_ID = int(getenv("LOGGER_ID", "-1002122538649"))
    MONGO_URI = getenv(
        "MONGO_DB_URI",
        "mongodb+srv://1:1@cluster0.ull4r.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    )
    DB_NAME = getenv("DB_NAME", "ExonRobot")
    REDIS_URL = "redis://default:wK6ZCiclq4iQKYpgfY90v6kd6WdPfEwl@redis-10186.c263.us-east-1-2.ec2.cloud.redislabs.com:10186/default"
    DATABASE_URL = getenv("DATABASE_URL", "postgres://avnadmin:AVNS_56xhfKFkBo-iiPYoj_F@choco-chocoxgithub-f883.b.aivencloud.com:16510/defaultdb?sslmode=require")

    # ɴᴏ ᴇᴅɪᴛ ᴢᴏɴᴇ
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://")


class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
                               
