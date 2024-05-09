import os
import fabric
import atexit
import subprocess
from enum import Enum
from typing import Optional
from abc import ABC, abstractmethod
from tempfile import TemporaryDirectory

class Shell(ABC):
    @abstractmethod
    def run(self, cmd_str: str):
        """
        Run a shell command
        """
        pass

    @abstractmethod
    def install(self, url: str, dst_dir: Optional[str] = None) -> str:
        """
        Install a file from a URL

        If dst_dir is None, the file is installed in the current directory

        If dst_dir doesn't exist, it is created
        """
        pass


class LocalShell(Shell):
    def run(self, cmd_str: str):
        cmd = cmd_str.strip()
        try:
            subprocess.run(cmd, shell=True, text=True, check=True)
        
        except subprocess.CalledProcessError as e:
            print(f"ERROR: {e}")

    def install(self, url: str, dst_dir: Optional[str] = None) -> str:
        filename = url.split("/")[-1]

        if dst_dir is not None:
            self.run(f"curl -LO {url}")
            return filename

        else:
            os.makedirs(dst_dir, exist_ok=True)

            filepath = f"{dst_dir}/{filename}"
            self.run(f"curl -LO {url} -o {filepath}")

            return filepath



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
            conn = fabric.Connection( self.remote,
                                      user=self.user,
                                      port=self.port,
                                      connect_kwargs={"password": self.password} )
        
        elif self.auth_type == RemoteShell_AuthType.PRIVATE_KEY:
            conn = fabric.Connection( self.remote,
                                      user=self.user,
                                      port=self.port,
                                      connect_kwargs={"key_filename": self.priv_key_path} )
        
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



    def __init__( self,
                  remote: str,
                  user: str,
                  port: int = 22,
                  password: Optional[str] = None,
                  priv_key: Optional[str] = None ):

        self.local_shell = LocalShell()

        self.remote = remote
        self.user = user
        self.password = password
        self.priv_key_path = priv_key
        self.port = port

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

    def _put_directory(self, local_dir: str, remote_dir: Optional[str] = None):
        ignore_dirs = [
            ".git",
            "test_environments",
            "__pycache__"
        ]

        if remote_dir is not None:
            # Create the remote directory if it doesn't exist
            self._conn.run(f'mkdir -p {remote_dir}')
        else:
            top_dir = os.path.basename(local_dir)
            self._conn.run(f'mkdir -p {top_dir}')

            remote_dir = top_dir

        # Walk through the directory tree
        for dirpath, dirnames, filenames in os.walk(local_dir):
            # Modify dirnames in-place to skip ignored directories
            dirnames[:] = [d for d in dirnames if d not in ignore_dirs]
            
            # Compute remote directory path
            relative_path   = os.path.relpath(dirpath, local_dir)
            remote_dir_path = os.path.join(remote_dir, relative_path)

            self._conn.run(f'mkdir -p {remote_dir_path}')

            # Upload each file in this directory
            for filename in filenames:
                local_file = os.path.join(dirpath, filename)
                remote_file_path = os.path.join(remote_dir_path, filename)

                self._conn.put(local_file, remote_file_path)

        # if remote_dir is not None:
        #     # Create the remote directory if it doesn't exist
        #     self._conn.run(f'mkdir -p {remote_dir}')
        # else:
        #     top_dir = os.path.basename(local_dir)
        #     self._conn.run(f'mkdir -p {top_dir}')

        #     remote_dir = top_dir
        
        # for root, dirs, files in os.walk(local_dir):
        #     # Determine the path on the remote server
        #     relative_path = os.path.relpath(root, local_dir)
        #     remote_dir_path = os.path.join(remote_dir, relative_path)
            
        #     # Create directories
        #     for dir_name in dirs:
        #         if dir_name in ignore_list:
        #             dirs.remove(dir_name)
        #             continue

        #         remote_subdir = os.path.join(remote_dir_path, dir_name)
        #         self._conn.run(f'mkdir -p {remote_subdir}')
            
        #     # Upload files
        #     for file in files:
        #         local_file       = os.path.join(root, file)
        #         remote_file_path = os.path.join(remote_dir_path, file)

        #         self._conn.put(local_file, remote_file_path)
        #         print("Uploaded", local_file, "to", remote_file_path)



    def run(self, cmd_str: str):
        self._run(self._conn, cmd_str)


    def put(self, local_path: str, remote_path: Optional[str] = None):
        if os.path.isdir(local_path):
            self._put_directory(local_path, remote_path)
        else:
            self._conn.put(local=local_path, remote=remote_path)

        # self._conn.put(local=local_path, remote=remote_path)


    def install(self, url: str, dst_dir: Optional[str] = None) -> str:
        """
        curl the file locally then sftp it
        to the remote machine
        """
        with TemporaryDirectory() as tmp_dir:
            # Download file locally
            filepath = self.local_shell.install(url, tmp_dir)

            if dst_dir is not None:
                self._conn.run(f"mkdir -p {dst_dir}")

            self.put(filepath, dst_dir)

            # Delete local file
            os.remove(filepath)

