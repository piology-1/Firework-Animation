# Firework Animation

A simple Python project that creates an animated fireworks display using Pygame. The program starts with a countdown and displays a "Happy New Year!" message before launching colorful fireworks with different explosion patterns.

## Installation and Run

This project uses [uv](https://docs.astral.sh/uv/).

Install the project dependencies:

```bash
uv sync
```

Run the project:

```bash
uv run main.py
```

## How It Works

- `Launcher` creates and manages fireworks.
- `Firework` moves upward and explodes at a random height.
- `Projectile` represents individual particles created during an explosion.
- Fireworks can explode in circular or star-shaped patterns.
- Projectiles gradually fade and disappear when they leave the screen.
