import socket

from aws_xray_sdk.core.daemon_config import DaemonConfig
from .base import Emitter
from .constants import DEFAULT_DAEMON_ADDRESS


class UDPEmitter(Emitter):
    """
    The default emitter the X-Ray recorder uses to send segments/subsegments
    to the X-Ray daemon over UDP using a non-blocking socket. If there is an
    exception on the actual data transfer between the socket and the daemon,
    it logs the exception and continue.
    """
    def __init__(self, daemon_address=DEFAULT_DAEMON_ADDRESS):

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.setblocking(0)
        self.set_daemon_address(daemon_address)

    def set_daemon_address(self, address):
        """
        Set up UDP ip and port from the raw daemon address
        string using ``DaemonConfig`` class utlities.
        """
        if address:
            daemon_config = DaemonConfig(address)
            self._ip, self._port = daemon_config.udp_ip, daemon_config.udp_port
