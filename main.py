import os
import random
import requests
import json
import discord
from datetime import datetime
from threading import Thread
from pystyle import Colors, Colorate, Center, Write
import asyncio
import sys


class Worker(Thread):
    def __init__(self, target, args):
        super().__init__()
        self.target = target
        self.args = args

    def run(self):
        self.target(*self.args)


def loadtokens(filename):
    try:
        with open(filename, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        Write.Print("Token file not found.\n", Colors.red_to_yellow, interval=0.01)
        return []


def validatetoken(token):
    headers = {"Authorization": token}
    response = requests.get("https://discord.com/api/v10/users/@me", headers=headers)
    if response.status_code == 200:
        return True, response.json()
    elif response.status_code == 401:
        return False, None
    else:
        return False, response.text


def getrandomstatus(filename):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            activitytype = random.choice(list(data.keys()))
            activityname = random.choice(data[activitytype])
            return activitytype, activityname
    except:
        Write.Print("Error loading statuses. Ensure data.json is properly formatted.\n", Colors.red_to_yellow, interval=0.01)
        return "playing", "Default Status"


class Aizerxd(discord.Client):
    def __init__(self, token, activity_file, ready_event):
        super().__init__()
        self.token = token
        self.activity_file = activity_file
        self.ready_event = ready_event

    async def on_ready(self):
        ct = datetime.now().strftime("%H:%M:%S")
        user_info = self.user
        username = user_info.name
        discriminator = user_info.discriminator
        activitytype, activityname = getrandomstatus(self.activity_file)
        status = random.choice(["dnd", "idle", "online"])
        print(Colorate.Horizontal(
            Colors.green_to_white,
            f"[{ct}] SUCCESSFULLY LOGIN TOKEN => {self.token[:25]}********** USERNAME => {username}#{discriminator} TYPE => {activitytype.upper()} STATUS => {activityname} USER STATUS => {status.upper()}",
            1
        ))

        await self.setstatus(activitytype, activityname, status)

        self.ready_event.set() 

    async def setstatus(self, activitytype, activityname, status):
        activity = None

        if activitytype == "playing":
            activity = discord.Game(name=activityname)
        elif activitytype == "watching":
            activity = discord.Activity(type=discord.ActivityType.watching, name=activityname)
        elif activitytype == "listening":
            activity = discord.Activity(type=discord.ActivityType.listening, name=activityname)
        elif activitytype == "streaming":
            activity = discord.Streaming(name=activityname, url="https://twitch.tv/example")

        if activity:
            await self.change_presence(status=discord.Status(status), activity=activity)
            ct = datetime.now().strftime("%H:%M:%S")
            # print(Colorate.Horizontal(
            #     Colors.cyan_to_blue,
            #     f"[{ct}] TOKEN => {self.token[:25]}********** TYPE => {activitytype.upper()} STATUS => {activityname} USER STATUS => {status.upper()}",
            #     1
            # ))

    async def start_bot(self):
        try:
            await self.start(self.token)
        except discord.errors.LoginFailure:
            ct = datetime.now().strftime("%H:%M:%S")
            Write.Print(f"[E] TOKEN => {self.token[:25]}********** INVALID [{ct}]\n", Colors.red_to_yellow, interval=0.01)
        except Exception as e:
            Write.Print(f"[E] ERROR: {e}\n", Colors.red_to_yellow, interval=0.01)


def startselfbot(token, activity_file, ready_event):
    bot = Aizerxd(token, activity_file, ready_event)
    asyncio.run(bot.start_bot())


def setstatuses(validtokens, activity_file):
    async def set_all_statuses():
        tasks = []
        for bot in bots:
            tasks.append(bot.setstatus())
        await asyncio.gather(*tasks)

    bots = []
    for token in validtokens:
        bot = Aizerxd(token, activity_file, asyncio.Event())
        bots.append(bot)

    asyncio.run(set_all_statuses())


def stop_program():
    Write.Print("[I] Stopping the program...\n", Colors.red_to_yellow, interval=0.01)
    sys.exit(0)


def mui():
    while True:
        user_input = input("Press 's' to stop the program: ")
        if user_input.lower() == "s":
            stop_program()


def main():
    os.system("cls" if os.name == "nt" else "clear")
    
    art = """
    ███╗   ███╗ █████╗ ███████╗███████╗    ██╗  ██╗ ██████╗ ███████╗████████╗███████╗██████╗ 
    ████╗ ████║██╔══██╗██╔════╝██╔════╝    ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗
    ██╔████╔██║███████║███████╗███████╗    ███████║██║   ██║███████╗   ██║   █████╗  ██████╔╝
    ██║╚██╔╝██║██╔══██║╚════██║╚════██║    ██╔══██║██║   ██║╚════██║   ██║   ██╔══╝  ██╔══██╗
    ██║ ╚═╝ ██║██║  ██║███████║███████║    ██║  ██║╚██████╔╝███████║   ██║   ███████╗██║  ██║
    ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝    ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
    """
    print(Center.XCenter(Colorate.Horizontal(Colors.blue_to_cyan, art, 1)))

    tokens = loadtokens("data/tokens.txt")
    if not tokens:
        Write.Print("[E] No valid tokens found. Exiting...\n", Colors.red_to_yellow, interval=0.01)
        return

    validtokens = []
    Write.Print("[C] Checking all tokens...\n", Colors.green_to_white, interval=0.01)
    
    
    def validate_and_append(token):
        isvalid, _ = validatetoken(token)
        if isvalid:
            validtokens.append(token)

    
    workers = [Worker(target=validate_and_append, args=(token,)) for token in tokens]
    for worker in workers:
        worker.start()

    for worker in workers:
        worker.join()

    Write.Print(f"[I] VALID TOKENS => {len(validtokens)}\n", Colors.green_to_white, interval=0.01)

    if not validtokens:
        Write.Print("[E] No valid tokens to start. Exiting...\n", Colors.red_to_yellow, interval=0.01)
        return

    threads = []
    ready_events = [asyncio.Event() for _ in validtokens]

    
    for token, event in zip(validtokens, ready_events):
        thread = Worker(target=startselfbot, args=(token, "data/data.json", event))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    
    os.system("cls" if os.name == "nt" else "clear")
    print(Center.XCenter(Colorate.Horizontal(Colors.blue_to_cyan, art, 1)))

    
    inpt = Thread(target=mui)
    inpt.daemon = True
    inpt.start()

    setstatuses(validtokens, "data/data.json")

if __name__ == "__main__":
    main()
