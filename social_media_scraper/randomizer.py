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
