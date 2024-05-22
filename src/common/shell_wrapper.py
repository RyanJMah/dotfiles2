import os
import sys
import fabric
import atexit
import subprocess
from enum import Enum
from typing import Optional
from abc import ABC, abstractmethod
from tempfile import TemporaryDirectory

class Shell(ABC):
    @abstractmethod
    def run(self, cmd_str: str) -> bool:
        """
        Run a shell command
        """
        pass

    @abstractmethod
    def install( self,
                 url: str,
                 dst_dir: Optional[str] = None ) -> str:
        """
        Install a file from a URL

        If dst_dir is None, the file is installed in the current directory

        If dst_dir doesn't exist, it is created
        """
        pass

    @abstractmethod
    def clone_git_repo( self,
                        url: str,
                        dst_dir: Optional[str] = None ):
        """
        Clone a git repository
        """
        pass


    @abstractmethod
    def _check_dependency(self, dependency: str) -> bool:
        """
        Check if a dependency is installed
        """
        pass

    def check_dependency(self, dependency: str) -> bool:
        print(f"checking for {dependency}... ", end="")
        return self._check_dependency(dependency)


    def symlink_dir_files(self, src: str, dst: str):
        """
        Symlinks every file in src to dst, instead of just
        symlinking the directory itself
        """

        cmd = f"""
        for f in "{src}"/*; do
            # Extract the basename of the file (the filename without the path)
            f_name="${{f##*/}}"

            # If the symlink already exists, remove it
            if [ -L "{dst}/$f_name" ]; then
                rm -r "{dst}/$f_name"
            fi
            
            # Create a symbolic link in the dst directory
            ln -sf "$f" "{dst}/$f_name"
        done
        """
        self.run(cmd)


class LocalShell(Shell):
    def run(self, cmd_str: str) -> bool:
        cmd = cmd_str.strip()
        try:
            subprocess.run(cmd, shell=True, text=True, check=True)
            return True
        
        except subprocess.CalledProcessError as e:
            print(f"ERROR: {e}")
            return False

    def install( self,
                 url: str,
                 dst_dir: Optional[str] = None ) -> str:

        filename = url.split("/")[-1]

        if dst_dir is None:
            self.run(f"curl -LO {url}")
            return filename
        
        # dst_dir is specified
        else:
            os.makedirs(dst_dir, exist_ok=True)
            filepath = os.path.join(dst_dir, filename)

            self.run(f"curl -Lo {filepath} {url}")

            return filepath

    def _clone_repo_safe(self, url: str, repo_path: str):
        cmd = f"""
        if [ -d {repo_path} ];
        then
            cd {repo_path}
            git fetch && git reset --hard origin/$(git symbolic-ref --short HEAD)                
        else
            git clone {url} {repo_path}
        fi
        """
        self.run(cmd)

    def clone_git_repo( self,
                        url: str,
                        dst_dir: Optional[str] = None ):

        repo_name = url.split("/")[-1].replace(".git", "")

        if dst_dir is None:
            self._clone_repo_safe(url, repo_name)
            return repo_name
        
        # dst_dir is specified
        else:
            os.makedirs(dst_dir, exist_ok=True)
            repo_path = os.path.join(dst_dir, repo_name)

            self._clone_repo_safe(url, repo_path)
            return repo_path

    def _check_dependency(self, dependency: str) -> bool:
        # return self.run(f"which {dependency}")
        p = subprocess.Popen(["which", dependency], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout, stderr = p.communicate()
        print(stdout.decode(), end="")

        return p.returncode == 0

class RemoteShell_AuthType(Enum):
    PASSWORD = 0
    PRIVATE_KEY = 1

class RemoteShell(Shell):
    def _run(self, conn: fabric.Connection, cmd_str: str) -> bool:
        cmd = cmd_str.strip()

        try:
            result = conn.run(cmd)

            if result.failed:
                print(f"ERROR: {result.stderr}")
                return False
            else:
                return True
        
        except Exception as e:
            print(f"ERROR: {e}")
            return False

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
        """
        NOTE: This function is recursive (with self.put calls)
        """
        if remote_dir is not None:
            # Create the remote directory if it doesn't exist
            self._conn.run(f'mkdir -p {remote_dir}')
        else:
            top_dir = os.path.basename(local_dir)
            self._conn.run(f'mkdir -p {top_dir}')

            remote_dir = top_dir

        for f in os.listdir(local_dir):
            local_file = os.path.join(local_dir, f)
            remote_file_path = os.path.join(remote_dir, f)

            # recursive call
            self.put(local_file, remote_file_path)
            print(f"{local_file} -> {remote_file_path}")


    def put(self, local_path: str, remote_path: Optional[str] = None):
        if os.path.isdir(local_path):
            self._put_directory(local_path, remote_path)
        else:
            self._conn.put(local=local_path, remote=remote_path, preserve_mode=False)


    def run(self, cmd_str: str) -> bool:
        return self._run(self._conn, cmd_str)


    def install( self,
                 url: str,
                 dst_dir: Optional[str] = None ) -> str:
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

    def clone_git_repo( self,
                        url: str,
                        dst_dir: Optional[str] = None ):

        with TemporaryDirectory() as tmp_dir:
            repo_path    = self.local_shell.clone_git_repo(url, tmp_dir)
            repo_tarball = f"{repo_path}.tar.gz"

            repo_name = url.split("/")[-1].replace(".git", "")

            cmd = f"""
            cd {tmp_dir}

            tar -czvf {repo_name}.tar.gz {repo_name}
            """
            self.local_shell.run(cmd)
        
            self.put(repo_tarball, dst_dir)

        # Extract
        tarball_name = repo_tarball.split("/")[-1]        

        cmd = f"""
        cd {dst_dir}
        tar -xzf {tarball_name}
        rm {tarball_name}
        """
        self.run(cmd)

    def _check_dependency(self, dependency: str) -> bool:
        return self.run(f"which {dependency}")

    def get_home(self) -> str:
        result = self._conn.run("echo $HOME")

        return result.stdout.strip()
