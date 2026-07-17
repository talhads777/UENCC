import pytest
from network.vpn_manager import VPNManager
from network.router_bot import RouterBot

def test_vpn_manager():
    mgr = VPNManager()
    status = mgr.check_status()
    assert "vpn_connected" in status
    assert "tor_active" in status
    assert isinstance(status["vpn_connected"], bool)

def test_router_bot():
    bot = RouterBot()
    res = bot.forward_port(8080, "192.168.1.10")
    assert res["status"] == "success"
    assert "8080" in res["message"]
