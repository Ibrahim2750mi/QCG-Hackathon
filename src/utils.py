"""Utility functions for coordinate conversion and collision detection."""
import math
from constants import TILE_WIDTH, TILE_HEIGHT, CHUNK_SIZE, MASTER_SEED


def iso_to_screen(iso_x, iso_y):
    """Convert isometric grid coordinates to screen coordinates"""
    screen_x = (iso_x - iso_y) * (TILE_WIDTH / 2)
    screen_y = (iso_x + iso_y) * (TILE_HEIGHT / 2)
    return screen_x, screen_y


def screen_to_chunk(screen_x, screen_y):
    """Convert screen coordinates to chunk coordinates"""
    tiles_per_chunk = CHUNK_SIZE
    chunk_x = int(screen_x / (TILE_WIDTH * tiles_per_chunk / 2))
    chunk_y = int(screen_y / (TILE_HEIGHT * tiles_per_chunk / 2))
    return chunk_x, chunk_y


def get_chunk_seed(chunk_x, chunk_y):
    """Generate a unique seed for each chunk using activation function"""
    center_x = chunk_x * CHUNK_SIZE + CHUNK_SIZE // 2
    center_y = chunk_y * CHUNK_SIZE + CHUNK_SIZE // 2

    combined = MASTER_SEED * math.sin(center_x * 0.1) * math.cos(center_y * 0.1)
    combined += (center_x * 73856093) ^ (center_y * 19349663)

    activated_seed = int(abs(combined * 1000) % (2 ** 31 - 1))
    return activated_seed


def get_hitbox_for_element(element):
    """Get custom hitbox for specific elements with directional extensions"""
    hitbox_width = TILE_WIDTH * 0.3
    hitbox_height = TILE_HEIGHT * 0.3

    if 'tree' in element:
        return [
            (-hitbox_width * 0.45, -hitbox_height * 3.0),
            (hitbox_width * 0.45, -hitbox_height * 3.0),
            (hitbox_width * 0.45, hitbox_height * 0.8),
            (-hitbox_width * 0.45, hitbox_height * 0.8)
        ]
    elif element == 'stone_large':
        return [
            (-hitbox_width * 0.8, -hitbox_height * 1.2),
            (hitbox_width * 0.8, -hitbox_height * 1.2),
            (hitbox_width * 0.8, hitbox_height * 0.6),
            (-hitbox_width * 0.8, hitbox_height * 0.6)
        ]
    elif element in ['log', 'log_large']:
        return [
            (-hitbox_width * 0.9, -hitbox_height * 1.0),
            (hitbox_width * 0.9, -hitbox_height * 1.0),
            (hitbox_width * 0.9, hitbox_height * 0.5),
            (-hitbox_width * 0.9, hitbox_height * 0.5)
        ]
    elif element == 'stone_tall':
        return [
            (-hitbox_width * 0.6, -hitbox_height * 0.8),
            (hitbox_width * 0.6, -hitbox_height * 0.8),
            (hitbox_width * 0.6, hitbox_height * 0.4),
            (-hitbox_width * 0.6, hitbox_height * 0.4)
        ]
    else:
        return [
            (-hitbox_width / 2, -hitbox_height / 2),
            (hitbox_width / 2, -hitbox_height / 2),
            (hitbox_width / 2, hitbox_height / 2),
            (-hitbox_width / 2, hitbox_height / 2)
        ]


def has_collision(element_type):
    """Determine if an element should have collision"""
    collision_types = {
        'tree_blocks_fall', 'tree_fat_fall', 'tree_thin_fall', 'tree_tall_fall',
        'tree_default_fall', 'tree_oak_fall',
        'stone_tall', 'stone_large', 'log', 'log_large'
    }
    return element_type in collision_types