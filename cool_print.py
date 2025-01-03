import sys
import time
import random
import heapq
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Optional
from colorama import init, Fore, Style
from typing import List

# Initialize colorama for cross-platform colored output
init(autoreset=True)

@dataclass(order=True)
class Event:
    scheduled_time: float
    priority: int = field(init=False, default=0)
    action: Callable = field(compare=False, default=None)

def generate_half_width_katakana() -> str:
    """
    Generates a random half-width Katakana character.
    Unicode Range: U+FF65 to U+FF9F
    """
    return chr(random.randint(0xFF65, 0xFF9F))

def generate_bell_curve_delay(lower: float, upper: float, z: int = 2, max_attempts: int = 1000) -> float:
    """
    Generates a delay following a Gaussian distribution, automatically calculating mu and sigma
    based on the provided lower and upper bounds to ensure most delays fall within [lower, upper].

    Args:
        lower (float): Minimum delay in seconds.
        upper (float): Maximum delay in seconds.
        z (int, optional): Number of standard deviations from the mean to set the bounds. Defaults to 2.
        max_attempts (int, optional): Maximum number of attempts to find a valid delay. Defaults to 1000.

    Returns:
        float: A delay value within [lower, upper].

    Raises:
        ValueError: If lower is not less than upper.
    """
    if lower >= upper:
        raise ValueError("Lower bound must be less than upper bound.")
    if z <= 0:
        raise ValueError("z must be a positive integer.")

    mu = (lower + upper) / 2
    sigma = (upper - lower) / (2 * z)

    for _ in range(max_attempts):
        delay = random.gauss(mu, sigma)
        if lower <= delay <= upper:
            return delay
    # If a valid delay isn't found after max_attempts, return the mean and issue a warning
    print(f"Warning: Could not find a delay within bounds after {max_attempts} attempts. Returning mu={mu}.")
    return mu


def linear_speed_up_delay_provider(low, up, line_length, nth_character: int) -> List[float]:
    """
    Provides delay values for cool_print function with a slowing effect.
    [lower_delay, upper_delay, placeholder_lower_delay, placeholder_upper_delay]
    """
    fraction_remains_l = low / 20
    fraction_remains_u = up / 20
    lower_delay = low - ((low - fraction_remains_l) * (nth_character / line_length))
    upper_delay = up - ((up - fraction_remains_u) * (nth_character / line_length))
    pl = low * 0.1
    pu = up * 0.1
    fraction_remains_l = pl / 20
    fraction_remains_u = pu / 20
    placeholder_lower_delay = pl - ((pl - fraction_remains_l) * (nth_character / line_length))
    placeholder_upper_delay = pu - ((pu - fraction_remains_u) * (nth_character / line_length))
    return [lower_delay, upper_delay, placeholder_lower_delay, placeholder_upper_delay]

def fixed_time_linear_speed_up_provider(fixed_time: float, line_length: int, nth_character: int) -> List[float]:
    """
    It takes fixed_time for the full line to appear. At the start it's slow (longer delays)
    and then it speeds up (shorter delays). This function returns a list of four values:
    [lower_delay, upper_delay, placeholder_lower_delay, placeholder_upper_delay].

    The approach here is to model the time between characters as an arithmetic sequence
    that sums to fixed_time over the entire line_length. The first delay is largest,
    the last delay is smallest.
    """
    # ----------------------------------------------------
    # 1) We want an arithmetic sequence of delays: d_1, d_2, ..., d_line_length
    # 2) Sum(d_1 to d_line_length) = fixed_time
    # 3) The first delay (d_1) is the largest and the last delay (d_line_length) is the smallest.
    #
    # Let ratio = how many times bigger d_1 is compared to d_line_length (just a design choice).
    # Then:
    #     d_1 = ratio * d_line_length
    #     sum = line_length * (d_1 + d_line_length) / 2 = fixed_time
    #
    # From sum, we solve for d_line_length:
    #     line_length * (ratio * d_line_length + d_line_length) / 2 = fixed_time
    #     line_length * (ratio + 1) * d_line_length / 2 = fixed_time
    #     d_line_length = (2 * fixed_time) / (line_length * (ratio + 1))
    # and hence
    #     d_1 = ratio * d_line_length
    #
    # Once d_1 and d_line_length are known, the nth delay is found by:
    #     d_n = d_1 + (n - 1) * (d_line_length - d_1) / (line_length - 1)
    #
    # ----------------------------------------------------

    # You can tweak this ratio to control how “slow” the start is compared to the end
    ratio = 3.0  # Means the first delay is 3x the last delay

    # Compute d_line_length (smallest delay) and d_1 (largest delay)
    d_line_length = (2.0 * fixed_time) / (line_length * (ratio + 1))
    d_1 = ratio * d_line_length

    # If line_length == 1, then nth_character == 1, we only have one delay
    if line_length == 1:
        d_n = fixed_time
    else:
        # Arithmetic progression step
        step = (d_line_length - d_1) / (line_length - 1)
        # Delay for the nth_character (1-indexed)
        d_n = d_1 + (nth_character - 1) * step

    # ----------------------------------------------------
    # Return four delay values. 
    #
    # For example:
    #   - lower_delay and upper_delay might be a “range” for normal characters
    #   - placeholder_lower_delay and placeholder_upper_delay might be a “range” 
    #     if you’re typing placeholders differently (faster, for example).
    # 
    # Adjust these multipliers as needed. 
    # ----------------------------------------------------
    lower_delay = 0.90 * d_n
    upper_delay = 1.10 * d_n
    placeholder_lower_delay = 0.40 * d_n
    placeholder_upper_delay = 0.60 * d_n

    return [lower_delay, upper_delay, placeholder_lower_delay, placeholder_upper_delay]

def default_delay_provider(line_length, nth_character:int) -> List[float]:
    """
    Provides default delay values for cool_print function.
    [lower_delay, upper_delay, placeholder_lower_delay, placeholder_upper_delay]
    """
    return [0.1, 0.3, 0.01, 0.02]

def cool_print(
    *args,
    sep: str = ' ',
    end: str = '\n',
    file: Any = sys.stdout,
    flush: bool = False,
    delay_provider: Callable[[int, int], List[float]] = default_delay_provider,
    z: int = 2,
    color_map: Optional[Dict[int, str]] = None,
    hide_cursor: bool = True  # New parameter to control cursor visibility
) -> None:
    """
    A custom print function that mimics Python's built-in print but with a dynamic typing effect.
    It handles multiple arguments, separators, and endings while displaying characters with random placeholders
    and supports custom colors for specific characters.

    Args:
        *args: Variable length argument list to be printed.
        sep (str, optional): String inserted between values, default a space.
        end (str, optional): String appended after the last value, default a newline.
        file (object, optional): A file-like object (stream); defaults to the current sys.stdout.
        flush (bool, optional): Whether to forcibly flush the stream.
        lower_delay (float, optional): Minimum delay in seconds for character replacement.
        upper_delay (float, optional): Maximum delay in seconds for character replacement.
        z (int, optional): Number of standard deviations for delay distribution. Defaults to 2.
        color_map (Dict[int, str], optional): A dictionary mapping character indices to colorama color codes.
            Example: {0: Fore.RED, 7: Fore.BLUE}
    """
    # ANSI escape codes for hiding and showing the cursor
    HIDE_CURSOR = '\033[?25l'
    SHOW_CURSOR = '\033[?25h'

    # Join the arguments using the specified separator
    text = sep.join(map(str, args))

    if not text or text == "":
        print("")
        return
    
    # Initialize the current_chars list with 'empty' status
    current_chars = [{'char': ' ', 'status': 'empty'} for _ in text]
    
    # Initialize the priority queue
    event_queue = []
    
    # Initialize start time
    start_time = time.time()
    
    # Concurrency control
    max_concurrent = 5
    active_replacements = 0
    replace_queue = []
    
    # Function to update the display
    def update_display():
        """
        Rewrites the entire row based on the current_chars list, applying custom colors if specified.
        """
        # Move cursor to the beginning of the line
        file.write('\r')
        # Reconstruct the display string with appropriate styling
        display_str = ''
        for idx, char_info in enumerate(current_chars):
            if char_info['status'] == 'placeholder':
                # Apply custom color if specified
                color = color_map.get(idx, Fore.GREEN) if color_map else Fore.GREEN
                display_str += f"{color}{Style.DIM}{char_info['char']}"
            elif char_info['status'] == 'correct':
                # Apply custom color if specified
                color = color_map.get(idx, Fore.GREEN) if color_map else Fore.GREEN
                display_str += f"{color}{Style.NORMAL}{char_info['char']}"
            else:
                display_str += ' '  # Empty space for unprocessed characters
        # Write the reconstructed string
        file.write(display_str)
        file.flush()
    
    # Replacement function
    def replace_char(index: int, correct_char: str):
        nonlocal active_replacements
        # Replace with correct character
        current_chars[index]['char'] = correct_char
        current_chars[index]['status'] = 'correct'
        update_display()
        # Decrement active replacements
        active_replacements -= 1
        # If there are pending replacements in the queue, schedule the next one
        if replace_queue:
            next_event = replace_queue.pop(0)
            heapq.heappush(event_queue, next_event)
    
    # Function to add placeholder and schedule replacement
    def add_placeholder(index: int, correct_char: str):
        nonlocal active_replacements
        # Add placeholder
        placeholder_char = generate_half_width_katakana()
        current_chars[index]['char'] = placeholder_char
        current_chars[index]['status'] = 'placeholder'
        update_display()
        
        # Schedule replacement
        lower_delay, upper_delay, _, _ = delay_provider(len(current_chars), index)
        delay = generate_bell_curve_delay(lower_delay, upper_delay, z)
        replacement_time = time.time() + delay
        def action():
            replace_char(index, correct_char)
        
        event = Event(scheduled_time=replacement_time, action=action)
        heapq.heappush(event_queue, event)
    
    # Schedule placeholder additions sequentially with a small delay between them
    for index, char in enumerate(text):
        _, _, placeholder_lower_delay, placeholder_upper_delay = delay_provider(len(current_chars), index)
        placeholder_delay = generate_bell_curve_delay(placeholder_lower_delay, placeholder_upper_delay, z)
        scheduled_time = start_time + index * placeholder_delay
        def action(index=index, char=char):
            nonlocal active_replacements
            # Add placeholder
            add_placeholder(index, char)
            # Increment active replacements
            active_replacements += 1
            # If over concurrency limit, move the next replacement event to replace_queue
            if active_replacements > max_concurrent:
                if event_queue:
                    event = heapq.heappop(event_queue)
                    replace_queue.append(event)
                    active_replacements -= 1
        event = Event(scheduled_time=scheduled_time, action=action)
        heapq.heappush(event_queue, event)
    
    # Main loop to process events
    while event_queue or replace_queue:
        if hide_cursor:
            file.write(HIDE_CURSOR)
            file.flush()
        current_time = time.time()
        while event_queue and event_queue[0].scheduled_time <= current_time:
            event = heapq.heappop(event_queue)
            event.action()
        # Sleep for a short duration to prevent high CPU usage
        time.sleep(0.01)  # 10ms
    
    if hide_cursor:
        file.write(SHOW_CURSOR)
        file.flush()
    
    # After all replacements, append the end string
    file.write(end)
    if flush:
        file.flush()

if __name__ == "__main__":
    # Example 1: Simple message without custom colors
    cool_print("Hello, World!")

    # Example 2: Multiple arguments with custom separator
    cool_print("The", "quick", "brown", "fox", sep="-")

    # Example 3: Using end parameter to avoid newline
    cool_print("This will ", end='')
    cool_print("continue on the same line.")

    # Example 4: Complex sentence with multiple replacements
    cool_print("Cool", "print", "is", "fun!", sep=' ', end='\n')

    # Example 5: Custom colors for specific characters
    # Color 'H' in red (index 0), 'W' in blue (index 7)
    color_map = {0: Fore.RED, 7: Fore.BLUE}
    cool_print("Hello, World!", color_map=color_map)