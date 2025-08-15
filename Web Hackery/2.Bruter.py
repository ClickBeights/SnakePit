# The wordlist can be found at:
# https://cdn.invicti.com/app/uploads/2024/05/28102929/SVNDigger-1.zip?_gl=1*184utjo*_gcl_au*MTIzOTg3MTcyNi4xNzU0NDcwODAz*_ga*MTcyNDYxNjAwMi4xNzU0NDcwODA0*_ga_WWNQ4DL457*czE3NTQ0NzA4MDMkbzEkZzEkdDE3NTQ0NzA4NzQkajYwJGwwJGgw
import queue
import requests
import threading
import sys

AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/138.0.3351.121"
EXTENSIONS = ['.php', '.bak', '.orig', '.inc']
TARGET = "http://testphp.vulnweb.com"
THREADS = 5
WORDLIST = "/home/kali/Downloads/all.txt"


def get_words(resume=None):
    # An inner function and was set up this way because it will always run in the context of 'get_words'
    # we placed inside of it.
    # It's purpose is to apply a list of extensions when making requests
    def extend_words(word):
        # If the word contains a '.', we will append it to the URL.
        if "." in word:
            words.put(f'/{word}')
        # Otherwise, we will treat it as a directory name.
        else:
            words.put(f'/{word}/')

        for extension in EXTENSIONS:
            words.put(f'/{word}{extension}')

    # Read the wordlist file by iterating each word in the file.
    with open(WORDLIST) as f:
        raw_words = f.read()

    found_resume = False
    words = queue.Queue()
    for word in raw_words.split():
        # Set the resume variable to the last path tested by the brute-forcer.
        # This functionality ensures that the session is resumed if interrupted by any reason.
        if resume is not None:
            if found_resume:
                extend_words(word)
            elif word == resume:
                found_resume = True
                print(f'Resuming wordlist from: {resume}')
        else:
            # print(word)
            extend_words(word)
    # Return queue full of words to use in the attack.
    return words


# Main brute forcing function. It accepts a Queue object populated with words.
def dir_bruter(words):
    headers = {'User-Agent': AGENT}
    # Loop through each word creating a URL with each request to the target app and send it.
    while not words.empty():
        url = f'{TARGET}{words.get()}'
        try:
            r = requests.get(url, headers=headers)
        # Used to inform us about any connection error by printing an X.
        except requests.exceptions.ConnectionError:
            sys.stderr.write('x');sys.stderr.flush()
            continue

        if r.status_code == 200:
            print(f'\nSuccess ({r.status_code}: {url})')
        elif r.status_code == 404:
            sys.stderr.write('.');sys.stderr.flush()
        # Any other type of error that could be interesting in understanding the WebApp.
        else:
            print(f'{r.status_code} => {url}')

if __name__ == '__main__':
    words = get_words()
    # Polished console output
    print('=' * 60)
    print(f'NOTE: For cleaner console output, run this script as:')
    print(f'      python3 {sys.argv[0]} 2>/dev/null')
    print('=' * 60)
    input('Press Enter to continue... ')
    for _ in range(THREADS):
        t = threading.Thread(target=dir_bruter, args=(words,))
        t.start()
