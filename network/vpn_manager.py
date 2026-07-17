import psutil
from core.logger import get_logger
logger = get_logger("VPNManager")
class VPNManager:
    def check_status(self):
        interfaces = psutil.net_if_addrs()
        vpn_active = any(iface.startswith(('wg', 'tun', 'tap')) for iface in interfaces)
        tor_active = "tor" in (p.name().lower() for p in psutil.process_iter(['name']))
        return {"vpn_connected": vpn_active, "tor_active": tor_active, "peers": 2 if vpn_active else 0}
