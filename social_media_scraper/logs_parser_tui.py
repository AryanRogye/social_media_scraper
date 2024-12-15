import curses
import os

def logsT(stdscr):
    """
    A TUI for selecting a username from the logs folder.
    Displays below existing terminal content without clearing it.
    """
    # Disable cursor
    curses.curs_set(0)

    # Path to the logs folder
    logs_folder = "./logs"

    # Get the list of folders inside the logs directory
    folders = [f for f in os.listdir(logs_folder) if os.path.isdir(os.path.join(logs_folder, f))]
    if not folders:
        stdscr.addstr("\nNo saved usernames found in logs directory. Press any key to exit.")
        stdscr.getch()
        return None

    current_selection = 0

    # Get terminal dimensions
    max_y, max_x = stdscr.getmaxyx()
    y, x = stdscr.getyx()

    # Calculate the starting position for the header
    header_y = max(0, y - 1)  # Ensure it doesn't go negative

    while True:
        # Display a header message above the options
        stdscr.addstr(header_y, 0, "Pick a username (q to quit):", curses.A_BOLD)

        # Display folders below the message
        for idx, folder in enumerate(folders):
            line_y = header_y + 1 + idx  # Start rendering below the header
            if line_y >= max_y - 1:  # Avoid writing past the terminal height
                break
            if idx == current_selection:
                stdscr.addstr(line_y, 0, f"> {folder}", curses.A_REVERSE)  # Highlight selected
            else:
                stdscr.addstr(line_y, 0, f"  {folder}")

        stdscr.refresh()

        # Get user input
        key = stdscr.getch()

        # Navigate with j/k or arrow keys
        if key in (curses.KEY_UP, ord('k')):  # Up
            current_selection = (current_selection - 1) % len(folders)
        elif key in (curses.KEY_DOWN, ord('j')):  # Down
            current_selection = (current_selection + 1) % len(folders)
        elif key in (curses.KEY_ENTER, 10, 13):  # Enter
            return folders[current_selection]
        elif key == ord('q'):  # Quit with 'q'
            exit(1)
