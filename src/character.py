"""Character sprite with animations and wave mode."""
import arcade
from math import pi
from constants import CHARACTER_SCALE, WAVE_MODE_ALPHA


class Character(arcade.Sprite):
    """Character with animation support"""

    def __init__(self):
        super().__init__()

        # Load character textures
        self.idle_textures = []
        self.run_textures = []
        self.run_left_textures = []
        self.run_right_textures = []

        try:
            # Load idle animations
            idle_patterns = [
                "assets/characters/character2_idle/character_1-5.png",
                "assets/characters/character2_idle/character_2-4.png",
                "assets/characters/character2_idle/character_3-4.png",
                "assets/characters/character2_idle/character_4-4.png",
                "assets/characters/character2_idle/character_5-4.png",
                "assets/characters/character2_idle/character_6-4.png",
                "assets/characters/character2_idle/character_7-4.png",
                "assets/characters/character2_idle/character_8-5.png"
            ]
            for pattern in idle_patterns:
                texture = arcade.load_texture(pattern)
                self.idle_textures.append(texture)

            # Load forward run animations
            run_patterns = [
                "assets/characters/character2_run/character_1-4.png",
                "assets/characters/character2_run/character_2-3.png",
                "assets/characters/character2_run/character_3-3.png",
                "assets/characters/character2_run/character_4-3.png",
                "assets/characters/character2_run/character_5-3.png",
                "assets/characters/character2_run/character_6-3.png",
                "assets/characters/character2_run/character_7-3.png",
                "assets/characters/character2_run/character_8-4.png"
            ]
            for pattern in run_patterns:
                try:
                    texture = arcade.load_texture(pattern)
                    self.run_textures.append(texture)
                except Exception as e:
                    print(f"Could not load {pattern}: {e}")

            # Load left run animations
            left_patterns = [
                "assets/characters/character2_left/character_1-9.png",
                "assets/characters/character2_left/character_2-8.png",
                "assets/characters/character2_left/character_3-8.png",
                "assets/characters/character2_left/character_4-8.png",
                "assets/characters/character2_left/character_5-8.png",
                "assets/characters/character2_left/character_6-8.png",
                "assets/characters/character2_left/character_7-8.png",
                "assets/characters/character2_left/character_8-9.png"
            ]
            for pattern in left_patterns:
                try:
                    texture = arcade.load_texture(pattern)
                    self.run_left_textures.append(texture)
                except Exception as e:
                    print(f"Could not load {pattern}: {e}")

            # Load right run animations
            right_patterns = [
                "assets/characters/character2_right/character_1-8.png",
                "assets/characters/character2_right/character_2-7.png",
                "assets/characters/character2_right/character_3-7.png",
                "assets/characters/character2_right/character_4-7.png",
                "assets/characters/character2_right/character_5-7.png",
                "assets/characters/character2_right/character_6-7.png",
                "assets/characters/character2_right/character_7-7.png",
                "assets/characters/character2_right/character_8-8.png"
            ]
            for pattern in right_patterns:
                try:
                    texture = arcade.load_texture(pattern)
                    self.run_right_textures.append(texture)
                except Exception as e:
                    print(f"Could not load {pattern}: {e}")

        except Exception as e:
            print(f"Error loading character textures: {e}")

        # Fallback if no textures loaded
        if not self.idle_textures:
            self.idle_textures = [arcade.make_soft_square_texture(32, arcade.color.BLUE, 255, 255)]
        if not self.run_textures:
            self.run_textures = self.idle_textures
        if not self.run_left_textures:
            self.run_left_textures = self.run_textures
        if not self.run_right_textures:
            self.run_right_textures = self.run_textures

        # Set initial texture
        self.texture = self.run_textures[0] if self.run_textures else self.idle_textures[0]
        self.scale = CHARACTER_SCALE

        # Animation state
        self.current_frame = 0
        self.frame_counter = 0
        self.current_animation = "forward"

        # Movement direction (in radians)
        self.direction = 0

        # Isometric position tracking
        self.iso_x = 0
        self.iso_y = 0

        # Wave mode state
        self.in_wave_mode = False

    def update_animation(self, delta_time=1 / 60, turn_direction=0):
        """Update character animation based on movement direction"""
        self.frame_counter += 1

        # Determine which animation to use
        if turn_direction > 0:
            target_animation = "left"
            texture_list = self.run_left_textures
        elif turn_direction < 0:
            target_animation = "right"
            texture_list = self.run_right_textures
        else:
            target_animation = "forward"
            texture_list = self.run_textures

        # Reset frame if animation changed
        if target_animation != self.current_animation:
            self.current_animation = target_animation
            self.current_frame = 0
            self.frame_counter = 0

        # Change frame every 6 updates
        if self.frame_counter >= 6:
            self.frame_counter = 0
            if texture_list:
                self.current_frame = (self.current_frame + 1) % len(texture_list)
                self.texture = texture_list[self.current_frame]

    def set_wave_mode(self, enabled):
        """Toggle wave mode visual effect"""
        self.in_wave_mode = enabled
        if enabled:
            self.alpha = WAVE_MODE_ALPHA
        else:
            self.alpha = 255