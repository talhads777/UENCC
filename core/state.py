import json, os
from core.config import CONFIG
STATE_FILE = CONFIG['system']['state_file']
CMD_FILE = CONFIG['system']['command_file']
def read_state():
    if not os.path.exists(STATE_FILE): return {}
    with open(STATE_FILE, "r") as f: return json.load(f)
def update_state(key, value):
    state = read_state(); state[key] = value
    with open(STATE_FILE, "w") as f: json.dump(state, f, indent=4)
def push_command(cmd_dict):
    cmds = []
    if os.path.exists(CMD_FILE):
        with open(CMD_FILE, "r") as f: cmds = json.load(f)
    cmds.append(cmd_dict)
    with open(CMD_FILE, "w") as f: json.dump(cmds, f, indent=4)
def pop_commands():
    if not os.path.exists(CMD_FILE): return []
    with open(CMD_FILE, "r") as f: cmds = json.load(f)
    with open(CMD_FILE, "w") as f: json.dump([], f)
    return cmds
