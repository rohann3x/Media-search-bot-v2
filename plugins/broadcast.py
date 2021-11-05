# © @BLACK_DEVIL_TG
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from bot.plugins.PSYCH0_TG.user_db import get_users
from bot.plugins.PSYCH0_TG.user_db import del_from_users
from pyrogram.errors import (FloodWait, PeerIdInvalid, UserIsBlocked, InputUserDeactivated)
    
ADMINS = [1780788805, 2022658797]

@Client.on_message(filters.private & filters.command('broadcast'), group=2)
async def broadcast(client, message):

    if not message.from_user.id in ADMINS: return await message.reply_sticker("CAACAgUAAxkBAALLp2E4bjXABidlSljadW7I--wNuyO8AAK9AwACoNa5VCN7pl8kEyPsIAQ")

    if not message.reply_to_message: return await message.reply("__📢 Please Reply To A Message To Broadcast It__")
        
    user_ids = await get_users()
    m = await message.reply('__Broadcasting message, Please wait__')    
    
    success = 0
    deleted = 0
    blocked = 0
    peerid = 0
    
    for user_id in user_ids:
        try:
            await message.reply_to_message.copy(user_id)
            success += 1
        except FloodWait as e:
            await asyncio.sleep(e.x)
            await message.copy(user_id)
            success += 1

        except UserIsBlocked:
            blocked += 1
            await del_from_userbase(user_id)

        except PeerIdInvalid:
            peerid += 1

        except InputUserDeactivated:
            deleted += 1
            await del_from_userbase(user_id)
            
    await m.edit(f"""
**📢 Broadcast Completed.**
    
**Total users:** {str(len(user_ids))}
**Blocked users:** {str(blocked)}
**Deleted accounts:** {str(deleted)}
**Send Failed:** {str(peerid)}
""")
