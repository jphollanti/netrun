import sys
import time
import random
import heapq
from dataclasses import dataclass, field
from typing import Any
from colorama import init, Fore, Style

# Initialize colorama for colored output
init(autoreset=True)

@dataclass(order=True)
class Event:
    scheduled_time: float
    priority: int = field(init=False, default=0)
    action: Any = field(compare=False, default=None)

def generate_half_width_katakana():
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
    
    for attempt in range(max_attempts):
        delay = random.gauss(mu, sigma)
        if lower <= delay <= upper:
            return delay
    # If a valid delay isn't found after max_attempts, return the mean and issue a warning
    print(f"Warning: Could not find a delay within bounds after {max_attempts} attempts. Returning mu={mu}.")
    return mu

def cool_print(*args, sep=' ', end='\n', file=sys.stdout, flush=False,
              lower_delay=0.1, upper_delay=0.5, z=2):
    """
    A custom print function that mimics Python's built-in print but with a dynamic typing effect.
    It handles multiple arguments, separators, and endings while displaying characters with random placeholders.
    
    Args:
        *args: Variable length argument list to be printed.
        sep (str, optional): String inserted between values, default a space.
        end (str, optional): String appended after the last value, default a newline.
        file (object, optional): A file-like object (stream); defaults to the current sys.stdout.
        flush (bool, optional): Whether to forcibly flush the stream.
        lower_delay (float, optional): Minimum delay in seconds for character replacement.
        upper_delay (float, optional): Maximum delay in seconds for character replacement.
        z (int, optional): Number of standard deviations for delay distribution. Defaults to 2.
    """
    # Join the arguments using the specified separator
    text = sep.join(map(str, args))
    
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
        Rewrites the entire row based on the current_chars list.
        """
        # Move cursor to the beginning of the line
        file.write('\r')
        # Reconstruct the display string with appropriate styling
        display_str = ''
        for char_info in current_chars:
            if char_info['status'] == 'placeholder':
                display_str += Fore.GREEN + Style.DIM + char_info['char']
            elif char_info['status'] == 'correct':
                display_str += Fore.GREEN + Style.NORMAL + char_info['char']
            else:
                display_str += ' '  # Empty space for unprocessed characters
        # Write the reconstructed string
        file.write(display_str)
        file.flush()
    
    # Replacement function
    def replace_char(index, correct_char):
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
    def add_placeholder(index, correct_char):
        nonlocal active_replacements
        # Add placeholder
        placeholder_char = generate_half_width_katakana()
        current_chars[index]['char'] = placeholder_char
        current_chars[index]['status'] = 'placeholder'
        update_display()
        
        # Schedule replacement
        delay = generate_bell_curve_delay(lower_delay, upper_delay, z)
        replacement_time = time.time() + delay
        def action():
            replace_char(index, correct_char)
        
        event = Event(scheduled_time=replacement_time, action=action)
        heapq.heappush(event_queue, event)
    
    # Schedule placeholder additions sequentially with a small delay between them
    placeholder_delay = 0.05  # 50ms between each placeholder addition
    for index, char in enumerate(text):
        scheduled_time = start_time + index * placeholder_delay
        def action(index=index, char=char):
            nonlocal active_replacements
            # Add placeholder
            add_placeholder(index, char)
            # Increment active replacements
            active_replacements += 1
            # If over concurrency limit, move the replacement event to replace_queue
            if active_replacements > max_concurrent:
                if event_queue:
                    event = heapq.heappop(event_queue)
                    replace_queue.append(event)
                    active_replacements -= 1
        event = Event(scheduled_time=scheduled_time, action=action)
        heapq.heappush(event_queue, event)
    
    # Main loop to process events
    while event_queue or replace_queue:
        current_time = time.time()
        while event_queue and event_queue[0].scheduled_time <= current_time:
            event = heapq.heappop(event_queue)
            event.action()
        # Sleep for a short duration to prevent high CPU usage
        time.sleep(0.01)  # 10ms
    
    # After all replacements, append the end string
    file.write(end)
    if flush:
        file.flush()

# Example Usage
if __name__ == "__main__":
    # Example 1: Simple message
    cool_print("Hello, World!")

    # Example 2: Multiple arguments with custom separator
    cool_print("The", "quick", "brown", "fox", sep="-")

    # Example 3: Using end parameter to avoid newline
    cool_print("This will ", end='')
    cool_print("continue on the same line.")

    # Example 4: Complex sentence with multiple replacements
    cool_print("Cool", "print", "is", "fun!", sep=' ', end='\n')
