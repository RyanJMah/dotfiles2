import click

@click.command()
@click.option( "--os", "os_type", required=True, type=click.Choice(['linux', 'macos']) )
def main(os_type):
    print(f"OS Type: {os_type}...")

    if os_type == 'linux':
        from src.linux.install_script import install_all

    elif os_type == 'macos':
        from src.macos.install_script import install_all
    
    else:
        raise ValueError("Invalid OS type")

    install_all()

if __name__ == '__main__':
    main()
