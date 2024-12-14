import random
import time
import os
import hashlib
from datetime import datetime

class Randomizer:
    oldRand = None  # Class-level variable to track the previous random value

    @staticmethod
    def _get_entropy():
        """Generates high-entropy data from various sources."""
        # Combine system time, process ID, and random bits
        entropy = (
            f"{time.time_ns()}"  # Nanosecond precision time
            f"{os.getpid()}"    # Process ID
            f"{random.getrandbits(128)}"  # Large random bits
            f"{hashlib.sha256(str(datetime.now()).encode()).hexdigest()}"  # Timestamp hash
        )
        # Hash the combined entropy for even distribution
        return hashlib.sha256(entropy.encode()).hexdigest()

    @staticmethod
    def _mix_entropy(seed_value):
        """Mix additional entropy into a seed value."""
        entropy = Randomizer._get_entropy()
        combined = f"{seed_value}{entropy}"
        return int(hashlib.sha256(combined.encode()).hexdigest(), 16)

    @staticmethod
    def randomize(func=None, lower=0, higher=100):
        """
        Generate a highly unpredictable random number between `lower` and `higher`.
        Applies a transformation function `func` if provided.

        Args:
            func (callable, optional): A function to transform the random value.
            lower (int): The lower bound for random number generation.
            higher (int): The upper bound for random number generation.

        Returns:
            int or any: A random value, potentially transformed by `func`.
        """
        # Get high-entropy seed
        seed_value = random.random()  # Base randomness
        mixed_seed = Randomizer._mix_entropy(seed_value)

        # Create a random value using the high-entropy seed
        random.seed(mixed_seed)  # Temporarily seed the random generator
        rand_value = random.randint(lower, higher)

        # Apply the transformation function if provided
        if func:
            rand_value = func(rand_value)

        # Store the value for additional entropy in subsequent calls
        Randomizer.oldRand = rand_value
        return rand_value

    @staticmethod
    def randomize_3minutes():
        # Step 1: Get a base random delay between 0 and 180 seconds
        base_delay = Randomizer.randomize(lower=0, higher=180)
        
        # Step 2: Introduce a mix factor (small random integer)
        mix_factor = Randomizer.randomize(lower=1, higher=10)
        
        # Multiply and mod by 181 to ensure we remain in the 0–180 range
        transformed_delay = (base_delay * mix_factor) % 181
        
        # Step 3: Get another random value to use in a bitwise operation
        shift_seed = Randomizer.randomize(lower=0, higher=255)  # 0–255 for a full byte of randomness
        
        # XOR the transformed delay with shift_seed, then mod again to stay in range
        transformed_delay = (transformed_delay ^ shift_seed) % 181
        
        # Step 4: Add a final layer: another random call to slightly bias the result
        bias = Randomizer.randomize(lower=-5, higher=5)
        transformed_delay = max(0, min(180, transformed_delay + bias)) 
        return transformed_delay
