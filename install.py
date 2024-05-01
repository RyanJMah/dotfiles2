import click

from src.common.main_installation import install_all

@click.command()
@click.option( "--os", "os_type", required=True, type=click.Choice(['linux', 'macos']) )
def main(os_type):
    print(f"OS Type: {os_type}...")

    assert( os_type in ["linux", "macos"] )

    install_all(os_type)

if __name__ == '__main__':
    main()
