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



IMPORTED = {}
MIGRATEABLE = []
HELPABLE = {}
STATS = []
USER_INFO = []
DATA_IMPORT = []
DATA_EXPORT = []

CHAT_SETTINGS = {}
USER_SETTINGS = {}

for module_name in ALL_MODULES:
    imported_module = importlib.import_module(f"Exon.modules.{module_name}")
    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__

    if imported_module.__mod_name__.lower() not in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        raise Exception("ᴄᴀɴ'ᴛ ʜᴀᴠᴇ ᴛᴡᴏ ᴍᴏᴅᴜʟᴇs ᴡɪᴛʜ ᴛʜᴇ sᴀᴍᴇ ɴᴀᴍᴇ! ᴘʟᴇᴀsᴇ ᴄʜᴀɴɢᴇ ᴏɴᴇ")

    if hasattr(imported_module, "get_help") and imported_module.get_help:
        HELPABLE[imported_module.__mod_name__.lower()] = imported_module

    # Chats to migrate on chat_migrated events
    if hasattr(imported_module, "__migrate__"):
        MIGRATEABLE.append(imported_module)

    if hasattr(imported_module, "__stats__"):
        STATS.append(imported_module)

    if hasattr(imported_module, "__user_info__"):
        USER_INFO.append(imported_module)

    if hasattr(imported_module, "__import_data__"):
        DATA_IMPORT.append(imported_module)

    if hasattr(imported_module, "__export_data__"):
        DATA_EXPORT.append(imported_module)

    if hasattr(imported_module, "__chat_settings__"):
        CHAT_SETTINGS[imported_module.__mod_name__.lower()] = imported_module

    if hasattr(imported_module, "__user_settings__"):
        USER_SETTINGS[imported_module.__mod_name__.lower()] = imported_module


# do not async

@Exoncmd(command="text")
def test(update: Update, context: CallbackContext):
    """#TODO

    Params:
        update: Update           -
        context: CallbackContext -
    """
    # pprint(ast.literal_eval(str(update)))
    # update.effective_message.reply_text("Hola tester! _I_ *have* `markdown`", parse_mode=ParseMode.MARKDOWN)
    update.effective_message.reply_text("ᴛʜɪs ᴘᴇʀsᴏɴ ᴇᴅɪᴛᴇᴅ ᴀ ᴍᴇssᴀɢᴇ")
    print(update.effective_message)












                              
def error_callback(_, context: CallbackContext):
    """#TODO

    Params:
        update  -
        context -
    """

    try:
        raise context.error
    except (Unauthorized, BadRequest):
        pass
        # remove update.message.chat_id from conversation list
    except TimedOut:
        pass
        # handle slow connection problems
    except NetworkError:
        pass
        # handle other connection problems
    except ChatMigrated:
        pass
        # the chat_id of a group has changed, use e.new_chat_id instead
    except TelegramError:
        pass
        # handle all other telegram related errors





            



def send_settings(chat_id: int, user_id: int, user=False):
    """#TODO

    Params:
        chat_id -
        user_id -
        user    -
    """

    if user:
        if USER_SETTINGS:
            settings = "\n\n".join(
                f"*{mod.__mod_name__}*:\n{mod.__user_settings__(user_id)}"
                for mod in USER_SETTINGS.values()
            )
            dispatcher.bot.send_message(
                user_id,
                "ᴛʜᴇsᴇ ᴀʀᴇ ʏᴏᴜʀ ᴄᴜʀʀᴇɴᴛ sᴇᴛᴛɪɴɢs:" + "\n\n" + settings,
                parse_mode=ParseMode.MARKDOWN,
            )

        else:
            dispatcher.bot.send_message(
                user_id,
                "sᴇᴇᴍs ʟɪᴋᴇ ᴛʜᴇʀᴇ ᴀʀᴇɴ'ᴛ ᴀɴʏ ᴜsᴇʀ sᴘᴇᴄɪғɪᴄ sᴇᴛᴛɪɴɢs ᴀᴠᴀɪʟᴀʙʟᴇ :'(",
                parse_mode=ParseMode.MARKDOWN,
            )

    elif CHAT_SETTINGS:
        chat_name = dispatcher.bot.getChat(chat_id).title
        dispatcher.bot.send_message(
            user_id,
            text=f"ᴡʜɪᴄʜ ᴍᴏᴅᴜʟᴇ ᴡᴏᴜʟᴅ ʏᴏᴜ ʟɪᴋᴇ ᴛᴏ ᴄʜᴇᴄᴋ {chat_name}'s sᴇᴛᴛɪɴɢs ғᴏʀ?",
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
            ),
        )
    else:
        dispatcher.bot.send_message(
            user_id,
            "sᴇᴇᴍs ʟɪᴋᴇ ᴛʜᴇʀᴇ ᴀʀᴇɴ'ᴛ ᴀɴʏ ᴄʜᴀᴛ sᴇᴛᴛɪɴɢs ᴀᴠᴀɪʟᴀʙʟᴇ :'(\nsᴇɴᴅ ᴛʜɪs "
            "ɪɴ ᴀ ɢʀᴏᴜᴘ ᴄʜᴀᴛ ʏᴏᴜ'ʀᴇ ᴀᴅᴍɪɴ ɪɴ ᴛᴏ ғɪɴᴅ ɪᴛs ᴄᴜʀʀᴇɴᴛ sᴇᴛᴛɪɴɢs!",
            parse_mode=ParseMode.MARKDOWN,
        )


@Exoncallback(pattern=r"stngs_")
def settings_button(update: Update, context: CallbackContext):
    """#TODO

    Params:
        update: Update           -
        context: CallbackContext -
    """

    query = update.callback_query
    user = update.effective_user
    bot = context.bot
    mod_match = re.match(r"stngs_module\((.+?),(.+?)\)", query.data)
    prev_match = re.match(r"stngs_prev\((.+?),(.+?)\)", query.data)
    next_match = re.match(r"stngs_next\((.+?),(.+?)\)", query.data)
    back_match = re.match(r"stngs_back\((.+?)\)", query.data)
    try:
        if mod_match:
            chat_id = mod_match[1]
            module = mod_match[2]
            chat = bot.get_chat(chat_id)
            text = f"*{escape_markdown(chat.title)}* ʜᴀs ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ sᴇᴛᴛɪɴɢs ғᴏʀ ᴛʜᴇ *{CHAT_SETTINGS[module].__mod_name__}* ᴍᴏᴅᴜʟᴇ:\n\n{CHAT_SETTINGS[module].__chat_settings__(chat_id, user.id)}"
            query.message.reply_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="ʙᴀᴄᴋ",
                                callback_data=f"stngs_back({chat_id})",
                            )
                        ]
                    ]
                ),
            )

        elif prev_match:
            chat_id = prev_match[1]
            curr_page = int(prev_match[2])
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                f"ʜɪ ᴛʜᴇʀᴇ! ᴛʜᴇʀᴇ ᴀʀᴇ ǫᴜɪᴛᴇ ᴀ ғᴇᴡ sᴇᴛᴛɪɴɢs ғᴏʀ {chat.title} - ɢᴏ ᴀʜᴇᴀᴅ ᴀɴᴅ ᴘɪᴄᴋ ᴡʜᴀᴛ ʏᴏᴜ'ʀᴇ ɪɴᴛᴇʀᴇsᴛᴇᴅ ɪɴ.",
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        curr_page - 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif next_match:
            chat_id = next_match[1]
            next_page = int(next_match[2])
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                f"ʜɪ ᴛʜᴇʀᴇ! ᴛʜᴇʀᴇ ᴀʀᴇ ǫᴜɪᴛᴇ ᴀ ғᴇᴡ sᴇᴛᴛɪɴɢs ғᴏʀ {chat.title} - ɢᴏ ᴀʜᴇᴀᴅ ᴀɴᴅ ᴘɪᴄᴋ ᴡʜᴀᴛ ʏᴏᴜ'ʀᴇ ɪɴᴛᴇʀᴇsᴛᴇᴅ ɪɴ.",
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        next_page + 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif back_match:
            chat_id = back_match[1]
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                text=f"ʜɪ ᴛʜᴇʀᴇ! ᴛʜᴇʀᴇ ᴀʀᴇ ǫᴜɪᴛᴇ ᴀ ғᴇᴡ sᴇᴛᴛɪɴɢs ғᴏʀ {escape_markdown(chat.title)} - ɢᴏ ᴀʜᴇᴀᴅ ᴀɴᴅ ᴘɪᴄᴋ ᴡʜᴀᴛ ʏᴏᴜ'ʀᴇ ɪɴᴛᴇʀᴇsᴛᴇᴅ ɪɴ.",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )

        # ensure no spinny white circle
        bot.answer_callback_query(query.id)
        query.message.delete()
    except BadRequest as excp:
        if excp.message not in [
            "ᴍᴇssᴀɢᴇ ɪs ɴᴏᴛ ᴍᴏᴅɪғɪᴇᴅ",
            "Query_id_invalid",
            "ᴍᴇssᴀɢᴇ ᴄᴀɴ'ᴛ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ",
        ]:
            log.exception("ᴇxᴄᴇᴘᴛɪᴏɴ ɪɴ sᴇᴛᴛɪɴɢs ʙᴜᴛᴛᴏɴs. %s", str(query.data))


@Exoncmd(command="settings")
def get_settings(update: Update, context: CallbackContext):
    """#TODO

    Params:
        update: Update           -
        context: CallbackContext -
    """

    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    msg = update.effective_message  # type: Optional[Message]

    # ONLY send settings in PM
    if chat.type == chat.PRIVATE:
        send_settings(chat.id, user.id, True)

    elif is_user_admin(update, user.id):
        text = "ᴄʟɪᴄᴋ ʜᴇʀᴇ ᴛᴏ ɢᴇᴛ ᴛʜɪs ᴄʜᴀᴛ sᴇᴛᴛɪɴɢs, ᴀs ᴡᴇʟʟ ᴀs ʏᴏᴜʀs."
        msg.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="sᴇᴛᴛɪɴɢs",
                            url=f"t.me/{context.bot.username}?start=stngs_{chat.id}",
                        )
                    ]
                ]
            ),
        )
    else:
        text = "ᴄʟɪᴄᴋ ʜᴇʀᴇ ᴛᴏ ᴄʜᴇᴄᴋ ʏᴏᴜʀ sᴇᴛᴛɪɴɢs."


@Exonmsg(Filters.status_update.migrate)
def migrate_chats(update: Update, context: CallbackContext):
    """#TODO

    Params:
        update: Update           -
        context: CallbackContext -
    """

    msg = update.effective_message  # type: Optional[Message]
    if msg.migrate_to_chat_id:
        old_chat = update.effective_chat.id
        new_chat = msg.migrate_to_chat_id
    elif msg.migrate_from_chat_id:
        old_chat = msg.migrate_from_chat_id
        new_chat = update.effective_chat.id
    else:
        return

    log.info("ᴍɪɢʀᴀᴛɪɴɢ ғʀᴏᴍ %s, ᴛᴏ %s", str(old_chat), str(new_chat))
    for mod in MIGRATEABLE:
        mod.__migrate__(old_chat, new_chat)

    log.info("sᴜᴄᴄᴇssғᴜʟʟʏ ᴍɪɢʀᴀᴛᴇᴅ!")
    raise DispatcherHandlerStop


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
