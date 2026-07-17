import streamlit as st, json, os, time
st.set_page_config(page_title="UENCC Dashboard", layout="wide")
st.title("UENCC - Unified Executive & Network Command Center")
def get_state():
    try:
        with open("uencc_state.json", "r") as f: return json.load(f)
    except: return {}
def send_command(cmd, payload=None):
    cmds = []
    if os.path.exists("uencc_commands.json"):
        with open("uencc_commands.json", "r") as f: cmds = json.load(f)
    cmds.append({"command": cmd, "payload": payload or {}})
    with open("uencc_commands.json", "w") as f: json.dump(cmds, f)
    st.toast(f"Command '{cmd}' sent!")
state = get_state()
tab1, tab2, tab3, tab4 = st.tabs(["Executive", "Network", "Automation", "Logs"])
with tab1:
    st.header("Executive OS")
    exec_state = state.get("executive", {})
    st.metric("Vault Health", exec_state.get("vault_health", "Unknown"))
    st.metric("Files", exec_state.get("file_count", 0))
    for c in exec_state.get("clusters", []): st.markdown(f"- {c}")
    agent_state = state.get("agents", {})
    for d in agent_state.get("pending_decisions", []): st.info(f"[{d['status']}] {d['task']}")
with tab2:
    st.header("Network Command Center")
    net_state = state.get("network", {})
    vpn = net_state.get("vpn", {})
    st.metric("VPN", "Connected" if vpn.get("vpn_connected") else "Disconnected")
    st.metric("Tor", "Active" if vpn.get("tor_active") else "Inactive")
    st.json(net_state.get("last_scan", {}))
    with st.form("port_forward"):
        port = st.number_input("Port", value=8080)
        ip = st.text_input("Internal IP", value="192.168.1.10")
        if st.form_submit_button("Forward Port"): send_command("forward_port", {"port": port, "ip": ip})
with tab3:
    st.header("Automation")
    agent_state = state.get("agents", {})
    st.metric("Cognitive Load", agent_state.get("cognitive_load", "Unknown"))
    if st.button("Run Multi-Agent Simulation"): send_command("run_simulation")
    if st.button("Network Scan"): send_command("scan_network")
with tab4:
    st.header("Logs")
    try:
        with open("uencc.log", "r") as f: st.code("".join(f.readlines()[-20:]), language="log")
    except: st.error("No logs yet")
time.sleep(2); st.rerun()
