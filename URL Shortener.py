import json
import random
import string
from pathlib import Path


DATA_FILE = Path("short_urls.json")
BASE_URL = "https://short.local/"
CODE_LENGTH = 6


def load_urls():
    if DATA_FILE.exists():
        with DATA_FILE.open("r") as file:
            return json.load(file)
    return {}


def save_urls(urls):
    with DATA_FILE.open("w") as file:
        json.dump(urls, file, indent=4)


def fix_url(url):
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url


def make_code(urls):
    characters = string.ascii_letters + string.digits
    code = ""

    while code == "" or code in urls:
        code = ""
        for count in range(CODE_LENGTH):
            code = code + random.choice(characters)

    return code


def shorten_url(long_url):
    urls = load_urls()
    long_url = fix_url(long_url)

    for code in urls:
        if urls[code] == long_url:
            return BASE_URL + code

    code = make_code(urls)
    urls[code] = long_url
    save_urls(urls)
    return BASE_URL + code


def expand_url(short_url):
    urls = load_urls()
    code = short_url.strip().split("/")[-1]

    if code in urls:
        return urls[code]
    return "Short URL not found."


def get_input(prompt):
    try:
        return input(prompt).strip()
    except EOFError:
        return "3"


def main():
    while True:
        print("\nURL Shortener")
        print("1. Shorten a URL")
        print("2. Expand a short URL")
        print("3. Quit")

        choice = get_input("Choose an option: ")

        if choice == "1":
            long_url = get_input("Enter the long URL: ")
            if long_url == "":
                print("URL cannot be empty.")
            else:
                print("Short URL:", shorten_url(long_url))

        elif choice == "2":
            short_url = get_input("Enter the short URL or code: ")
            if short_url == "":
                print("Short URL cannot be empty.")
            else:
                print("Original URL:", expand_url(short_url))

        elif choice == "3":
            print("Goodbye.")
            break

        else:
            print("Please choose 1, 2, or 3.")


main()
