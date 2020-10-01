# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""Filterlər
komutlar:
.addblacklist
.listblacklist
.rmblacklist"""
import re

from telethon import events

import userbot.plugins.sql_helper.blacklist_sql as sql
from userbot.utils import admin_cmd, edit_or_reply, sudo_cmd


@borg.on(events.NewMessage(incoming=True))
async def on_new_message(event):
    # TODO: exempt admins from locks
    name = event.raw_text
    snips = sql.get_chat_blacklist(event.chat_id)
    for snip in snips:
        pattern = r"( |^|[^\w])" + re.escape(snip) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            try:
                await event.delete()
            except Exception:
                await event.reply("Bu söhbətdə SİLMƏK icazəm yoxdur")
                sql.rm_from_blacklist(event.chat_id, snip.lower())
            break


@borg.on(admin_cmd("textblacklist ((.|\n)*)"))
@borg.on(sudo_cmd("textblacklist ((.|\n)*)", allow_sudo=True))
async def on_add_black_list(event):
    starksayxd = await edit_or_reply(event, "Bu mətni qara siyahı xD olaraq təyin etməyə çalışırıq")
    text = event.pattern_match.group(1)
    to_blacklist = list(
        set(trigger.strip() for trigger in text.split("\n") if trigger.strip())
    )
    for trigger in to_blacklist:
        sql.add_to_blacklist(event.chat_id, trigger.lower())
    await starksayxd.edit(
        "{} cari söhbətdəki qara siyahıya əlavə edildi".format(
            len(to_blacklist)
        )
    )


@borg.on(admin_cmd("Qara siyahı"))
@borg.on(sudo_cmd("Qara siyahı", allow_sudo=True))
async def on_view_blacklist(event):
    sensibleleecher = await edit_or_reply(event, "Qara siyahı xD")
    all_blacklisted = sql.get_chat_blacklist(event.chat_id)
    OUT_STR = "Mövcud Söhbətin Qara Siyahıları:\n"
    if len(all_blacklisted) > 0:
        for trigger in all_blacklisted:
            OUT_STR += f"👉 {trigger} \n"
    else:
        OUT_STR = "'Qara siyahı yoxdur.Addblacklist istifadə edərək yadda saxlamağa başlayın'"
    if len(OUT_STR) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(OUT_STR)) as out_file:
            out_file.name = "blacklist.text"
            await borg.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption="Mövcud Söhbətin Qara Siyahıları",
                reply_to=event,
            )
            await event.delete()
    else:
        await sensibleleecher.edit(OUT_STR)


@borg.on(admin_cmd("rmblacklist ((.|\n)*)"))
@borg.on(sudo_cmd("rmblacklist ((.|\n)*)", allow_sudo=True))
async def on_delete_blacklist(event):
    sensibleisleecher = await edit_or_reply(event, "Tamam Bu Qara Siyahı XD-nin Silinməsi")
    text = event.pattern_match.group(1)
    to_unblacklist = list(
        set(trigger.strip() for trigger in text.split("\n") if trigger.strip())
    )
    successful = 0
    for trigger in to_unblacklist:
        if sql.rm_from_blacklist(event.chat_id, trigger.lower()):
            successful += 1
    await sensibleisleecher.edit(
        f"Silindi {successful} / {len(to_unblacklist)} qara siyahıdan"
    )
