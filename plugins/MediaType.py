import asyncio
import logging
from typing import List, Optional, Tuple, Union
import pyrogram
import yaml

from pyrogram.types import (
Audio, Document, 
Photo, Video, 
VideoNote, Voice
)

from rich.logging import RichHandler
from utils.file_management import get_next_name, manage_duplicate_file
from utils.log import LogFilter
import argparse
from pandas import DataFrame,concat

from os.path import (
dirname,join,
abspath,isdir,
exists,getsize
)

from os import remove,system
from shutil import copy

import warnings

def _can_download(_type: str, file_formats: dict, file_format: Optional[str]) -> bool:

    if _type in ["audio", "document", "video"]:
        allowed_formats: list = file_formats[_type]
        if not file_format in allowed_formats and allowed_formats[0] != "all":
            return False
    return True


def _is_exist(file_path: str) -> bool:

    return not isdir(file_path) and exists(file_path)


async def _get_media_meta(
    media_obj: Union[Audio, Document, Photo, Video, VideoNote, Voice],
    _type: str,
) -> Tuple[str, Optional[str]]:

    if _type in ["audio", "document", "video"]:
        # pylint: disable = C0301
        file_format: Optional[str] = media_obj.mime_type.split("/")[-1]  # type: ignore
    else:
        file_format = None

    if _type in ["voice", "video_note"]:
        # pylint: disable = C0209
        file_format = media_obj.mime_type.split("/")[-1]  # type: ignore
        file_name: str = join(
            THIS_DIR,
            'downloads',
            "{}_{}.{}".format(
                _type,
                media_obj.date.isoformat(),  # type: ignore
                file_format,
            ),
        )
    else:
        file_name = join(
            THIS_DIR, 'downloads', getattr(media_obj, "file_name", None) or ""
        )
    return file_name, file_format
