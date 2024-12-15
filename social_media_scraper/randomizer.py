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
    def _randomize_with_entropy(base_range, transform_mod, max_bias):
        base_delay = Randomizer.randomize(lower=0, higher=base_range)
        mix_factor = Randomizer.randomize(lower=1, higher=10)
        transformed_delay = (base_delay * mix_factor) % transform_mod
        shift_seed = Randomizer.randomize(lower=0, higher=255)
        transformed_delay = (transformed_delay ^ shift_seed) % transform_mod
        bias = Randomizer.randomize(lower=-max_bias, higher=max_bias)
        return max(0, min(base_range, transformed_delay + bias))

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
    def randomize_15sec():
        return Randomizer._randomize_with_entropy(15, 16, 5)
    @staticmethod
    def randomize_30sec():
        return Randomizer._randomize_with_entropy(30, 31, 5) 
    @staticmethod
    def randomize_1minutes():
        return Randomizer._randomize_with_entropy(60, 61, 5)
    
    @staticmethod
    def randomize_3minutes():
        return Randomizer._randomize_with_entropy(180, 181, 5)
