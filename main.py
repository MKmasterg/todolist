import readline
from interface.cli import handle_command, print_help
from interface.arg_parser import parse_args
from data.database import SessionLocal


def main():
    # Configure readline for command history
    readline.parse_and_bind('tab: complete')

    print("Welcome to the CLI application.")
    print_help()
    
    # Create a database session for the CLI
    db = SessionLocal()
    try:
        print("> ", end=" ")
        user_input = input().strip()
        while user_input.lower() != "exit":
            parsed_input = parse_args(user_input)
            if parsed_input:
                handle_command(db, parsed_input[0].lower(), parsed_input[1:])
            print("> ", end=" ")
            user_input = input().strip()
    finally:
        db.close()


if __name__ == "__main__":
    main()
