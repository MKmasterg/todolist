import readline
import asyncio
from interface.cli.cli import handle_command, print_help, print_error
from interface.cli import parse_args
from data.database import AsyncSessionLocal


async def async_main():
    # Configure readline for command history
    readline.parse_and_bind('tab: complete')

    print("Welcome to the CLI application.\nWarning: CLI is deprecated and will be removed in future versions.\nPlease migrate to the new API.")
    print_help()

    while True:
        # Use thread to read blocking input without blocking the event loop
        user_input = await asyncio.to_thread(input, "> ")
        user_input = user_input.strip()
        if user_input.lower() == "exit":
            break
        parsed_input = parse_args(user_input)
        if not parsed_input:
            continue

        # Create a fresh AsyncSession per command to avoid cross-loop/session issues
        async with AsyncSessionLocal() as db:
            try:
                await handle_command(db, parsed_input[0].lower(), parsed_input[1:])
            except Exception as e:
                print_error(f"Error executing command: {str(e)}")


if __name__ == "__main__":
    asyncio.run(async_main())
