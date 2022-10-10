import argparse, json, os, time
from os.path import dirname,join,abspath
from configparser import ConfigParser
from pyrogram import Client
from pyrogram.errors import ChannelInvalid, FloodWait, PeerIdInvalid
from pyrogram.types import ChatPrivileges
from pandas import read_csv


def get_message(origin_chat, message_id):

	try:
		message = tg.get_messages(origin_chat, message_id)
		return message
	except FloodWait as e:
		print(f"..FloodWait {e.value} seconds..")
		time.sleep(e.value)
	except Exception as e:
		print(f"trying again... Due to: {e}")
		time.sleep(10)

	return get_message(origin_chat, message_id)

def is_empty_message(message, message_id, last_message_id) -> bool:

	if message.empty or message.service or message.dice or message.location:
		print(f"{message_id}/{last_message_id} (blank id)")
		wait_a_moment(message_id, skip=True)
		return True
	else:
		return False

def foward_photo(message, destino):

	try:
		tg.send_photo(
			chat_id=destino,
			photo=id_file(message.id)[0],
			caption=id_file(message.id)[1]
		)
		return
	except FloodWait as e:
		print(f"..FloodWait {e.value} seconds..")
		time.sleep(e.value)
	except Exception as e:
		print(f"trying again... Due to: {e}")

	foward_photo(message, destino)

def foward_text(message, destino):

	text = message.text.markdown
	try:
		tg.send_message(
			chat_id=destino,
			text=text,
			disable_notification=True,
			disable_web_page_preview=True,
		)
		return
	except FloodWait as e:
		print(f"..FloodWait {e.value} seconds..")
		time.sleep(e.value)
	except Exception as e:
		print(f"trying again... Due to: {e}")
		time.sleep(10)

	foward_text(message, destino)

def foward_document(message, destino):

	try:
		tg.send_document(
			chat_id=destino,
			document=id_file(message.id)[0],
			caption=id_file(message.id)[1]
		)
		return
	except FloodWait as e:
		print(f"..FloodWait {e.value} seconds..")
		time.sleep(e.value)
	except Exception as e:
		print(f"trying again... Due to: {e}")

	foward_document(message, destino)

def foward_audio(message, destino):

	try:
		tg.send_audio(
			chat_id=destino,
			audio=id_file(message.id)[0],
			caption=id_file(message.id)[1]
		)
		return
	except FloodWait as e:
		print(f"..FloodWait {e.value} seconds..")
		time.sleep(e.value)
	except Exception as e:
		print(f"trying again... Due to: {e}")

	foward_audio(message, destino)

def foward_voice(message, destino):

	try:
		tg.send_voice(
			chat_id=destino,
			voice=id_file(message.id)[0],
			caption=id_file(message.id)[1]
		)
		return
	except FloodWait as e:
		print(f"..FloodWait {e.value} seconds..")
		time.sleep(e.value)
	except Exception as e:
		print(f"trying again... Due to: {e}")

	foward_voice(message, destino)

def foward_video_note(message, destino):

	try:
		tg.send_video_note(
			chat_id=destino,
			video_note=id_file(message.id)[0],
			caption=id_file(message.id)[1]
		)
		return
	except FloodWait as e:
		print(f"..FloodWait {e.value} seconds..")
		time.sleep(e.value)
	except Exception as e:
		print(f"trying again... Due to: {e}")

	foward_video_note(message, destino)

def foward_video(message, destino):

	try:
		tg.send_video(
			chat_id=destino,
			video=id_file(message.id)[0],
			caption=id_file(message.id)[1]
		)
		return
	except FloodWait as e:
		print(f"..FloodWait {e.value} seconds..")
		time.sleep(e.value)
	except Exception as e:
		print(f"trying again... Due to: {e}")

	foward_video(message, destino)

def foward_poll(message, destino):

	if message.poll.type != "regular":
		return
	try:
		tg.send_poll(
			chat_id=destino,
			question=message.poll.question,
			options=[option.text for option in message.poll.options],
			is_anonymous=message.poll.is_anonymous,
			allows_multiple_answers=message.poll.allows_multiple_answers,
			disable_notification=True,
		)
		return
	except FloodWait as e:
		print(f"..FloodWait {e.value} seconds..")
		time.sleep(e.value)
	except Exception as e:
		print(f"trying again... Due to: {e}")
		time.sleep(10)

	foward_poll(message, destino)

def get_sender(message):

	if message.photo:
		return foward_photo
	if message.text:
		return foward_text
	if message.document:
		return foward_document
	if message.sticker:pass
	if message.animation:pass
	if message.audio:
		return foward_audio
	if message.voice:
		return foward_voice
	if message.video:
		return foward_video
	if message.video_note:
		return foward_video_note
	if message.poll:
		return foward_poll

	print("\nNot recognized message type:\n")
	print(message)
	raise Exception


def check_chat_id(chat_id):

	try:
		chat_obj = tg.get_chat(chat_id)
		chat_title = chat_obj.title
		return chat_title
	except ChannelInvalid:  # When you are not part of the channel
		print("\nNon-accessible chat")
		if MODE == "bot":
			print(
				"\nCheck that the bot is part of the chat as an administrator."
				+ "It is necessary for bot mode."
			)
		else:
			print("\nCheck that the user account is part of the chat.")
		return False
	except PeerIdInvalid:  # When the chat_id is invalid
		print(f"\nInvalid chat_id: {chat_id}")
		return False
