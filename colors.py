import time
import sys

class ColorText:
    """
    A utility class to print colorful and styled text in the terminal.
    Supports multiple colors, underlining, bold text, and loading animations.
    """

    # ANSI color codes
    COLORS = {
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

    def printColored(self, text, color="white", underline=False):
        """
        Prints the text in the specified color with optional underlining.
        """
        color_code = self.COLORS.get(color.lower(), self.COLORS["white"])
        style = f"{color_code[:-1]}{self.UNDERLINE}" if underline else color_code
        print(f"{style}{text}{self.RESET}")

    # Cool Loading with Optional Spinner Animation
    def coolerLoading(self, num, delay=0.1):
        """
        Displays a spinner animation using Braille characters.
    
        Args:
            num (int): Number of steps in the spinner animation.
            delay (float): Time delay (in seconds) between updates.
        """
        spinner = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"  # Braille spinner
        for i in range(num):
            char = spinner[i % len(spinner)]
            sys.stdout.write(f"\r\033[92m{char}\033[0m")  # Green spinner character
            sys.stdout.flush()
            time.sleep(delay)
        print()  # Print a newline after the animation ends

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
