"""Game constants and configuration values."""
from math import pi

# Screen settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Procedural Forest Terrain - Infinite Runner"

# Tile settings
TILE_WIDTH = 128
TILE_HEIGHT = 64

# Camera movement speed
CAMERA_SPEED = 10

# Character settings
CHARACTER_SPEED = 12
TURN_SPEED = 0.15
CHARACTER_SCALE = 1.0

# Chunk settings
CHUNK_SIZE = 16
RENDER_DISTANCE = 4

# Master seed for reproducible terrain
MASTER_SEED = 12345

# Game settings
COLLISION_PENALTY = 50
COLLISION_COOLDOWN = 15

# Quantum wave mode settings
MAX_QUANTUM_ENERGY = 100
QUANTUM_DRAIN_RATE = 2.5
QUANTUM_RECHARGE_RATE = 0.1
WAVE_MODE_ALPHA = 128

# Scene layer names
LAYER_NAME_GROUND = "Ground"
LAYER_NAME_OBJECTS = "Objects"
LAYER_NAME_WALLS = "Walls"
LAYER_NAME_COINS = "Coins"
LAYER_NAME_CHARACTERS = "Characters"

# Coin settings
COIN_VALUE = 100
COIN_SPAWN_CHANCE = 0.15

# Health settings
MAX_HEALTH = 100
HEALTH_PENALTY = 2