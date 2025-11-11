# Placement-Protocol


# Placement-Protocol is a terminal-based real-time simulation written in pure Python. It is built to show a deep understanding of computer science fundamentals and practical system design.

Unlike simple terminal games, it is designed like a mini operating system. It combines:

* ECS (Entity Component System) architecture
* Threaded Input, AI, and Analytics Systems
* Event-driven State Machines
* Live Profiler & Memory Visualization
* Networking & Real-Time Data Streaming

Everything runs inside a single terminal window—no GUI, no engines—just logic, rendering, and engineering clarity.

---

## Features & Systems Breakdown

### Core Gameplay

* Two “engineers” compete in a terminal arena using movement and firing mechanics.
* Real-time rendering uses the curses library, optimized for per-frame updates.
* Memory-safe rendering, I/O buffering, and state synchronization.

---

### ECS (Entity-Component-System)

This demonstrates modular, scalable architecture inspired by modern game engines:

| Type           | Example                                                    |
| -------------- | ---------------------------------------------------------- |
| Entities       | Engineers, Powerups                                       |
| Components     | Position, Health, Skill, Score                            |
| Systems        | RenderingSystem, PhysicsSystem, EventSystem, NetworkSystem |

This shows an understanding of composition over inheritance, decoupled logic, and scalable architecture.

---

### State, Events & Game Loop

* The central EventBus manages all I/O, system updates, and threading safely.
* A full state machine handles menus, gameplay, pause, and overlay modes.
* Clean loop timing and frame management with a 60 FPS cap.

This demonstrates real-time event systems, timing, and loop design.

---

### Profiler & Diagnostics

* The built-in Profiler (toggle with `P`) shows:

  * FPS
  * Memory usage
  * Thread count
  * System event latency
* Memory usage is visualized as bar graphs (█ blocks).
* Logs every snapshot with a timestamp to placement_log.txt.

This demonstrates instrumentation, performance tracking, and runtime diagnostics.

---

### Persistence & I/O

* Save game state (F) and load (L) using JSON serialization.
* Buffered writes, safe threading, and live snapshot recovery.

This shows serialization, file I/O buffering, and safe concurrency.

---

### Spectator Analytics Server

This is a threaded TCP socket server that streams live match data as JSON.

Start with T or the console command:

```bash
nc localhost 9090
```

You’ll receive:

```json
{
  "time": 102.5,
  "uptime": "00:01:42",
  "fps": 58,
  "cpu": 8.1,
  "memory": 84,
  "clients": 2,
  "players": [
    {"name": "Aaryan", "health": 92, "score": 14},
    {"name": "Priya", "health": 88, "score": 15}
  ],
  "events": 3
}
```

This demonstrates network I/O, multithreading, and real-time telemetry.

---

### Developer Console

Press ` ` (backtick) to open the runtime console:

```bash
> heal p1 50
> spawn_powerup
> boost_fps
> log_state
```

This shows an understanding of REPL design, command parsing, and runtime debugging systems.

---

## Technical Concepts Demonstrated

| Concept           | Implementation                                          |
| ----------------- | ------------------------------------------------------- |
| State Management  | Finite state machine controlling arena, menus, overlays |
| Event System      | Central async EventBus for I/O and system communication |
| Threading         | Input, AI, and Analytics handled via daemon threads     |
| Memory Management | Live visualization and periodic monitoring              |
| I/O Buffering     | Buffered logs and file snapshots                        |
| ECS Architecture  | Modular composition for all entities and systems        |
| Serialization     | JSON-based save/load                                    |
| Profiling         | Real-time FPS, memory, and CPU usage overlay            |
| Networking        | Threaded socket analytics server                        |
| Diagnostics       | Leak detection and event latency tracking               |

---

## Why It’s Unique

This isn’t just a terminal game; it’s a sandbox for system design. It shows engineering clarity, architecture design thinking, and technical versatility, all in 100% Python, with no engines or frameworks involved.

---

## Setup & Run

### Requirements

```bash
pip install windows-curses psutil
```

### Run

```bash
python placement_war_ecs_stream.py
```

### Controls

| Action                  | Key           |
| ----------------------- | ------------- |
| Move Player 1           | W / A / S / D |
| Move Player 2           | Arrow Keys    |
| Fire                    | Space / Enter |
| Toggle Help Overlay     | H             |
| Toggle Profiler         | P             |
| Save / Load             | F / L         |
| Toggle Analytics Server | T             |
| Developer Console       | ` (backtick)  |
| Quit                    | Q             |

---

## File Outputs

| File                          | Description                           |
| ----------------------------- | ------------------------------------- |
| placement_log.txt            | Continuous game and performance log   |
| placement_save.json          | Saved game snapshot                   |
| stream_log.txt *(optional)*  | Analytics stream archive (if enabled) |

---

## Future Scope

* Remote multiplayer via sockets
* WebSocket dashboard for analytics visualization
* AI-driven placement simulations
* Plugin system for modding engineers’ abilities

---

## About the Developer

**Aniket Bisht**  
2nd-year B.Tech CSE 
Passionate about systems, AI, and building things that feel alive in the terminal.  
Dedicated to honoring his father’s legacy and making his mother proud.  
Focused on clarity, architecture, and creativity in every project.

---

## Key Takeaway

"This isn’t about pixels; it’s about processes. Every frame is proof of architecture."
