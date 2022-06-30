# TODO LIST : )

## ADD
 - ~~Memoserv support.~~
 - ~~Use memopermabanmsg function?~~ <--- Permabans just give a KICK server response, there's no way to check for this.

## FIX
 - Mask & target not being passed to ``_max_msg_len``.
    - Is this even possible to keep updated reliably?
 - ~~No error message when Pesterchum fails to join a channel. (For example, when the channel name length is over CHANNELLEN)~~
 - Choose memo window doesn't get updated on theme change.
 - Right click menu's color doesn't get updated on theme change in memos.
 - help() causes console to crash...? 
    - Console is hopelessly broken, it'd be easier to make a list of what commands *don't* cause it to crash. Does anyone use this?

## CHANGE
 - When everything has been tested and more people have compatible versions, switch Pesterchum over to using metadata and message tags by default instead of wraping its protocol in PRIVMSG. The current method should stay availible for compatibility.
