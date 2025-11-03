"""Terrain generation functions using quantum states."""
from math import sin, cos, pi
from quantum_state import QuantumState


def quantum_terrain(tile_x, tile_y):
    """Generate terrain using quantum states"""
    q = QuantumState(tile_x, tile_y)

    # Step 1: Create superposition
    q.hadamard()

    # Step 2: Introduce coordinate-dependent rotation
    theta = (sin(tile_x * 0.15) + cos(tile_y * 0.13)) * pi / 2
    q.ry(theta)

    # Step 3: Local interference
    phi = ((tile_x * 0.23 + tile_y * 0.37) % (2 * pi)) * 0.5
    q.phase_shift(phi)

    # Step 4: Another layer of Y-rotation for pattern complexity
    q.ry((tile_x * tile_y * 0.002) % (pi / 2))

    # Step 5: Measurement
    density = q.measure()

    # Optional: smooth second state for variation
    q2 = QuantumState(tile_y, tile_x)
    q2.hadamard()
    q2.ry(sin(tile_y * 0.21) * pi / 3)
    variation = q2.measure()

    combined = (density + 0.6 * variation) / 1.6

    if combined < 0.75:
        return None
    elif combined < 0.78:
        return 'tree_thin_fall'
    elif combined < 0.80:
        return 'tree_fat_fall'
    elif combined < 0.82:
        return 'tree_oak_fall'
    elif combined < 0.85:
        return 'stone_large'
    elif combined < 0.87:
        return 'log'
    else:
        return 'stone_tall' if (tile_x + tile_y) % 3 == 0 else 'bush_small'


def quantum_terrain_phase(tile_x, tile_y):
    """Generate terrain using standard quantum phase logic."""
    q = QuantumState(tile_x, tile_y)
    q.hadamard()
    q.rotate(tile_x * 0.1)
    q.hadamard()
    density = q.measure()
    return terrain_type_from_density(density)


def quantum_terrain_ry(tile_x, tile_y):
    """Generate terrain using an RY quantum gate instead of rotation."""
    q = QuantumState(tile_x, tile_y)
    q.hadamard()
    q.ry(tile_x * 0.3 + tile_y * 0.2)
    q.hadamard()
    q.ry(tile_y * 0.15)
    density = q.measure()
    return terrain_type_from_density(density)


def hybrid_terrain(tile_x, tile_y, wave_mode):
    """Mix terrain types between phase-based and RY-based depending on state."""
    if not wave_mode:
        if (tile_x + tile_y) % 7 < 5:
            return quantum_terrain_phase(tile_x, tile_y)
        else:
            return quantum_terrain_ry(tile_x, tile_y)
    else:
        if (tile_x * tile_y) % 5 < 3:
            return quantum_terrain_ry(tile_x, tile_y)
        else:
            return quantum_terrain_phase(tile_x, tile_y)


def terrain_type_from_density(d):
    """Convert density value to terrain type."""
    if d < 0.35:
        return None
    elif d < 0.45:
        return 'tree_thin'
    elif d < 0.60:
        return 'tree_oak_fall'
    elif d < 0.65:
        return 'tree_fat_fall'
    elif d < 0.70:
        return 'stone_large'
    elif d < 0.75:
        return 'stone_tall'
    elif d < 0.80:
        return 'log'
    else:
        return 'bush_small'