import os; import atexit; import base64; import shutil; from datetime import datetime
all_lst = {}; global current_lst; current_lst = None
DELIMITER = "|" + "\x1F\x1E\x1D\x1C\x1B"; KEY = "jeans2025"
AUTOSAVE_FILE = "jeans/autosave.txt"
MAX_BACKUPS = 10

def set_autosave_file(filename):
    global AUTOSAVE_FILE
    if not filename.endswith('.txt'):
        filename += '.txt'
    AUTOSAVE_FILE = filename

def get_backup_filename():
    base_name = os.path.basename(AUTOSAVE_FILE).replace('.txt', '')
    return f"backup/{base_name}_backup.txt"

def manage_backups():
    backup_file = get_backup_filename()
    if not os.path.exists(backup_file): return
    try:
        with open(backup_file, 'r') as f: lines = f.readlines()
        if len(lines) >= MAX_BACKUPS: lines = lines[-(MAX_BACKUPS-1):]
        with open(backup_file, 'w') as f: f.writelines(lines)
    except Exception as e: print(f"Well butter my biscuit, backup management done went sideways: {e}")

def save_to_backup(data):
    backup_file = get_backup_filename()
    try:
        os.makedirs(os.path.dirname(backup_file), exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(backup_file, 'a') as f: f.write(f"[{timestamp}] {data}\n")
        manage_backups()
    except Exception as e: print(f"Lord have mercy, backup save got all cattywampus: {e}")

def list_backups():
    backup_file = get_backup_filename()
    if not os.path.exists(backup_file): print("Well I'll be hornswoggled, ain't no backup file to be found"); return []
    try:
        with open(backup_file, 'r') as f: lines = f.readlines()
        return [(i+1, line[1:20]) for i, line in enumerate(lines) if line.startswith('[')]
    except Exception as e: print(f"Bless your heart, couldn't wrangle them backups: {e}"); return []

def restore_from_backup(backup_number):
    backup_file = get_backup_filename()
    if not os.path.exists(backup_file): print("Well shoot, ain't no backup file 'round these parts"); return False
    try:
        with open(backup_file, 'r') as f: lines = f.readlines()
        if backup_number < 1 or backup_number > len(lines): print("That backup number's about as useful as a screen door on a submarine"); return False
        backup_line = lines[backup_number - 1]
        if not backup_line.startswith('['): print("This here backup format's more confused than a cat in a dog house"); return False
        encrypted_data = backup_line[22:].strip()
        global all_lst, current_lst
        content = decrypt_data(encrypted_data); parts = content.split(DELIMITER)
        if len(parts) < 2: print("This backup data's emptier than a politician's promise"); return False
        num_lists = int(parts[0]); all_lst.clear(); idx = 1
        for _ in range(num_lists):
            if idx >= len(parts): break
            list_name = parts[idx]; list_size = int(parts[idx + 1]); idx += 2; new_list = []
            for _ in range(list_size):
                if idx >= len(parts): break
                item = parts[idx]
                try:
                    if '.' in item: new_list.append(float(item))
                    elif item.lstrip('-').isdigit(): new_list.append(int(item))
                    else: new_list.append(item)
                except ValueError: new_list.append(item)
                idx += 1
            all_lst[list_name] = new_list
        if idx < len(parts):
            current_info = parts[idx]
            if current_info.startswith("CURRENT:"):
                current_name = current_info[8:]
                if current_name != "None" and current_name in all_lst: current_lst = all_lst[current_name]
        print(f"Hot diggity dog! Successfully rustled up backup #{backup_number} like a Sunday barbecue"); return True
    except Exception as e: print(f"Well ain't that a fine howdy-do, backup restoration got itself in a pickle: {e}"); return False
def encrypt_data(data):
    encrypted = [chr(ord(char) ^ ord(KEY[i % len(KEY)])) for i, char in enumerate(data)]
    return base64.b64encode(''.join(encrypted).encode('utf-8')).decode('utf-8')

def decrypt_data(data):
    try:
        decoded = base64.b64decode(data.encode('utf-8')).decode('utf-8')
        return ''.join([chr(ord(char) ^ ord(KEY[i % len(KEY)])) for i, char in enumerate(decoded)])
    except: return data 

def jeans_off():
    try:
        dir_path = os.path.dirname(AUTOSAVE_FILE)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        data = f"{len(all_lst)}{DELIMITER}"
        for name, lst in all_lst.items():
            data += f"{name}{DELIMITER}{len(lst)}{DELIMITER}"
            for item in lst: data += f"{item}{DELIMITER}"
        current_name = None
        for name, lst in all_lst.items():
            if lst is current_lst: current_name = name; break
        data += f"CURRENT:{current_name or 'None'}"
        
        encrypted_data = encrypt_data(data)
        
        save_to_backup(encrypted_data)
        
        with open(AUTOSAVE_FILE, "w") as f: f.write(encrypted_data)
        print("Y'all's database is now snug as a bug in a rug with that fancy encryption")
        print(f"Got your backup saved faster than you can say 'sweet tea' (keepin' the last {MAX_BACKUPS} saves)")
    except Exception as e: print(f"Well shucks, the persistence layer got more tangled than Christmas lights: {e}")

def jeans_on():
    global current_lst, all_lst
    try:
        if os.path.exists(AUTOSAVE_FILE):
            with open(AUTOSAVE_FILE, "r") as f: encrypted_content = f.read()
            content = decrypt_data(encrypted_content); parts = content.split(DELIMITER)
            if len(parts) < 2: return
            num_lists = int(parts[0]); all_lst.clear(); idx = 1
            for _ in range(num_lists):
                if idx >= len(parts): break
                list_name = parts[idx]; list_size = int(parts[idx + 1]); idx += 2
                new_list = []
                for _ in range(list_size):
                    if idx >= len(parts): break
                    item = parts[idx]
                    try:
                        if '.' in item: new_list.append(float(item))
                        elif item.lstrip('-').isdigit(): new_list.append(int(item))
                        else: new_list.append(item)
                    except ValueError: new_list.append(item)
                    idx += 1
                all_lst[list_name] = new_list
            if idx < len(parts):
                current_info = parts[idx]
                if current_info.startswith("CURRENT:"):
                    current_name = current_info[8:]
                    if current_name != "None" and current_name in all_lst: current_lst = all_lst[current_name]
            print(f"Well howdy! Done loaded up {len(all_lst)} collections slicker than butter on a hot skillet")
    except Exception as e: print(f"Dadgum it, data hydration went and got itself all discombobulated: {e}")

def show_all():
	print("Looky here at all them collections we got cookin' in memory:\n"); [print(f"{x}\n") for x in all_lst]

def format_list(lst, delimeter):
	y = ""; [y := f"{y}{delimeter}{x}" for x in lst]; return f"{len(lst)}{y}"

def jeans(lst, delimeter, option, fname):
    try:
        try: os.mkdir("jeans")
        except FileExistsError: pass
        file_n = f"jeans/{fname}.txt"
        if option == 1:
            with open(file_n, "w") as txt: txt.write(format_list(lst, delimeter)); print("Collection's all tucked away nice and proper in storage")
        if option == 2:
            with open(file_n, "r") as txt: the_str = txt.read(); the_lst = the_str.split(delimeter); len_lst = int(the_lst[0]); lst.clear()
            for i in range(1, len_lst + 1):
                if i < len(the_lst):
                    item = the_lst[i]
                    try:
                        if '.' in item: lst.append(float(item))
                        elif item.lstrip('-').isdigit(): lst.append(int(item))
                        else: lst.append(item)
                    except ValueError: lst.append(item)
            print(f"Well ain't that something, collection loaded up like a pickup truck: {lst}")
    except Exception as e: print(e)

def make_list():
    lstname = input(f"Collection name: "); new_list = []; all_lst[lstname] = new_list; print(f"Well butter my grits! New collection '{lstname}' is ready to roll in memory")
    global current_lst; current_lst = new_list

def yo(val, lst=None):
    if lst is None: lst = current_lst
    if lst is None: print("Hold your horses there, partner! Ain't no collection picked out yet"); return
    print(f"Fixin' to work on this here collection: {lst}")
    if val == 1:  # Add
        x = input("What you want to add to this collection ('q' to mosey on out): ")
        if x == "q": return
        try:
            if '.' in x: lst.append(float(x))
            else: lst.append(int(x))
        except ValueError: lst.append(x)
        print(f"Well I'll be jiggered! Added '{x}' to the collection\n{lst}"); yo(1, lst)
    elif val == 2: # Delete
        x = input("What you want to boot out of this collection ('q' to skedaddle): ")
        if x == "q": return
        try:
            if '.' in x: lst.remove(float(x))
            elif x.isdigit(): lst.remove(int(x))
            else: lst.remove(x)
            print(f"Gave '{x}' the old heave-ho from the collection\n{lst}")
        except ValueError: print(f"Well ain't that peculiar, '{x}' ain't nowhere to be found in this collection")
        yo(2, lst)
    elif val == 3:  # Edit
        if len(lst) == 0: print("This collection's emptier than a barn in winter, nothing to fiddle with"); return
        try:
            index = int(input(f"Which spot you want to tinker with (0-{len(lst)-1}): "))
            if 0 <= index < len(lst):
                old_value = lst[index]; print(f"Right now at spot {index} we got: {old_value}")
                new_value = input("What you want to put there instead: ")
                try:
                    if '.' in new_value: lst[index] = float(new_value)
                    elif new_value.lstrip('-').isdigit(): lst[index] = int(new_value)
                    else: lst[index] = new_value
                except ValueError: lst[index] = new_value
                print(f"Switched out {old_value} for {lst[index]} slick as you please"); print(f"Collection's looking like: {lst}")
            else: print("That spot's about as real as a three-dollar bill")
        except ValueError: print("That index format's more confused than a mosquito in a mannequin factory")
    elif val == 4: lst.sort(key=lambda item: (type(item).__name__, str(item).lower())); print(f'Got that collection sorted neater than Sunday shoes\n{lst}')
    elif val == 5: print(lst)
    else: print("Well bless your heart, that operation ain't something I know how to do")

def load_list():
    global current_lst; fname = input("What file you want to rustle up (no extension): ")
    if fname:
        try:
            temp_list = []; jeans(temp_list, DELIMITER, 2, fname)
            if temp_list: current_lst = temp_list; all_lst[fname] = current_lst; print(f"Well I'll be hornswoggled! Loaded {fname}.txt into active memory like a dream")
            else: print("That file's about as empty as a politician's soul, or maybe it ain't there at all")
        except Exception as e: print(f"Shoot, couldn't wrangle that file back to life: {e}")

def save_current_list():
    if current_lst is None or len(current_lst) == 0: print("Ain't got nothing worth saving right now, sugar"); return
    fname = input("What you want to call this file (no extension): ")
    if fname: jeans(current_lst, DELIMITER, 1, fname)

def run_app():
    jeans_on()
    while True:
        try:   
            i = input('Action [add/del/edit/sort/all/new/save/load/backups/restore] or "q" to terminate: ').lower()
            if i == "add": yo(1)
            elif i == "del": yo(2)
            elif i == "edit": yo(3)
            elif i == "sort": yo(4)
            elif i == "all": yo(5)
            elif i == "new": make_list()
            elif i == "save": save_current_list()
            elif i == "load": load_list()
            elif i == "lists": show_all()
            elif i == "backups":
                backups = list_backups()
                if backups: print("Here's all them backups we got stored up:"); [print(f"  {num}. {timestamp}") for num, timestamp in backups]
                else: print("Ain't got no backups to speak of right now")
            elif i == "restore":
                backups = list_backups()
                if backups:
                    print("Pick one of these here backups to bring back:"); [print(f"  {num}. {timestamp}") for num, timestamp in backups]
                    try: backup_num = int(input("Which backup number you want (enter the number): ")); restore_from_backup(backup_num)
                    except ValueError: print("That number's about as valid as a two-headed quarter")
                else: print("Sorry partner, ain't got no backups to restore from")
            elif i == "q": jeans_off(); break
            else: print("Well butter my biscuit, that command ain't ringing any bells. Try again, sugar.")
        except Exception as e: print(e)

def create_file_handler():
    """Create a file handler interface for external use"""
    class JeansHandler:
        def __init__(self):
            jeans_on()  # Load existing data
        
        def create_collection(self, name):
            global all_lst, current_lst
            all_lst[name] = []
            current_lst = all_lst[name]
            return True
        
        def add_item(self, collection_name, item):
            global all_lst
            if collection_name in all_lst:
                all_lst[collection_name].append(item)
                jeans_off()  # Save after each operation
                return True
            return False
        
        def get_collection(self, collection_name):
            return all_lst.get(collection_name, [])
        
        def list_collections(self):
            return list(all_lst.keys())
        
        def save(self):
            jeans_off()
            return True
    
    return JeansHandler()

atexit.register(jeans_off)

if __name__ == "__main__":
    run_app()