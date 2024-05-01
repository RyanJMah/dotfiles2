import click

@click.command()
@click.option( "--os", "os_type", required=True, type=click.Choice(['linux', 'macos']) )
def main(os_type):
    pass

if __name__ == '__main__':
    main()
