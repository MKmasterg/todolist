from interface.cli import handle_command, print_help
from interface.arg_parser import parse_args


def main():
    print("Welcome to the CLI application.")
    print_help()
    print("> ", end=" ")
    user_input = input().strip()
    while user_input.lower() != "exit":
        parsed_input = parse_args(user_input)
        if parsed_input:
            handle_command(parsed_input[0].lower(), parsed_input[1:])
        print("> ", end=" ")
        user_input = input().strip()


if __name__ == "__main__":
    main()
