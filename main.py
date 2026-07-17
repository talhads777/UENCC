import asyncio, sys, subprocess
from core.logger import get_logger
from core.state import pop_commands, update_state, read_state
from executive.obsidian_watcher import ObsidianWatcher
from agents.orchestrator import Orchestrator
from network.scanner import Scanner
from network.vpn_manager import VPNManager
from network.router_bot import RouterBot
from integrations.telegram_bot import TelegramBot
logger = get_logger("Daemon")
async def command_processor(scanner, router, orchestrator):
    while True:
        for cmd in pop_commands():
            action = cmd.get("command")
            payload = cmd.get("payload", {})
            logger.info(f"Executing: {action}")
            if action == "scan_network":
                res = await scanner.scan_ports()
                devs = await scanner.discover_devices()
                net_state = read_state().get("network", {})
                net_state.update({"last_scan": res, "devices": devs})
                update_state("network", net_state)
            elif action == "forward_port":
                router.forward_port(payload.get("port"), payload.get("ip"))
            elif action == "run_simulation":
                await orchestrator.run_simulation()
        await asyncio.sleep(1)
async def network_monitor(vpn_mgr):
    while True:
        status = vpn_mgr.check_status()
        net_state = read_state().get("network", {})
        net_state["vpn"] = status
        update_state("network", net_state)
        await asyncio.sleep(30)
async def main():
    logger.info("Starting UENCC Daemon...")
    watcher = ObsidianWatcher()
    orchestrator = Orchestrator()
    scanner = Scanner()
    vpn_mgr = VPNManager()
    router = RouterBot()
    tg_bot = TelegramBot()
    tasks = [
        asyncio.create_task(watcher.watch_loop()),
        asyncio.create_task(orchestrator.sync_state()),
        asyncio.create_task(network_monitor(vpn_mgr)),
        asyncio.create_task(command_processor(scanner, router, orchestrator)),
        asyncio.create_task(tg_bot.poll())
    ]
    await asyncio.gather(*tasks)
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--daemon-only":
        asyncio.run(main())
    else:
        logger.info("Starting UI Subprocess...")
        ui_process = subprocess.Popen([sys.executable, "-m", "streamlit", "run", "ui/app.py", "--server.headless", "true"])
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            logger.info("Shutting down...")
            ui_process.terminate()
