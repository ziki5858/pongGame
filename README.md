# Pong Game 🎮

**Technology stack** 🛠️  Python 3.12 · Pygame 2.6 · Standard Library only  
**Difficulty focus** 🧠  Real-time input · bounded AI · modular architecture  

---

## 1  Executive Summary 🚀
This repo contains a fully-playable remake of *Pong* written from scratch in Pygame.

* ✨ **Multi-ball mode** (1-3 balls) with independent physics.  
* 🤖 **Three AI levels** driven by analytic trajectory prediction.  
* 🎛️ **GUI settings panel** — no CLI flags required.  
* 🏎️ **60 FPS loop** with strict separation of rendering, physics & input.  

---

## 2  Quick Start ⚡
```bash
python -m venv venv
source venv/bin/activate   # Windows ➜ venv\Scripts\activate
pip install pygame==2.6.1
python pongGame.py
```
*All assets (sprites 🎨 + sounds 🔊) ship with the repo.*

### Controls 🎮
| Player | Keys |
|--------|------|
| **Left paddle** | **W** = up · **S** = down |
| **Right paddle** (human) | **↑** = up · **↓** = down |
| **Global** | **C/F** choose Computer/Friend · **Esc** to quit |

---

## 3  Folder Layout 📂
```
├─ ball.py              # Ball sprite + velocity helpers
├─ player.py            # Paddle sprite + life management
├─ InputBox.py          # Numeric text field widget
├─ GameTextManager.py   # HUD & menu rendering
├─ GameBoardManager.py  # Screen + sprite orchestration
├─ BallManager.py       # Physics + collisions + redraw
├─ CollisionManager.py  # Pure collision logic & scoring
├─ MovementManager.py   # Human controls + AI steering
├─ constantsGlobal.py   # Tunables + runtime state container
└─ pongGame.py          # Entry point & game loop
```

---

## 4  Architecture Overview 🏗️
The codebase follows a **“manager / sprite”** split that keeps gameplay logic, rendering, and low‑level physics neatly separated:

| Layer | Main Classes | Responsibility |
|-------|--------------|----------------|
| **Rendering** | `GameBoardManager`, `GameTextManager` | Screen clears, HUD, menus, centre‑line; no physics knowledge. |
| **Physics** | `BallManager`, `CollisionManager` | Ball stepping, paddle/wall/side collision, scoring. |
| **Input & AI** | `MovementManager` | Human key handling **plus** analytic AI that predicts the earliest ball intercept. |
| **State** | `GlobalData` | Single, typed container for runtime settings and sprite groups. |

Such layering means you can redesign the UI (e.g. switch to OpenGL) without touching physics, or swap in a reinforcement‑learning agent without rewriting rendering.

---

## 5  Key Design Decisions 📝
* 🔮 **Analytic AI over simulation** — predictable & O(1) cost regardless of FPS.  
* 💾 **Lazy asset caching** — fonts & sprites loaded once, zero per‑frame I/O.  
* 🔄 **No circular imports** — managers expose minimal public APIs, keeping modules testable.  
* ♻️ **Clean restart flow** — blocking loop ensures fresh state reset without recreating the window.  

---

## 6  Potential Extensions 🔭
1. **Event bus / ECS** for decoupled signalling between subsystems.  
2. **Unit tests** for collision math (PyTest).  
3. **Dynamic scaling**—derive positions from logical coords so the window can resize.  
4. **Power‑ups**: paddle shrink/expand, speed toggles, multi‑ball on hit.  

---

## 7  License 📜
Released under the MIT License — free to use, modify & distribute.
