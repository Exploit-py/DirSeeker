import asyncio
import argparse
import aiohttp
from colorama import Fore
import pyfiglet

accept_status = [200, 301, 403]


async def find(session, url):
    async with session.get(url) as response:
        return url, response

async def dirseeker(host, wordlist, threads, verbose=False):
    async with aiohttp.ClientSession() as session:
        tasks = []

        for directory in wordlist:
            url = f"{host}/{directory}"
            tasks.append(find(session, url)) # "agendar" requisições

            if len(tasks) == threads:
                results = await asyncio.gather(*tasks)

                if verbose:
                    for result in results:
                        response = result[1]
                        status = response.status
                        content_type = response.headers.get("Content-Type")
                        content_length = response.headers.get("Content-Length")
                        print(f"{Fore.GREEN if status in accept_status else Fore.RED}{result[0]}{'': ^10}STATUS: {status}{'': ^10}(Content Type: {content_type}, Length: {content_length}){Fore.RESET}")

                else:
                    for result in results:
                        response = result[1]
                        status = response.status
                        content_type = response.headers.get("Content-Type")
                        content_length = response.headers.get("Content-Length")
                        if status in accept_status:
                            print(f"{Fore.GREEN}{result[0]}{'': ^10}STATUS: {status}{'': ^10}(Content Type: {content_type}, Length: {content_length}){Fore.RESET}")

                tasks = []

        if tasks:
            results = await asyncio.gather(*tasks)

            for result in results:
                response = result[1]
                status = response.status
                content_type = response.headers.get("Content-Type")
                content_length = response.headers.get("Content-Length")
                print(f"{Fore.GREEN if status in accept_status else Fore.RED}{result[0]}{'': ^10}STATUS: {status}{'': ^10}(Content Type: {content_type}, Length: {content_length}){Fore.RESET}")


class Banner:
    def __init__(self, host: str, wordlist, threads: int, verbose: bool):
        self.host = host
        self.wordlist = wordlist
        self.threads = threads
        self.verbose = verbose
        self.banner()
    
    def banner(self):
        ascii_art = pyfiglet.Figlet()
        info =  f"\n\n{Fore.RED}{'-'*20}"\
                f"{Fore.RESET}\nHOSTS: {Fore.WHITE}{self.host}{Fore.RESET}\nWORDLIST: {Fore.WHITE}{self.wordlist}{Fore.RESET}\nTHREADS: {Fore.WHITE}{self.threads}{Fore.RESET}\nVERBOSE: {Fore.WHITE}{self.verbose}{Fore.RESET}\n{Fore.RED}"\
                f"{'-'*20}{Fore.RESET}"

        author = "Author: Exploit-py\nDate: 16/02/2023"
        print(Fore.RED + ascii_art.renderText("DirSeeker") + Fore.RESET + author + info)


def main():
    parser = argparse.ArgumentParser(description="Make HTTP requests to discover directories.")
    parser.add_argument("host", type=str, help="The base URL for the requests")
    parser.add_argument("wordlist", type=str, help="The file containing a list of directories to request")
    parser.add_argument("-t", "--threads", type=int, default=50, help="Threads")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show verbose output")
    args = parser.parse_args()

    with open(args.wordlist, "r") as file:
        wordlist = file.read().split("\n")

    Banner(args.host, args.wordlist, args.threads, args.verbose)
    asyncio.run(dirseeker(args.host, wordlist, args.threads, args.verbose))


if __name__ == '__main__':
    main()
