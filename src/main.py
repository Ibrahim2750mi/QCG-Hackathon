from math import sqrt, sin, cos, pi
from pathlib import Path
import arcade

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TILE_SIZE = 64
CHUNK_SIZE = 16


def rect2iso(x, y):
    """Convert to isometric"""
    iso_x = x * (sqrt(2) / 2) + y * (sqrt(2) / 2)
    iso_y = -x * (sqrt(2) / 2) + y * (sqrt(2) / 2)
    return iso_x, -iso_y / sqrt(2)


class QuantumState:
    """Minimal quantum simulator for terrain"""

    def __init__(self, x, y):
        # Use position directly for phase, not seed
        # This creates unique quantum states per tile
        self.phase = (x * 0.1234 + y * 0.4321 + sin(x * 0.1) * cos(y * 0.1)) % (2 * pi)

    def hadamard(self):
        """Create superposition"""
        self.phase = (self.phase + pi / 4) % (2 * pi)

    def rotate(self, angle):
        """Rotate phase"""
        self.phase = (self.phase + angle) % (2 * pi)

    def measure(self):
        """Get probability (0 to 1)"""
        return (cos(self.phase) + 1) / 2


def quantum_terrain(tile_x, tile_y):
    """Generate terrain using quantum states - each tile gets unique quantum behavior"""
    # Create quantum state directly from world position
    q = QuantumState(tile_x, tile_y)

    # Apply quantum gates - creates interference patterns
    q.hadamard()  # Superposition

    # Spatial correlation with more variation
    angle = (tile_x * 0.314 + tile_y * 0.271 + sin(tile_x * 0.05) * 3.14) % (2 * pi)
    q.rotate(angle)

    q.hadamard()  # Interference

    # Additional rotation for more chaos
    q.rotate((tile_x * tile_y * 0.001) % (2 * pi))

    # Measure quantum state
    density = q.measure()

    # Add second quantum state for more variation
    q2 = QuantumState(tile_y, tile_x)  # Flipped coords
    q2.hadamard()
    q2.rotate(tile_x * 0.1)
    variation = q2.measure()

    # Combine both measurements
    combined = (density + variation * 0.5) / 1.5

    # Determine terrain feature with non-uniform distribution
    if combined < 0.35:
        return None  # Empty
    elif combined < 0.45:
        return 'tree_thin'
    elif combined < 0.55:
        return 'tree_tall'
    elif combined < 0.65:
        return 'tree_fat'
    elif combined < 0.75:
        return 'stone_large'
    elif combined < 0.85:
        return 'log'
    else:
        return 'stone_tall' if (tile_x + tile_y) % 3 == 0 else 'bush_small'


class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Quantum Terrain")
        arcade.set_background_color(arcade.color.FOREST_GREEN)

        self.camera = arcade.camera.Camera2D()
        self.scene = arcade.Scene()
        self.scene.add_sprite_list("Ground")
        self.scene.add_sprite_list("Objects")

        # Player
        self.player = arcade.SpriteSolidColor(32, 32, arcade.color.RED)
        self.player.center_x = SCREEN_WIDTH / 2
        self.player.center_y = SCREEN_HEIGHT / 2

        # Load textures
        assets = Path("assets/terrain")
        try:
            self.textures = {
                'land': arcade.load_texture(str(assets / "land_iso.png")),
                'tree_thin': arcade.load_texture(str(assets / "tree_thin_fall_NW.png")),
                'tree_tall': arcade.load_texture(str(assets / "tree_tall_fall_NW.png")),
                'tree_fat': arcade.load_texture(str(assets / "tree_fat_fall_NW.png")),
                'stone_large': arcade.load_texture(str(assets / "stone_largeC_NW.png")),
                'stone_tall': arcade.load_texture(str(assets / "stone_tallG_NW.png")),
                'log': arcade.load_texture(str(assets / "log_NW.png")),
                'log_large': arcade.load_texture(str(assets / "log_large_NW.png")),
                'bush_small': arcade.load_texture(str(assets / "plant_bushSmall_NW.png")),
            }
            print("✓ Textures loaded")
        except Exception as e:
            print(f"✗ Texture error: {e}")
            self.textures = {
                'land': arcade.make_soft_square_texture(64, arcade.color.DARK_GREEN, 255, 255),
                'tree_thin': arcade.make_soft_square_texture(64, arcade.color.DARK_BROWN, 255, 255),
                'tree_tall': arcade.make_soft_square_texture(64, arcade.color.BROWN, 255, 255),
                'tree_fat': arcade.make_soft_square_texture(64, arcade.color.SADDLE_BROWN, 255, 255),
                'stone_large': arcade.make_soft_square_texture(64, arcade.color.GRAY, 255, 255),
                'stone_tall': arcade.make_soft_square_texture(64, arcade.color.LIGHT_GRAY, 255, 255),
                'log': arcade.make_soft_square_texture(64, arcade.color.WOOD_BROWN, 255, 255),
                'log_large': arcade.make_soft_square_texture(64, arcade.color.DARK_BROWN, 255, 255),
                'bush_small': arcade.make_soft_square_texture(64, arcade.color.DARK_GREEN, 255, 255),
            }

        self.chunks = {}
        self.keys = {'w': False, 'a': False, 's': False, 'd': False}

        # Generate initial terrain
        self.update_chunks()

    def screen_to_chunk(self, x, y):
        return int(x / (TILE_SIZE * CHUNK_SIZE)), int(y / (TILE_SIZE * CHUNK_SIZE))

    def update_chunks(self):
        cx, cy = self.screen_to_chunk(
            self.camera.position[0] + SCREEN_WIDTH / 2,
            self.camera.position[1] + SCREEN_HEIGHT / 2
        )

        # Keep only nearby chunks
        needed = {(cx + dx, cy + dy) for dx in range(-2, 3) for dy in range(-2, 3)}

        for pos in list(self.chunks.keys()):
            if pos not in needed:
                # Remove sprites from old chunks
                for sprite in self.chunks[pos]:
                    sprite.remove_from_sprite_lists()
                del self.chunks[pos]

        # Generate new chunks
        for pos in needed:
            if pos not in self.chunks:
                self.generate_chunk(pos[0], pos[1])

    def generate_chunk(self, chunk_x, chunk_y):
        """Generate chunk using quantum terrain - NO SEED, pure position-based"""
        sprites = []

        for x in range(CHUNK_SIZE):
            for y in range(CHUNK_SIZE):
                # World tile position (not chunk-relative)
                tile_x = chunk_x * CHUNK_SIZE + x
                tile_y = chunk_y * CHUNK_SIZE + y

                screen_x, screen_y = rect2iso(tile_x * TILE_SIZE, tile_y * TILE_SIZE)

                # Ground (always present)
                ground = arcade.Sprite()
                ground.texture = self.textures['land']
                ground.center_x = screen_x
                ground.center_y = screen_y
                self.scene.add_sprite("Ground", ground)
                sprites.append(ground)

                # Quantum-generated feature (deterministic per world position)
                feature = quantum_terrain(tile_x, tile_y)
                if feature and feature in self.textures:
                    obj = arcade.Sprite()
                    obj.texture = self.textures[feature]
                    obj.center_x = screen_x
                    obj.center_y = screen_y
                    self.scene.add_sprite("Objects", obj)
                    sprites.append(obj)

        self.chunks[(chunk_x, chunk_y)] = sprites
        print(f"Generated chunk ({chunk_x}, {chunk_y}) - {len(sprites)} sprites")

    def on_key_press(self, key, mod):
        if key == arcade.key.W: self.keys['w'] = True
        if key == arcade.key.A: self.keys['a'] = True
        if key == arcade.key.S: self.keys['s'] = True
        if key == arcade.key.D: self.keys['d'] = True

    def on_key_release(self, key, mod):
        if key == arcade.key.W: self.keys['w'] = False
        if key == arcade.key.A: self.keys['a'] = False
        if key == arcade.key.S: self.keys['s'] = False
        if key == arcade.key.D: self.keys['d'] = False

    def on_update(self, dt):
        speed = 5
        dx = dy = 0

        if self.keys['w']: dy = speed
        if self.keys['s']: dy = -speed
        if self.keys['a']: dx = -speed
        if self.keys['d']: dx = speed

        if dx or dy:
            self.player.center_x += dx
            self.player.center_y += dy
            self.camera.position = (
                self.camera.position[0] + dx,
                self.camera.position[1] + dy
            )
            self.update_chunks()

    def on_draw(self):
        self.clear()
        self.camera.use()

        # Draw ground layer
        self.scene["Ground"].draw()

        # Sort objects and player by y for depth
        objects = list(self.scene["Objects"].sprite_list)
        objects.append(self.player)
        objects.sort(key=lambda s: -s.center_y)

        sprite_list = arcade.sprite_list.SpriteList()

        for obj in objects:
            sprite_list.append(obj)
        sprite_list.draw()

        # UI (no camera transform)
        arcade.camera.Camera2D().use()

        arcade.draw_text(
            "QUANTUM TERRAIN GENERATION",
            10, SCREEN_HEIGHT - 30,
            arcade.color.CYAN, 14, bold=True
        )

        arcade.draw_text(
            f"Chunks: {len(self.chunks)} | Sprites: {len(self.scene['Ground']) + len(self.scene['Objects'])}",
            10, SCREEN_HEIGHT - 50,
            arcade.color.WHITE, 10
        )


if __name__ == "__main__":
    Game()
    arcade.run()