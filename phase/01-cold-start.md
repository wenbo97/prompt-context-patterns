# Chapter 1: The Cold Start Problem

## Problem

Our AI coding assistant needs to run build commands. But the build environment requires a heavy initialization script that takes **3-5 minutes** to load. Every time the AI opens a new terminal to run `msbuild`, it starts cold.

```
[AI] Let me check if your fix compiles...
[Terminal] Loading build environment... (3 min)
[Terminal] Restoring packages... (1 min)  
[Terminal] Building project... (10 sec)
[AI] Build succeeded!
```

That's 4 minutes of waiting for 10 seconds of useful work. For a single project, annoying. For 1000 projects, impossible.

## Thinking

We need the build environment to initialize **once** and stay alive across multiple AI interactions. The options:

| Approach | Pros | Cons |
|----------|------|------|
| **Background terminal** | Simple | AI can't send commands to it |
| **HTTP server wrapping the shell** | Standard API | Needs port management, firewall rules |
| **Named pipe to a persistent process** | No network, native IPC, bidirectional | Windows-specific |

We're on Windows, the build system is Windows-specific anyway, and we don't want to deal with port conflicts on locked-down dev machines.

## Solution

Built an **MCP server** (Model Context Protocol — a standard interface for AI tools) that:

1. Spawns a `cmd.exe` process at startup and runs the init script
2. Keeps that process alive in the background
3. Communicates via **named pipes** — the AI sends a build command, the pipe routes it to the living shell, and the output comes back

```
AI Assistant  →  MCP Tool  →  Named Pipe  →  Persistent Shell (already initialized)
                                              ↳ runs build in 10 seconds, not 4 minutes
```

The init script runs once. Every subsequent build command is fast.

**Key design choice**: We used a `SemaphoreSlim` to ensure only one command runs at a time through the pipe. Concurrent commands to a single `cmd.exe` stdin would produce garbled output.
