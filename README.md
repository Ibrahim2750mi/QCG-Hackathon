# QCG-Hackathon
# Mam: Infinite Quantum Terrain Runner

**Mam** is an innovative isometric infinite runner game that merges quantum computing concepts with engaging procedurally generated gameplay. Powered by quantum-inspired algorithms, Mam delivers unpredictably diverse worlds and a unique gaming experience that showcases the potential of quantum computing in interactive entertainment.

![Game Genre](https://img.shields.io/badge/Genre-Infinite%20Runner-blue)
![Quantum Computing](https://img.shields.io/badge/Quantum-Inspired-purple)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![Arcade](https://img.shields.io/badge/Arcade-Library-red)

---

## 🌍 Core Concept

Mam delivers an endless isometric world built using quantum-enhanced procedural generation. Players navigate through ever-expanding terrain, dodging obstacles and collecting resources while experiencing truly unique gameplay powered by quantum algorithms. Each playthrough creates unrepeatable patterns that classical random generation cannot achieve.

---

## 🎮 Gameplay Features

### **Infinite Runner Mechanics**
- **Automatic Forward Movement**: Character constantly moves forward through the procedurally generated world
- **Dynamic Turning**: Use LEFT/RIGHT or A/D keys to smoothly change direction
- **Quantum Wave Mode**: Hold W to phase through obstacles using quantum energy
- **Score System**: Based on total displacement from starting position
- **Collision Penalties**: Hitting obstacles deducts 50 points (with 6-frame cooldown)

### **Quantum Wave Mode** ⚛️
- **Energy System**: 100% quantum energy that depletes at 2.5% per frame during use
- **Phasing Ability**: Pass through solid obstacles while in wave mode
- **Visual Effects**: Character becomes semi-transparent with cyan particle effects
- **Strategic Resource**: Energy recharges slowly (0.1% per frame) when not in use
- **Risk/Reward**: Choose when to use limited quantum energy for obstacle avoidance

### **Character Animation**
- Animated sprite with multiple states:
  - Forward running animation
  - Left turn animation
  - Right turn animation
  - Idle animation
- Smooth transitions between animation states
- Frame-based animation system (8 frames per animation)

---

## 🛠️ Quantum Technology Integration

### **Quantum-Driven Terrain Generation**

**Quantum State Simulation**:
- Custom `QuantumState` class simulates quantum phenomena
- Uses phase-based representation of quantum states
- Implements Hadamard gates for superposition creation
- Phase rotation operations for quantum interference effects

**Quantum Terrain Algorithm**:
```python
def quantum_terrain(tile_x, tile_y):
    """Generate terrain using quantum states"""
    q = QuantumState(tile_x, tile_y)
    q.hadamard()  # Create superposition
    q.rotate(angle)  # Apply quantum rotation
    q.hadamard()  # Second superposition
    density = q.measure()  # Collapse to classical value
```

**Key Features**:
- **Hadamard Transformations**: Create quantum superposition states
- **Phase Rotation**: Introduce quantum interference patterns
- **Measurement Collapse**: Convert quantum probabilities to terrain features
- **Multi-State Combination**: Blend multiple quantum states for varied terrain

### **Terrain Feature Distribution**
Quantum measurement probabilities determine terrain elements:
- **65% threshold**: Open grass tiles (no obstacles)
- **65-68%**: Thin fall trees
- **68-70%**: Fat fall trees
- **70-72%**: Oak fall trees
- **72-75%**: Large stones
- **75-77%**: Logs
- **77-100%**: Tall stones and small bushes

### **Comparison Modes**
Press **Q** to toggle between:
- **Quantum Mode**: Uses quantum state simulation for terrain generation
- **Random Mode**: Uses classical pseudo-random generation for comparison

---

## 🎯 Technical Features

### **Rendering System**
- **Isometric Projection**: Converts 2D grid coordinates to isometric screen space
- **Layer-Based Rendering**: Organized sprite layers for proper depth sorting
  - Ground layer (grass tiles)
  - Objects layer (decorative elements)
  - Walls layer (collision objects)
  - Coins layer (collectibles)
  - Characters layer (player sprite)
- **Depth Sorting**: Dynamic Y-position sorting for realistic object overlap
- **Efficient Culling**: Spatial hashing for optimized collision detection

### **Procedural Chunk System**
- **Chunk-Based Generation**: World divided into 16×16 tile chunks
- **Dynamic Loading**: Chunks generate as player approaches (4-chunk render distance)
- **Deterministic Seeds**: Each chunk uses unique seed for reproducible terrain
- **Memory Management**: Distant chunks automatically unload to optimize performance
- **Seed Activation Function**: Uses trigonometric functions for chunk seed variation

### **Physics & Collision**
- **Custom Hitboxes**: Directionally-extended collision boxes for visual accuracy
  - Trees: Extended downward for trunk collision
  - Rocks: Slightly enlarged for better gameplay feel
  - Logs: Elongated horizontal collision
- **Collision Detection**: Arcade physics engine with spatial hashing
- **Smooth Movement**: Continuous character movement with turn-based direction changes
- **Collision Feedback**: Visual warning and score penalty system

### **Camera System**
- **Modern Camera2D**: Uses Arcade's latest camera implementation
- **Smooth Following**: Camera tracks character movement in real-time
- **Dual Camera Modes**: World-space camera for terrain, screen-space for UI
- **Coordinate Conversion**: Seamless transformation between isometric and screen space

---

## 📋 Requirements

### **Dependencies**
```
Python 3.8+
arcade >= 2.6.0
```

### **Assets Required**
```
assets/
├── terrain/
│   ├── land_NE.png
│   ├── tree_blocks_fall_NE.png
│   ├── tree_default_fall_NE.png
│   ├── tree_fat_fall_NE.png
│   ├── tree_thin_fall_NE.png
│   ├── tree_oak_fall_NE.png
│   ├── stone_tallG_NE.png
│   ├── stone_largeC_NE.png
│   ├── plant_bushSmall_NE.png
│   ├── log_NE.png
│   ├── log_large_NE.png
│   └── skull-fotor-bg-remover-2025110325712.png
└── characters/
    ├── character2_idle/ (8 frames: character_1-5.png through character_8-5.png)
    ├── character2_run/ (8 frames: character_1-4.png through character_8-4.png)
    ├── character2_left/ (8 frames: character_1-9.png through character_8-9.png)
    └── character2_right/ (8 frames: character_1-8.png through character_8-8.png)
```

---

## 🚀 Getting Started

### **Installation**

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/QCG-Hackathon.git
   cd QCG-Hackathon
   ```

2. **Install Dependencies**
   ```bash
   pip install arcade
   ```

3. **Verify Assets**
   - Ensure all texture assets are in the `assets/` directory
   - Check that character animation frames are properly organized

4. **Run the Game**
   ```bash
   python src/main.py
   ```

---

## 🎮 Controls

| Key | Action |
|-----|--------|
| **LEFT** or **A** | Turn character left |
| **RIGHT** or **D** | Turn character right |
| **HOLD W** | Activate quantum wave mode (phase through obstacles) |
| **Q** | Toggle between Quantum and Random terrain generation |
| **R** | Restart game (when game over) |

---

## 🎨 Game Mechanics Explained

### **Score System**
- **Base Score**: Calculated from straight-line displacement from start position
- **Collision Penalty**: -50 points per collision with obstacles
- **Cooldown System**: 6-frame grace period between collision penalties
- **Final Score**: `Displacement + Total Penalties`

### **Quantum Energy Management**
- **Maximum Energy**: 100%
- **Drain Rate**: 2.5% per frame while wave mode active (~40 frames of continuous use)
- **Recharge Rate**: 0.1% per frame while inactive (1000 frames for full recharge)
- **Visual Indicator**: Cyan energy bar at top-left (turns red below 20%)

### **Obstacle Variety**
Generated obstacles include:
- **Trees**: 6 different fall tree variants with extended trunk collision
- **Stones**: Tall stones and large stone clusters
- **Logs**: Regular and large fallen logs
- **Bushes**: Small decorative bushes (no collision)

---

## 🔬 Quantum Algorithm Details

### **QuantumState Class**
Simulates quantum behavior for terrain generation:

**Phase-Based Representation**:
- Stores quantum state as phase angle (0 to 2π)
- Phase influenced by spatial coordinates and trigonometric functions

**Hadamard Gate**:
- Creates superposition by adding π/4 to phase
- Simulates equal probability of quantum states

**Rotation Gate**:
- Applies arbitrary phase rotation
- Introduces quantum interference patterns

**Measurement**:
- Collapses quantum state to classical probability
- Uses cosine function: `(cos(phase) + 1) / 2`
- Returns value between 0 and 1 for terrain threshold checks

### **Why Quantum for Terrain?**
- **True Unpredictability**: Quantum measurements produce irreproducible patterns
- **Interference Effects**: Phase rotations create natural-looking terrain variation
- **Superposition Benefits**: Hadamard gates enable multiple terrain possibilities
- **Educational Value**: Players experience quantum concepts through gameplay

---

## 🚀 Future Expansion Ideas

### **Multiplayer Quantum Worlds**
- Quantum entanglement mechanics linking player worlds
- Cooperative terrain modification
- Competitive obstacle courses with quantum randomness

### **Advanced Quantum Features**
- **Grover's Algorithm**: Efficient search for rare terrain features and items
- **Quantum Walks**: Biome distribution using quantum walk algorithms
- **Real Quantum Circuits**: Integration with IBM Q or other quantum backends
- **Quantum Teleportation**: Instant player movement mechanics

### **Enhanced Gameplay**
- Collectible coins and power-ups
- Boss encounters with quantum behavior
- Upgradeable quantum abilities
- Procedurally generated music using quantum randomness

### **Educational Elements**
- In-game quantum computing tutorials
- Visualization of quantum states during terrain generation
- Challenge modes teaching quantum concepts
- Quantum circuit builder mini-game

---

## 📊 Performance Specifications

- **Chunk Size**: 16×16 tiles per chunk
- **Render Distance**: 4 chunks in each direction (9×9 chunk grid)
- **Tile Dimensions**: 128×64 pixels (isometric)
- **Target Frame Rate**: 60 FPS
- **Screen Resolution**: 1280×720 pixels
- **Character Speed**: 8 pixels per frame
- **Turn Speed**: 0.1 radians per frame

---

## 🛠️ Development

### **Project Structure**
```
QCG-Hackathon/
├── src/
│   └── main.py              # Main game implementation
├── assets/
│   ├── terrain/             # Terrain texture assets
│   └── characters/          # Character animation frames
├── README.md                # This file
└── requirements.txt         # Python dependencies
```

### **Key Classes**
- **`QuantumState`**: Quantum simulation for terrain generation
- **`Character`**: Animated player sprite with wave mode
- **`ProceduralForestTerrain`**: Main game window and logic

### **Constants & Configuration**
All game parameters are easily adjustable:
- Screen dimensions and tile sizes
- Character movement speeds
- Chunk generation settings
- Quantum energy parameters
- Collision penalties and cooldowns

---

## 🤝 Contributing

We welcome contributions from quantum computing enthusiasts and game developers!

**Areas for Contribution**:
- Additional quantum algorithms (Shor's, QAOA, VQE)
- New terrain generation methods
- Gameplay features and mechanics
- Performance optimizations
- Educational content and tutorials
- Asset creation (sprites, animations, sounds)

**How to Contribute**:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📚 Learn More

### **Quantum Computing Resources**
- [Quantum Random Number Generation](https://qiskit.org/textbook/ch-algorithms/random-numbers.html)
- [Grover's Search Algorithm](https://qiskit.org/textbook/ch-algorithms/grover.html)
- [Quantum Walks](https://arxiv.org/abs/quant-ph/0303081)
- [Qiskit Textbook](https://qiskit.org/textbook/)

### **Game Development**
- [Python Arcade Documentation](https://api.arcade.academy/)
- [Procedural Generation Techniques](https://www.redblobgames.com/)
- [Isometric Game Development](https://gamedevelopment.tutsplus.com/tutorials/creating-isometric-worlds-a-primer-for-game-developers--gamedev-6511)

---

## 📜 License

This project is part of the Quantum Computing Game Hackathon. Please check repository for specific license information.

---

## 🎮 Credits

**Developed for**: Quantum Computing Game Hackathon  
**Engine**: Python Arcade Library  
**Quantum Concepts**: Inspired by real quantum computing principles  
**Game Design**: Infinite runner meets quantum physics  

---

## ❓ FAQ

**Q: Do I need a real quantum computer to run this?**  
A: No! The game simulates quantum behavior classically. However, future versions may integrate with real quantum backends.

**Q: What makes the terrain generation "quantum"?**  
A: We use quantum-inspired algorithms (superposition, phase rotation, measurement) to create genuinely unpredictable and non-repeating patterns.

**Q: Can I use this for learning quantum computing?**  
A: Absolutely! The game demonstrates quantum concepts like superposition, measurement, and quantum interference in an interactive way.

**Q: How is quantum terrain different from random terrain?**  
A: Press Q to compare! Quantum terrain uses interference patterns and phase-based generation, while random terrain uses standard pseudo-random numbers.

**Q: Is the game endless?**  
A: Yes! The procedurally generated world extends infinitely in all directions with unique terrain in every chunk.

---

## 🌟 Start Your Quantum Adventure!

Experience the fusion of quantum computing and gaming. Download Mam today and explore infinite worlds generated by the principles of quantum mechanics!

```bash
git clone https://github.com/yourusername/QCG-Hackathon.git
cd QCG-Hackathon
pip install arcade
python src/main.py
```

**Where science, fun, and infinite terrain unite!** ⚛️🎮🌍
