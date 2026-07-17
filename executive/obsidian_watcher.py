import os, glob, asyncio
from core.logger import get_logger
from core.state import update_state
from core.config import CONFIG
logger = get_logger("ObsidianWatcher")
class ObsidianWatcher:
    def __init__(self):
        self.vault_path = CONFIG['executive']['obsidian_vault_path']
        os.makedirs(self.vault_path, exist_ok=True)
    async def watch_loop(self):
        logger.info(f"Starting Obsidian Watcher on {self.vault_path}")
        while True:
            md_files = glob.glob(os.path.join(self.vault_path, "**/*.md"), recursive=True)
            health = "Healthy" if len(md_files) > 0 else "Empty/Warning"
            clusters = ["AI Research", "Network Sec", "Personal Finance"] if md_files else []
            update_state("executive", {"vault_health": health, "file_count": len(md_files), "clusters": clusters})
            await asyncio.sleep(CONFIG['executive']['scan_interval_seconds'])
