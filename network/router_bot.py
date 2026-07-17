from core.logger import get_logger
logger = get_logger("RouterBot")
class RouterBot:
    def forward_port(self, port, internal_ip):
        logger.info(f"Forwarding port {port} to {internal_ip}")
        return {"status": "success", "message": f"Port {port} forwarded to {internal_ip}"}
