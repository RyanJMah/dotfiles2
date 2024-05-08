import click

from src.common.main_installation import install_all

@click.command()
@click.option( "--os", "os_type", required=True, type=click.Choice(['linux', 'macos']), help="Operating system" )
@click.option( "--remote", default=None, type=str, help="Remote hostname or IP address" )
@click.option( "--user", default=None, type=str, help="Remote username" )
@click.option( "--password", default=None, type=str, help="Remote password" )
@click.option( "--priv-key", default=None, type=str, help="Remote ssh private key" )
def main(os_type, remote, user, password, priv_key):
    print(f"OS Type: {os_type}...")

    assert( os_type in ["linux", "macos"] )

    install_all(os_type, remote, user, password, priv_key)

if __name__ == '__main__':
    main()
