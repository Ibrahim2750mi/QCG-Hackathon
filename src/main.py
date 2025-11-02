import arcade
import random
import math

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Procedural Forest Terrain"

# Tile settings
TILE_WIDTH = 128
TILE_HEIGHT = 64

# Camera movement speed
CAMERA_SPEED = 10

# Character settings
CHARACTER_SPEED = 6
CHARACTER_SCALE = 1.0

# Chunk settings
CHUNK_SIZE = 16
RENDER_DISTANCE = 4

# Master seed for reproducible terrain
MASTER_SEED = 12345

# Scene layer names
LAYER_NAME_GROUND = "Ground"
LAYER_NAME_OBJECTS = "Objects"
LAYER_NAME_WALLS = "Walls"
LAYER_NAME_CHARACTERS = "Characters"


class Character(arcade.Sprite):
    """Character with animation support"""

    def __init__(self, character_folder="character_run"):
        super().__init__()

        # Load character textures
        self.idle_textures = []
        self.run_textures = []

        try:
            # Load idle animations (try character_idle folder)
            for i in range(1, 9):
                for pattern in [f"assets/characters/character_idle/character_{i}-3.png",
                                f"assets/characters/character_idle/character_{i}-2.png"]:
                    try:
                        texture = arcade.load_texture(pattern)
                        self.idle_textures.append(texture)
                        break
                    except:
                        continue

            # Load run animations from specified folder
            if character_folder == "assets/characters/character_run":
                # Original character uses sprite_3_X.png format
                for i in range(8):
                    try:
                        texture = arcade.load_texture(f"{character_folder}/sprite_3_{i}.png")
                        self.run_textures.append(texture)
                    except:
                        pass
            elif character_folder == "assets/characters/character2_run":
                # Character 2 uses character_X-Y.png format
                patterns = [
                    f"{character_folder}/character_1-4.png",
                    f"{character_folder}/character_2-3.png",
                    f"{character_folder}/character_3-3.png",
                    f"{character_folder}/character_4-3.png",
                    f"{character_folder}/character_5-3.png",
                    f"{character_folder}/character_6-3.png",
                    f"{character_folder}/character_7-3.png",
                    f"{character_folder}/character_8-4.png"
                ]
                for pattern in patterns:
                    try:
                        texture = arcade.load_texture(pattern)
                        self.run_textures.append(texture)
                    except Exception as e:
                        print(f"Could not load {pattern}: {e}")
        except Exception as e:
            print(f"Error loading character textures: {e}")

        # Fallback if no textures loaded
        if not self.idle_textures:
            self.idle_textures = [arcade.make_soft_square_texture(32, arcade.color.BLUE, 255, 255)]
        if not self.run_textures:
            self.run_textures = self.idle_textures

        # Set initial texture
        self.texture = self.idle_textures[0] if self.idle_textures else self.run_textures[0]
        self.scale = CHARACTER_SCALE

        # Animation state
        self.current_frame = 0
        self.frame_counter = 0
        self.is_moving = False

        # Isometric position tracking
        self.iso_x = 0
        self.iso_y = 0

    def update_animation(self, delta_time):
        """Update character animation"""
        self.frame_counter += 1

        # Change frame every 8 updates
        if self.frame_counter >= 8:
            self.frame_counter = 0

            if self.is_moving and self.run_textures:
                self.current_frame = (self.current_frame + 1) % len(self.run_textures)
                self.texture = self.run_textures[self.current_frame]
            elif self.idle_textures:
                self.current_frame = (self.current_frame + 1) % len(self.idle_textures)
                self.texture = self.idle_textures[self.current_frame]


class ProceduralForestTerrain(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.SKY_BLUE)

        # Camera setup - using modern Camera2D
        self.camera = arcade.camera.Camera2D()

        # Scene to manage all sprites
        self.scene = None

        # Load textures
        self.textures = {}
        self.load_textures()

        # Store active chunks {(chunk_x, chunk_y): chunk_data}
        self.chunks = {}

        # Character
        self.character = None

        # Physics engine
        self.physics_engine = None

        # Movement keys
        self.keys_pressed = {
            'up': False,
            'down': False,
            'left': False,
            'right': False
        }

    def load_textures(self):
        """Load all forest-themed textures"""
        try:
            # Ground tiles
            self.textures['grass'] = arcade.load_texture("assets/terrain/ground_grass_NE.png")

            # Trees (various types for variety)
            self.textures['tree_blocks_fall'] = arcade.load_texture("assets/terrain/tree_blocks_fall_NE.png")
            self.textures['tree_default_fall'] = arcade.load_texture("assets/terrain/tree_default_fall_NE.png")
            self.textures['tree_fat_fall'] = arcade.load_texture("assets/terrain/tree_fat_fall_NE.png")
            self.textures['tree_thin_fall'] = arcade.load_texture("assets/terrain/tree_thin_fall_NE.png")
            self.textures['tree_oak_fall'] = arcade.load_texture("assets/terrain/tree_oak_fall_NE.png")

            # Rocks and details
            self.textures['stone_tall'] = arcade.load_texture("assets/terrain/stone_tallG_NE.png")
            self.textures['stone_large'] = arcade.load_texture("assets/terrain/stone_largeC_NE.png")

            # Plants
            self.textures['bush_small'] = arcade.load_texture("assets/terrain/plant_bushSmall_NE.png")

            # Logs
            self.textures['log'] = arcade.load_texture("assets/terrain/log_NE.png")
            self.textures['log_large'] = arcade.load_texture("assets/terrain/log_large_NE.png")

        except Exception as e:
            print(f"Error loading textures: {e}")
            # Create a fallback texture
            self.textures['grass'] = arcade.load_texture(":resources:images/tiles/grassCenter.png")

    def setup(self):
        """Set up initial scene, chunks and character"""
        # Create the Scene with organized layers
        self.scene = arcade.Scene()

        # Add sprite lists for different layers
        self.scene.add_sprite_list(LAYER_NAME_GROUND)
        self.scene.add_sprite_list(LAYER_NAME_OBJECTS, use_spatial_hash=True)
        self.scene.add_sprite_list(LAYER_NAME_WALLS, use_spatial_hash=True)
        self.scene.add_sprite_list(LAYER_NAME_CHARACTERS)

        # Create character
        self.character = Character()
        self.character.center_x = SCREEN_WIDTH / 2
        self.character.center_y = SCREEN_HEIGHT / 2
        self.character.iso_x = 0
        self.character.iso_y = 0

        # Add character to scene
        self.scene.add_sprite(LAYER_NAME_CHARACTERS, self.character)

        # Generate initial chunks
        self.update_chunks()

        # Initialize physics engine with walls from scene
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.character,
            self.scene[LAYER_NAME_WALLS]
        )

    def iso_to_screen(self, iso_x, iso_y):
        """Convert isometric grid coordinates to screen coordinates"""
        screen_x = (iso_x - iso_y) * (TILE_WIDTH / 2)
        screen_y = (iso_x + iso_y) * (TILE_HEIGHT / 2)
        return screen_x, screen_y

    def screen_to_chunk(self, screen_x, screen_y):
        """Convert screen coordinates to chunk coordinates"""
        tiles_per_chunk = CHUNK_SIZE
        chunk_x = int(screen_x / (TILE_WIDTH * tiles_per_chunk / 2))
        chunk_y = int(screen_y / (TILE_HEIGHT * tiles_per_chunk / 2))
        return chunk_x, chunk_y

    def get_chunk_seed(self, chunk_x, chunk_y):
        """Generate a unique seed for each chunk using activation function"""
        center_x = chunk_x * CHUNK_SIZE + CHUNK_SIZE // 2
        center_y = chunk_y * CHUNK_SIZE + CHUNK_SIZE // 2

        combined = MASTER_SEED * math.sin(center_x * 0.1) * math.cos(center_y * 0.1)
        combined += (center_x * 73856093) ^ (center_y * 19349663)

        activated_seed = int(abs(combined * 1000) % (2 ** 31 - 1))
        return activated_seed

    def get_hitbox_for_element(self, element):
        """Get custom hitbox for specific elements with directional extensions"""
        hitbox_width = TILE_WIDTH * 0.3
        hitbox_height = TILE_HEIGHT * 0.3

        # Trees need extended hitboxes towards the bottom (where trunk appears visually)
        if 'tree' in element:
            return [
                (-hitbox_width * 0.5, -hitbox_height * 3.0),
                (hitbox_width * 0.5, -hitbox_height * 3.0),
                (hitbox_width * 0.5, hitbox_height * 0.8),
                (-hitbox_width * 0.5, hitbox_height * 0.8)
            ]

        # Large rocks get slightly extended hitbox
        elif element == 'rock_large':
            return [
                (-hitbox_width * 0.8, -hitbox_height * 1.2),
                (hitbox_width * 0.8, -hitbox_height * 1.2),
                (hitbox_width * 0.8, hitbox_height * 0.6),
                (-hitbox_width * 0.8, hitbox_height * 0.6)
            ]

        # Logs and stumps
        elif element in ['log', 'log_large']:
            return [
                (-hitbox_width * 0.9, -hitbox_height * 1.0),
                (hitbox_width * 0.9, -hitbox_height * 1.0),
                (hitbox_width * 0.9, hitbox_height * 0.5),
                (-hitbox_width * 0.9, hitbox_height * 0.5)
            ]

        # Large bushes
        elif element == 'stone_tall':
            return [
                (-hitbox_width * 0.6, -hitbox_height * 0.8),
                (hitbox_width * 0.6, -hitbox_height * 0.8),
                (hitbox_width * 0.6, hitbox_height * 0.4),
                (-hitbox_width * 0.6, hitbox_height * 0.4)
            ]

        # Default hitbox
        else:
            return [
                (-hitbox_width / 2, -hitbox_height / 2),
                (hitbox_width / 2, -hitbox_height / 2),
                (hitbox_width / 2, hitbox_height / 2),
                (-hitbox_width / 2, hitbox_height / 2)
            ]

    def has_collision(self, element_type):
        """Determine if an element should have collision"""
        collision_types = {
            'tree_blocks_fall', 'tree_fat_fall', 'tree_thin_fall', 'tree_tall_fall',
            'tree_default_fall', 'tree_oak_fall',
            'stone_tall', 'stone_large', 'log', 'log_large'
        }
        return element_type in collision_types

    def generate_terrain_element(self, tile_x, tile_y, rng):
        """Determine what terrain element to place at this position"""
        noise = rng.random()

        if noise < 0.35:
            tree_type = rng.random()
            if tree_type < 0.3:
                return 'tree_blocks_fall'
            elif tree_type < 0.5:
                return 'tree_oak_fall'
            elif tree_type < 0.7:
                return 'tree_default_fall'
            elif tree_type < 0.85:
                return 'tree_fat_fall'
            else:
                return 'tree_thin_fall'
        elif noise < 0.40:
            return 'stone_tall' if rng.random() < 0.7 else 'stone_large'
        elif noise < 0.43:
            return 'log' if rng.random() < 0.6 else 'log_large'
        elif noise < 0.48:
            return 'bush_small'
        else:
            return None

    def create_chunk(self, chunk_x, chunk_y):
        """Create a chunk of tiles and add to scene"""
        chunk_seed = self.get_chunk_seed(chunk_x, chunk_y)
        rng = random.Random(chunk_seed)

        start_tile_x = chunk_x * CHUNK_SIZE
        start_tile_y = chunk_y * CHUNK_SIZE

        # Store sprites for this chunk so we can remove them later
        chunk_sprites = {
            'ground': [],
            'objects': [],
            'walls': []
        }

        for x in range(CHUNK_SIZE):
            for y in range(CHUNK_SIZE):
                tile_x = start_tile_x + x
                tile_y = start_tile_y + y

                screen_x, screen_y = self.iso_to_screen(tile_x, tile_y)

                # Create ground sprite
                grass_sprite = arcade.Sprite()
                grass_sprite.texture = self.textures['grass']
                grass_sprite.center_x = screen_x
                grass_sprite.center_y = screen_y
                self.scene.add_sprite(LAYER_NAME_GROUND, grass_sprite)
                chunk_sprites['ground'].append(grass_sprite)

                # Generate terrain element
                element = self.generate_terrain_element(tile_x, tile_y, rng)
                if element and element in self.textures:
                    detail_sprite = arcade.Sprite()
                    detail_sprite.texture = self.textures[element]
                    detail_sprite.center_x = screen_x
                    detail_sprite.center_y = screen_y
                    detail_sprite.iso_x = tile_x
                    detail_sprite.iso_y = tile_y

                    # Set up hitbox for collision objects
                    if self.has_collision(element):
                        hitbox_points = self.get_hitbox_for_element(element)
                        detail_sprite.hit_box = arcade.hitbox.HitBox(
                            hitbox_points,
                            position=(detail_sprite.center_x, detail_sprite.center_y)
                        )
                        # Add to walls layer
                        self.scene.add_sprite(LAYER_NAME_WALLS, detail_sprite)
                        chunk_sprites['walls'].append(detail_sprite)
                    else:
                        # Non-collision objects go to objects layer
                        self.scene.add_sprite(LAYER_NAME_OBJECTS, detail_sprite)
                        chunk_sprites['objects'].append(detail_sprite)

        return chunk_sprites

    def update_chunks(self):
        """Update chunks based on camera position"""
        center_chunk_x, center_chunk_y = self.screen_to_chunk(
            self.camera.position[0] + SCREEN_WIDTH / 2,
            self.camera.position[1] + SCREEN_HEIGHT / 2
        )

        chunks_needed = set()
        for dx in range(-RENDER_DISTANCE, RENDER_DISTANCE + 1):
            for dy in range(-RENDER_DISTANCE, RENDER_DISTANCE + 1):
                chunks_needed.add((center_chunk_x + dx, center_chunk_y + dy))

        # Remove chunks that are too far
        chunks_to_remove = []
        for chunk_pos in self.chunks.keys():
            if chunk_pos not in chunks_needed:
                chunks_to_remove.append(chunk_pos)

        for chunk_pos in chunks_to_remove:
            chunk_data = self.chunks[chunk_pos]
            # Remove sprites from scene
            for sprite in chunk_data['ground']:
                sprite.remove_from_sprite_lists()
            for sprite in chunk_data['objects']:
                sprite.remove_from_sprite_lists()
            for sprite in chunk_data['walls']:
                sprite.remove_from_sprite_lists()
            del self.chunks[chunk_pos]

        # Create new chunks
        for chunk_pos in chunks_needed:
            if chunk_pos not in self.chunks:
                self.chunks[chunk_pos] = self.create_chunk(*chunk_pos)

    def on_key_press(self, key, modifiers):
        """Handle key press"""
        if key == arcade.key.UP or key == arcade.key.W:
            self.keys_pressed['up'] = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.keys_pressed['down'] = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.keys_pressed['left'] = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.keys_pressed['right'] = True

    def on_key_release(self, key, modifiers):
        """Handle key release"""
        if key == arcade.key.UP or key == arcade.key.W:
            self.keys_pressed['up'] = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.keys_pressed['down'] = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.keys_pressed['left'] = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.keys_pressed['right'] = False

    def on_update(self, delta_time):
        """Update camera position and character"""
        moved = False

        # Set character velocity based on keys
        self.character.change_x = 0
        self.character.change_y = 0

        if self.keys_pressed['up']:
            self.character.change_y = CHARACTER_SPEED
            moved = True
        if self.keys_pressed['down']:
            self.character.change_y = -CHARACTER_SPEED
            moved = True
        if self.keys_pressed['left']:
            self.character.change_x = -CHARACTER_SPEED
            moved = True
        if self.keys_pressed['right']:
            self.character.change_x = CHARACTER_SPEED
            moved = True

        # Store old position for camera calculation
        old_x = self.character.center_x
        old_y = self.character.center_y

        # Update physics for player
        self.physics_engine.update()

        # Calculate movement delta for camera
        move_x = self.character.center_x - old_x
        move_y = self.character.center_y - old_y

        if abs(move_x) > 0.1 or abs(move_y) > 0.1:
            # Update camera to follow character
            current_pos = self.camera.position
            self.camera.position = (current_pos[0] + move_x, current_pos[1] + move_y)
            self.update_chunks()
            self.character.is_moving = True
        else:
            self.character.is_moving = moved

        # Update animations
        self.character.update_animation(delta_time)

    def on_draw(self):
        """Render the screen with proper layering"""
        self.clear()

        self.camera.use()

        # Draw ground layer
        self.scene[LAYER_NAME_GROUND].draw()

        # For isometric rendering, we need to sort objects and character by Y position
        # Collect all sprites that need Y-sorting
        all_objects = []
        all_objects.extend(self.scene[LAYER_NAME_OBJECTS])
        all_objects.extend(self.scene[LAYER_NAME_WALLS])
        all_objects.extend(self.scene[LAYER_NAME_CHARACTERS])

        # Sort by Y position (lower Y = drawn first = appears behind)
        all_objects.sort(key=lambda s: -s.center_y)

        spritelist = arcade.sprite_list.SpriteList(use_spatial_hash=True)
        spritelist.extend(all_objects)
        spritelist.draw()


def main():
    window = ProceduralForestTerrain()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()