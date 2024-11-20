import importlib
import re
import time
from sys import argv, version_info

from Abg.helpers.human_read import get_readable_time
from pyrogram import __version__ as pver
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram import __version__ as lver
from telegram.error import (
    BadRequest,
    ChatMigrated,
    NetworkError,
    TelegramError,
    TimedOut,
    Unauthorized,
)
from telegram.ext import CallbackContext, Filters
from telegram.ext.dispatcher import DispatcherHandlerStop
from telegram.utils.helpers import escape_markdown
from telethon import __version__ as tver

import Exon.modules.no_sql.users_db as sql
from Exon import Abishnoi as pbot
from Exon import BOT_USERNAME
from Exon import LOGGER as log
from Exon import OWNER_ID, OWNER_USERNAME, SUPPORT_CHAT, TOKEN
from Exon import StartTime, dispatcher, telethn, updater
# needed to dynamically load modules
# NOTE: Module order is not guaranteed, specify that in the config file!
from Exon.modules import ALL_MODULES
from Exon.modules.helper_funcs.chat_status import is_user_admin
from Exon.modules.helper_funcs.decorators import Exoncallback, Exoncmd, Exonmsg
from Exon.modules.helper_funcs.misc import paginate_modules
from Exon.modules.language import gs







def main():
    if SUPPORT_CHAT is not None and isinstance(SUPPORT_CHAT, str):
        try:
            dispatcher.bot.sendAnimation(
                f"@{SUPPORT_CHAT}",
                animation="https://te.legra.ph/file/8dea393ddf4fc2e339179.gif",
                caption=f"""
ㅤ🥀 {dispatcher.bot.first_name} ɪs ᴀʟɪᴠᴇ ʙᴀʙʏ ✨ .....

━━━━━━━━━━━━━
⍟ ᴍʏ [ᴏᴡɴᴇʀ](https://t.me/{OWNER_USERNAME})
⍟ **ʟɪʙʀᴀʀʏ ᴠᴇʀsɪᴏɴ :** `{lver}`
⍟ **ᴛᴇʟᴇᴛʜᴏɴ ᴠᴇʀsɪᴏɴ :** `{tver}`
⍟ **ᴘʏʀᴏɢʀᴀᴍ ᴠᴇʀsɪᴏɴ :** `{pver}`
⍟ **ᴘʏᴛʜᴏɴ ᴠᴇʀsɪᴏɴ :** `{version_info[0]}.{version_info[1]}.{version_info[2]}`
⍟ **ʙᴏᴛ ᴠᴇʀsɪᴏɴ :** `2.69``
━━━━━━━━━━━━━
""",
                parse_mode=ParseMode.MARKDOWN,
            )
        except Unauthorized:
            log.warning("ʙᴏᴛ ɪsɴᴛ ᴀʙʟᴇ ᴛᴏ sᴇɴᴅ ᴍᴇssᴀɢᴇ ᴛᴏ sᴜᴘᴘᴏʀᴛ_ᴄʜᴀᴛ, ɢᴏ ᴀɴᴅ ᴄʜᴇᴄᴋ !")
        except BadRequest as e:
            log.warning(e.message)

    log.info(
        f"ᴜsɪɴɢ ʟᴏɴɢ ᴘᴏʟʟɪɴɢ. ........... ᴇɴᴊᴏʏ ʏᴏᴜʀ ʙᴏᴛ sᴛᴀʀᴛᴇᴅ ᴀs →  {dispatcher.bot.first_name} "
    )
    updater.start_polling(timeout=15, read_latency=4, drop_pending_updates=True)

    if len(argv) in {1, 3, 4}:
        telethn.run_until_disconnected()

    else:
        telethn.disconnect()
    updater.idle()


if __name__ == "__main__":
    log.info(f"[ᴇxᴏɴ] →  sᴜᴄᴄᴇssғᴜʟʟʏ ʟᴏᴀᴅᴇᴅ ᴍᴏᴅᴜʟᴇs: {str(ALL_MODULES)}")
    telethn.start(bot_token=TOKEN)
    pbot.start()
    main()
