from vira.cli.handlers import ViraApplication
from vira.utils.arguments import parse_arguments


def main():
    """CLI entry point"""
    app = ViraApplication()
    args = parse_arguments()
    app.run(args)


if __name__ == "__main__":
    main()