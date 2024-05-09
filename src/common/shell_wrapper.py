import os
import fabric
import atexit
import subprocess
from enum import Enum
from typing import Optional
from abc import ABC, abstractmethod

class Shell(ABC):
    @abstractmethod
    def run(self, cmd_str: str):
        pass

    @abstractmethod
    def install(self, url: str, dst_dir: Optional[str] = None):
        pass


class LocalShell(Shell):
    def run(self, cmd_str: str):
        cmd = cmd_str.strip()
        try:
            subprocess.run(cmd, shell=True, text=True, check=True)
        
        except subprocess.CalledProcessError as e:
            print(f"ERROR: {e}")

    def install(self, url: str, dst_dir: Optional[str] = None):
        self.run(f"curl -LO {url}")

        if dst_dir is not None:
            self.run(f"mv {os.path.basename(url)} {dst_dir}")


class RemoteShell_AuthType(Enum):
    PASSWORD = 0
    PRIVATE_KEY = 1

class RemoteShell(ABC):
    def _run(self, conn: fabric.Connection, cmd_str: str):
        cmd = cmd_str.strip()

        result = conn.run(cmd)

        if result.failed:
            print(f"ERROR: {result.stderr}")

    def _log_in(self) -> fabric.Connection:
        conn: fabric.Connection

        if self.auth_type == RemoteShell_AuthType.PASSWORD:
            conn = fabric.Connection(self.remote, user=self.user, connect_kwargs={"password": self.password})
        
        elif self.auth_type == RemoteShell_AuthType.PRIVATE_KEY:
            conn = fabric.Connection(self.remote, user=self.user, connect_kwargs={"key_filename": self.priv_key_path})
        
        else:
            raise Exception("Invalid authentication type")

        # Fabric actually only connects when a command is run,
        # this is a dummy command to force the connection
        try:
            self._run(conn, r"echo Connected to remote shell $SHELL")

        except Exception as e:
            print(e)
            raise Exception("ERROR: Could not connect to remote shell, check your credentials")

        return conn

    def _exit_handler(self):
        self.conn.close()
        os.remove(self._tmp_folder, missing_ok=True)

    def __init__( self,
                  remote: str,
                  user: str,
                  password: Optional[str] = None,
                  priv_key: Optional[str] = None ):

        self.local_shell = LocalShell()

        self.remote = remote
        self.user = user
        self.password = password
        self.priv_key_path = priv_key

        self.auth_type: RemoteShell_AuthType

        # Password authentication
        if self.password is not None:
            self.auth_type = RemoteShell_AuthType.PASSWORD
        
        # Private key authentication
        else:
            self.auth_type = RemoteShell_AuthType.PRIVATE_KEY

            # Use default private key path if not specified
            if self.priv_key_path is None:
                home = os.path.expanduser("~")
                self.priv_key_path = os.path.join(home, ".ssh", "id_rsa")
            else:
                self.priv_key_path = priv_key
        
        # Establish connection
        self._conn = self._log_in()

        self._tmp_folder = "/tmp/remote_shell_tmp"

        os.remove(self._tmp_folder, missing_ok=True)
        os.makedirs(self._tmp_folder, exist_ok=True)


    def run(self, cmd_str: str):
        self._run(self._conn, cmd_str)

    def install(self, url: str, dst_dir: Optional[str] = None):
        """
        curl the file locally then sftp it
        to the remote machine
        """
        self.local_shell.install(url)

        filename = url.split("/")[-1]

        self.conn.put(filename)
        self.conn.run(f"mv {filename} {dst_dir}")
