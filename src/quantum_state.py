"""Quantum state simulation for procedural terrain generation."""
from math import sin, cos, pi


class QuantumState:
    """
    Minimal quantum-inspired state for procedural terrain.
    Simulates a 1-qubit system where the phase encodes variation.
    """

    def __init__(self, x: float, y: float):
        # Initialize phase based on world coordinates
        self.phase = (x * 0.1234 + y * 0.4321 + sin(x * 0.1) * cos(y * 0.1)) % (2 * pi)

    def hadamard(self):
        """
        Simulates a Hadamard gate — creates superposition by mixing base state.
        This adds variability to the phase space.
        """
        self.phase = (self.phase + pi / 4 + sin(self.phase)) % (2 * pi)

    def rotate(self, angle: float):
        """
        Rotate phase (Z-axis rotation) — equivalent to an RZ gate.
        Only affects the *phase*, not amplitude.
        """
        self.phase = (self.phase + angle) % (2 * pi)

    def ry(self, theta: float):
        """
        Rotate around Y-axis — modifies both phase and implied probability amplitude.
        Produces stronger variations than rotate().
        """
        delta = sin(theta) * cos(self.phase)
        self.phase = (self.phase + delta * pi) % (2 * pi)

    def phase_shift(self, phi: float):
        """
        Apply a fixed phase offset — useful for biasing certain regions.
        """
        self.phase = (self.phase + phi) % (2 * pi)

    def measure(self) -> float:
        """
        Return a pseudo 'probability' (0–1) derived from the phase.
        This determines how 'dense' or 'active' a terrain tile is.
        """
        return (cos(self.phase) + 1) / 2