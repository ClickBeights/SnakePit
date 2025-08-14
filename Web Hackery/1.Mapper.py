import contextlib
import os
import queue
import requests  # This library is not built-in, must be installed. Used mainly to manage cookies.
import sys
import threading
import time

# List of file extensions that we do not want:
FILTERED = [".jpg", ".gif", ".png", ".css"]
# Define the target WordPress site:
TARGET = "http://target-website/wordpress"
THREADS = 10
# A queue object to store file paths we located locally.
answers = queue.Queue()
# A queue object to store files that we attempt to locate on remote server.
web_paths = queue.Queue()

def gather_paths():
    # Using the os.walk function to walk through in the local WebApp directory.
    for root, _, files in os.walk('.'):
        # Build the full paths to target files.
        for fname in files:
            # Test them against the Filtered list:
            if os.path.splitext(fname)[1] in FILTERED:
                continue
            path = os.path.join(root, fname)
            # Foe each valid extension, add the path to the queue
            if path.startswith('.'):
                path = path[1:]
            # Used to compare them with files found on the remote server for attack.
            print(path)
            web_paths.put(path)

# Create a simple context manager that converts a generator function into a context manager.
@contextlib.contextmanager
# This function executes code inside a different directory and guarantees smooth return to the original directory.
def chdir(path):
    """
    On enter, change directory to specified path.
    On exit, change directory to original.
    """
    this_dir = os.getcwd()
    os.chdir(path)
    try:
        # Controls back to gather_paths function.
        yield
    # This operator always executes regardless of any exceptions raised.
    finally:
        # Reverts to the original directory
        os.chdir(this_dir)

def test_remote():
    # Keep executing until web_paths is empty and grab the path from each queue iteration:
    while not web_paths.empty():
        # Add the URL to the target's URL base path.
        path = web_paths.get()
        url = f'{TARGET}{path}'
        # Target may have throttle enabled.
        time.sleep(2)
        # Attempt to retrieve it with a request.
        r = requests.get(url)
        if r.status_code == 200:
            # On success, add the URL to the answers queue.
            answers.put(url)
            # Both + and x are used to understand how the target responds.
            sys.stdout.write('+')
        else:
            # They can be substituted with valid output or removed entirely.
            sys.stdout.write('x')
        sys.stdout.flush()

def run():
    mythreads = list()
    # Starts by 10 Threads defined earlier.
    for i in range(THREADS):
        print(f'Spawning thread {i}')
        t = threading.Thread(target=test_remote)
        mythreads.append(t)
        t.start()

    for thread in mythreads:
        # Wait for all threads to complete.
        thread.join()

if __name__ == '__main__':
    # chdir contex manager inside the 'with' statement which calls the generator with the
    # directory path to execute the code in, when exiting, program returns to original directory.
    with chdir("/home/kali/Downloads/wordpress"):
        gather_paths()
    # Used to review the output so far before continuing. Should be the files we
    # want to test against the target from our local installation.
    input('Press enter to continue.')
    # Runs the files we want from our installation against the remote one.
    run()
    # The following is to save results for further review.
    with open('MappingResults.txt', 'w') as f:
        while not answers.empty():
            f.write(f'{answers.get()}\n')
    print('done')
