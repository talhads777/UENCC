import asyncio
from core.logger import get_logger
from core.config import CONFIG
logger = get_logger("NetworkScanner")
class Scanner:
    def __init__(self):
        self.target = CONFIG['network']['target_subnet']
        self.ports = CONFIG['network']['scan_ports']
    async def scan_ports(self, ip="127.0.0.1"):
        logger.info(f"Scanning {ip} ports {self.ports}")
        open_ports = []
        for port in self.ports:
            try:
                fut = asyncio.open_connection(ip, port)
                reader, writer = await asyncio.wait_for(fut, timeout=0.5)
                open_ports.append(port)
                writer.close(); await writer.wait_closed()
            except: pass
        logger.info(f"Open ports: {open_ports}")
        return {"ip": ip, "open_ports": open_ports}
    async def discover_devices(self):
        return [{"ip": "192.168.1.1", "mac": "00:11:22:33:44:55", "name": "Gateway"}, {"ip": "192.168.1.10", "mac": "AA:BB:CC:DD:EE:FF", "name": "ExOS-Node"}]
