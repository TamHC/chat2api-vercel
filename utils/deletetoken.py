import time

import chatgpt.globals as globals
from chatgpt.refreshToken import save_refresh_map
from chatgpt.wssClient import save_wss_map

from utils.Logger import logger


async def write_token_file(token_file,token_list):
    try:           
        content = "\n".join(token_list).encode() + '\n'.encode()
        globals.dbx.files_upload(content, token_file, mode=globals.WriteMode('overwrite'))
    except Exception as e:
        logger.error(f"write file error.{str(e)}")


async def del_token(token):
    if token in refresh_map.keys():
        del refresh_map[token]
        await save_refresh_map(globals.refresh_map)
    if token in wss_map.keys():
        del wss_map[token]
        await save_wss_map(globals.wss_map)
    if token in token_list:
        globals.token_list.remove(token)
        await write_token_file(globals.TOKENS_FILE, globals.token_list)
    if token not in error_token_list:
        globals.error_token_list.append(token)
        await write_token_file(globals.ERROR_TOKENS_FILE, globals.error_token_list)
