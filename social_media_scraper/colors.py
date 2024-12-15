import time
import sys
import threading
import shutil
import curses
import os

def detect_colors():
    try:
        curses.setupterm()
        return curses.tigetnum("colors")
    except Exception:
        return 8  # Default to 8 colors

class ColorText:
    """
    A utility class to print colorful and styled text in the terminal.
    Supports multiple colors, underlining, bold text, and loading animations.
    """
    def __init__(self):
        self.COLORS = self.get_colors()

    def get_colors(self):
        """
        Dynamically fetch terminal-supported colors.
        """
        color_support = detect_colors()
        colorterm = os.getenv("COLORTERM")
        if color_support >= 256:
            return {
                "black": "\033[38;5;0m",
                "grey": "\033[38;5;245m",
                "dark_grey": "\033[38;5;240m",  # Dark Grey
                "red": "\033[38;5;196m",
                "dark_red": "\033[38;5;124m",  # Dark Red
                "light_red": "\033[38;5;203m",  # Light Red in 256-color palette
                "orange": "\033[38;5;214m",  # Orange in 256-color palette
                "green": "\033[38;5;46m",
                "yellow": "\033[38;5;226m",
                "blue": "\033[38;5;21m",
                "blue_1": "\033[38;5;21m",       # Bright Blue
                "blue_2": "\033[38;5;33m",       # Medium Blue
                "blue_3": "\033[38;5;39m",       # Deep Sky Blue
                "blue_4": "\033[38;5;45m",       # Dodger Blue
                "blue_5": "\033[38;5;75m",       # Steel Blue
                "blue_6": "\033[38;5;123m",      # Light Steel Blue
                "blue_7": "\033[38;5;147m",      # Slate Blue
                "magenta": "\033[38;5;201m",
                "cyan": "\033[38;5;51m",
                "cyan_1": "\033[38;5;51m",       # Bright Cyan
                "cyan_2": "\033[38;5;43m",       # Medium Cyan
                "cyan_3": "\033[38;5;50m",       # Deep Cyan
                "cyan_4": "\033[38;5;87m",       # Aqua Marine
                "cyan_5": "\033[38;5;122m",      # Light Cyan
                "cyan_6": "\033[38;5;159m",      # Pale Turquoise
                "cyan_7": "\033[38;5;195m",      # Powder Blue
                "white": "\033[38;5;15m",
            }
        elif colorterm and "truecolor" in colorterm:
            return {
                "black": "\033[38;2;0;0;0m",
                "grey": "\033[38;2;169;169;169m",  # Light Grey
                "dark_grey": "\033[38;2;105;105;105m",  # Dark Grey
                "red": "\033[38;2;255;0;0m",
                "dark_red": "\033[38;2;139;0;0m",  # Dark Red
                "light_red": "\033[38;2;255;102;102m",  # Light Red (RGB: 255, 102, 102)
                "orange": "\033[38;2;255;165;0m",  # Orange (RGB: 255, 165, 0)
                "green": "\033[38;2;0;255;0m",
                "yellow": "\033[38;2;255;255;0m",
                "blue": "\033[38;2;0;0;255m",
                "blue_1": "\033[38;2;0;0;255m",       # Bright Blue (RGB: 0, 0, 255)
                "blue_2": "\033[38;2;30;144;255m",    # Dodger Blue (RGB: 30, 144, 255)
                "blue_3": "\033[38;2;65;105;225m",    # Royal Blue (RGB: 65, 105, 225)
                "blue_4": "\033[38;2;70;130;180m",    # Steel Blue (RGB: 70, 130, 180)
                "blue_5": "\033[38;2;0;191;255m",     # Deep Sky Blue (RGB: 0, 191, 255)
                "blue_6": "\033[38;2;100;149;237m",   # Cornflower Blue (RGB: 100, 149, 237)
                "blue_7": "\033[38;2;135;206;235m",   # Sky Blue (RGB: 135, 206, 235)
                "magenta": "\033[38;2;255;0;255m",
                "cyan": "\033[38;2;0;255;255m",
                "cyan_1": "\033[38;2;0;255;255m",       # Bright Cyan (RGB: 0, 255, 255)
                "cyan_2": "\033[38;2;72;209;204m",      # Medium Turquoise (RGB: 72, 209, 204)
                "cyan_3": "\033[38;2;0;206;209m",       # Dark Turquoise (RGB: 0, 206, 209)
                "cyan_4": "\033[38;2;32;178;170m",      # Light Sea Green (RGB: 32, 178, 170)
                "cyan_5": "\033[38;2;95;158;160m",      # Cadet Blue (RGB: 95, 158, 160)
                "cyan_6": "\033[38;2;175;238;238m",     # Pale Turquoise (RGB: 175, 238, 238)
                "cyan_7": "\033[38;2;224;255;255m",     # Light Cyan (RGB: 224, 255, 255)
                "white": "\033[38;2;255;255;255m",
            }
        else:
            return {
                "black": "\033[30m",
                "grey": "\033[90m",
                "red": "\033[91m",
                "green": "\033[92m",
                "yellow": "\033[93m",
                "blue": "\033[94m",
                "magenta": "\033[95m",
                "cyan": "\033[96m",
                "white": "\033[97m",
            }
    RESET = "\033[0m"
    UNDERLINE = ";4m"
    def printSeparator(self, color="green"):
        # Get terminal size
        terminal_width = shutil.get_terminal_size().columns
        # Create a separator line matching the terminal width
        separator_line = "-" * terminal_width
        self.printColored(separator_line, color=color)
    def loadingWhileScripting(self, func1, func2):
        try:
            func1.start()
            func2.start()

            func1.join()
            func2.join()
        except Exception as e:
            self.printColored(f"Error during threading: {e}", color="red")
    def getThreadForLoading(self, max_val, delay=0.1):
        """
        Creates a thread for the loading animation.

        Args:
            num (int): Number of loading steps.
            delay (float): Delay (in seconds) between each step.
        """
        max_val = int(max_val / delay)
        return threading.Thread(target=self.coolerLoading, args=(max_val,), kwargs={"delay": delay})

    def printColored(self, text, color="white", underline=False):
        """
        Prints the text in the specified color with optional underlining.
        """
        color_code = self.COLORS.get(color.lower(), self.COLORS["white"])
        style = f"{color_code[:-1]}{self.UNDERLINE}" if underline else color_code
        print(f"{style}{text}{self.RESET}")


    def coolerLoading(self, max_steps, delay=0.1):
        """
        Displays a cool loading bar animation with progress and a spinner,
        alternating between red and white colors.
        
        Args:
            max_steps (int): Total steps in the loading animation.
            delay (float): Time delay (in seconds) between updates.
        """
        try:
            spinner = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"  # Braille spinner
            bar_length = 30  # Total length of the loading bar

            # Dynamically retrieve available colors for the animation
            available_colors = [
                self.COLORS.get("cyan", ""),
                self.COLORS.get("cyan_1", ""),
                self.COLORS.get("cyan_2", ""),
                self.COLORS.get("cyan_3", ""),
                self.COLORS.get("cyan_4", ""),
                self.COLORS.get("cyan_5", ""),
                self.COLORS.get("cyan_6", ""),
                self.COLORS.get("cyan_7", ""),
                self.COLORS.get("blue", ""),
                self.COLORS.get("blue_1", ""),
                self.COLORS.get("blue_2", ""),
                self.COLORS.get("blue_3", ""),
                self.COLORS.get("blue_4", ""),
                self.COLORS.get("blue_5", ""),
                self.COLORS.get("blue_6", ""),
                self.COLORS.get("blue_7", ""),
            ]
            
            # Remove any empty strings in case a color isn't found in the dictionary
            colors = [color for color in available_colors if color]
            
            if not colors:  # Fallback to white if no colors are defined
                colors = [self.COLORS.get("white", "\033[97m")]
            
            for step in range(max_steps + 1):
                # Calculate progress percentage
                progress = step / max_steps
                filled_length = int(bar_length * progress)
            
                # Generate the loading bar
                bar = f"{'█' * filled_length}{'-' * (bar_length - filled_length)}"
            
                # Cycle through available colors
                color_code = colors[step % len(colors)]  # Alternate between colors
                spinner_char = spinner[step % len(spinner)]
            
                # Display the loading animation with progress percentage
                sys.stdout.write(
                    f"\r{color_code}[{bar}] {spinner_char} {int(progress * 100)}%{self.RESET} Loading..."
                )
                sys.stdout.flush()
                time.sleep(delay)
            
            print()  # Print a newline after the animation ends
        except Exception as e:
            self.printColored(f"There was an error with the loading bar: {e}", color="red")

    def coolLoading(self, num, delay=0.5, char="█", max_bar_length=None, cooler=False):
        if cooler:
            self.coolerLoading(num, delay=delay)
            return
        """
        Displays a growing loading bar with cycling colors.
    
        Args:
            num (int): Number of steps in the loading animation.
            delay (float): Time delay (in seconds) between updates.
            char (str): Character to use for the loading bar.
            max_bar_length (int, optional): Maximum length of the loading bar. 
                                            If None, bar grows indefinitely.
        """
        colors = [
            "\033[91;4m",  # Red and underlined
            "\033[92;4m",  # Green and underlined
            "\033[93;4m",  # Yellow and underlined
            "\033[94;4m",  # Blue and underlined
            "\033[95;4m",  # Magenta and underlined
            "\033[96;4m",  # Cyan and underlined
        ]
    
        bar = ""  # Initialize an empty bar
    
        for i in range(num):
            # Cycle through colors
            color = colors[i % len(colors)]
    
            # Add the `char` to the bar
            bar += char
    
            # If max_bar_length is set, trim the bar length
            if max_bar_length and len(bar) > max_bar_length:
                bar = bar[:max_bar_length]
    
            # Print the bar (doesn't overwrite previous lines)
            sys.stdout.write(f"{color}{bar}{self.RESET}\n")
            sys.stdout.flush()
    
            # Add a short delay
            time.sleep(delay)
    
        # Final print to indicate the end
        print(f"{colors[-1]}Loading complete!{self.RESET}")
