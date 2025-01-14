# Snake Game

A classic **Snake** game implemented in Python using the `pygame` library. Control the snake, eat food to grow, and try to achieve the highest score without crashing into walls or yourself!

## Features
- **Dynamic Speed**: The game becomes faster as your score increases.
- **Scoring System**: Displays the current score at the top-left corner of the screen.
- **Restart Option**: Easily restart the game by pressing `R` after a game over.
- **Customizable**: Modify snake speed, colors, or grid size to make the game your own.

---

## Requirements
- Python 3.7+
- `pygame` library

### Install pygame
Use pip to install `pygame`:
```bash
pip install pygame
```

---

## How to Run
1. Save the main game file as `snake_game.py`.
2. Open a terminal and navigate to the directory containing the file.
3. Run the game using:
   ```bash
   python snake_game.py
   ```

---

## Controls
- **Arrow Keys**: Control the snake's movement.
  - `Up Arrow`: Move up
  - `Down Arrow`: Move down
  - `Left Arrow`: Move left
  - `Right Arrow`: Move right
- **R**: Restart the game after a game over.
- **Q**: Quit the game after a game over.

---

## Game Rules
1. Guide the snake to eat the red food. Each food increases your score by 1.
2. The snake grows longer as it eats, making the game progressively harder.
3. Avoid running into walls or the snake's own body.
4. If you crash, the game ends, and you can restart or quit.

---

## Customization
You can modify the following variables in the `snake_game.py` file:
- **Colors**: Change the snake, food, or background colors.
- **Speed**: Adjust the `clock.tick(10 + score // 5)` line to modify the speed progression.
- **Grid Size**: Modify `CELL_SIZE`, `WIDTH`, or `HEIGHT` for different layouts.

---

## Screenshot
![Snake Game Screenshot](https://via.placeholder.com/600x400.png?text=Snake+Game)
*Sample screenshot of the game interface.*

---

## License
This project is open-source and free to use for educational or personal purposes.

---

Happy gaming! 🎮
