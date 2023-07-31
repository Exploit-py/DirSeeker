import argparse
import asyncio
import aiohttp
import platform
import os
from colorama import Fore
import pyfiglet


def check_platform():
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class Config:
    def __init__(self, args):
        self.URL = args.URL
        self.wordlist = args.wordlist
        self.verbose = args.verbose
        self.remove_anchor = args.remove_anchor
        self.threads = args.threads
        self.fix_url()
        self.fix_wordlist()

        
    def fix_url(self):
        if not self.URL.startswith(("http://", "https://")):
            self.URL = "https://" + self.URL
        
        if not self.URL.endswith("/"):
            self.URL += "/"
        
    def fix_wordlist(self):
        with open(self.wordlist, "r") as file:
            wordlist = file.readlines()

        if self.remove_anchor:
            self.wordlist = [directory.replace("#", "").strip() for directory in wordlist]
        
        else:
            self.wordlist = [directory.strip() for directory in wordlist]

class Banner:
    def __init__(self, args):
        self.URL = args.URL
        self.wordlist = args.wordlist
        self.verbose = args.verbose
        self.remove_anchor = args.remove_anchor
        self.threads = args.threads
    
    async def banner(self):
        ascii_art = pyfiglet.Figlet()
        info =  f"\n\n{Fore.RED}{'-'*20}{Fore.RESET}\n"\
                f"HOST: {Fore.MAGENTA}{self.URL}{Fore.RESET}\n"\
                f"Wordlist: {Fore.MAGENTA}{self.wordlist}{Fore.RESET}\n"\
                f"Remove Anchor: {Fore.MAGENTA}{self.remove_anchor}{Fore.RESET}\n"\
                f"Verbose: {Fore.MAGENTA}{self.verbose}{Fore.RESET}\n"\
                f"Threads: {Fore.MAGENTA}{self.threads}{Fore.RESET}\n"\
                f"{Fore.RED}{'-'*20}{Fore.RESET}\n"

        author = "Author: Exploit-py\nDate: 31/07/2023\nDiscord: .main.cpp"
        print(Fore.RED + ascii_art.renderText("DirSeeker") + Fore.RESET + author + info)
        await asyncio.sleep(0.7)


class DirSeeker(Config):
    def __init__(self, args):
        super().__init__(args)
        self.http_status_message = {200: "OK", 201: "Created", 204: "No Content", 301: "Moved Permanently", 308: "Permanent Redirect", 302: "Found (Temporary Redirect)", 307: "Temporary Redirect", 401: "Unauthorized", 403: "Forbidden", 405: "Method Not Allowed"}
    
    async def process_urls(self, url_queue):
        async with aiohttp.ClientSession() as session:
            while not url_queue.empty():
                url = await url_queue.get()
                try:
                    async with session.get(url) as response:
                        if self.verbose:
                            print(f"{Fore.GREEN if response.status in self.http_status_message else Fore.RED}"
                                  f"URL: {url}"
                                  f" | Status: {response.status} - {self.http_status_message.get(response.status, 'ERROR')}"
                                  f" | Content-Type: {response.headers.get('Content-Type')}"
                                  f" | Length: {response.headers.get('Content-Length')}\n{Fore.RESET}")

                        else:
                            if response.status in self.http_status_message:
                                print(f"{Fore.GREEN if response.status in self.http_status_message else Fore.RED}"
                                  f"URL: {url}"
                                  f" | Status: {response.status} - {self.http_status_message.get(response.status, 'ERROR')}"
                                  f" | Content-Type: {response.headers.get('Content-Type')}"
                                  f" | Length: {response.headers.get('Content-Length')}\n{Fore.RESET}")

                except aiohttp.client_exceptions.ClientConnectorError:
                    print(f"\nError connecting to {url}. Check the URL or your internet connection.\n")
                    os.abort()
                


async def main(args):
    banner_task = asyncio.create_task(Banner(args).banner())
    await banner_task

    arguments = DirSeeker(args)

    url_queue = asyncio.Queue()

    for directory in arguments.wordlist:
        url_queue.put_nowait(arguments.URL + directory.strip())

    tasks = [arguments.process_urls(url_queue) for _ in range(arguments.threads)] # quantas conexões simultâneas ele irá fazer

    print("Starting...\n")
    await asyncio.gather(*tasks)


check_platform()

parser = argparse.ArgumentParser(description="Simple script that tries to search directories of a site using bruteforce technique")

parser.add_argument("URL", type=str, help="URL that will be used to find new directories")
parser.add_argument("-w", "--wordlist", type=str, help="Wordlist that will contain the directories", required=True)
parser.add_argument("-v", "--verbose", action="store_true", help="Verbose Mode", default=False, required=False)
parser.add_argument("-t", "--threads", type=int, default=10, help="Number of simultaneous connections")
parser.add_argument("--remove_anchor", action="store_true", help="Remove Anchors (#) from wordlist", default=False, required=False)

args = parser.parse_args()

if __name__ == "__main__":
    asyncio.run(main(args))

