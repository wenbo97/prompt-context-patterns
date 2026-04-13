# Chapter 3: The AI Thinks It's on Linux

## Problem

Builds started failing with cryptic errors:

```
error MSB4184: The expression "[System.IO.Path]::GetFullPath('C:/PackageCache/...')" 
cannot be evaluated. The given path's format is not supported.
```

The path looks fine to a human. But the build system expects `C:\PackageCache\...` with **backslashes**.

Then a second problem: some commands sent by the AI made the entire shell session **freeze permanently**.

## Thinking

**The slash problem**: Our AI assistant was trained predominantly on Linux/macOS examples. When it generates file paths, it naturally uses forward slashes. On Linux, both `/` and `\` work. On Windows, most APIs accept both — except some MSBuild path validation rules that specifically require backslashes.

The tricky part: the path passes our initial validation (we weren't checking slashes), enters the build system, gets deep into MSBuild property evaluation, and fails there with an unhelpful error message.

**The freeze problem**: The AI sometimes generates commands like:

```batch
del /P somefile.dll          REM → prompts "Are you sure (Y/N)?"
choice /C YN /M "Continue?"  REM → waits for keypress
```

These commands wait for interactive input. But our named pipe doesn't provide interactive input — it's a one-way command/response channel. The shell blocks waiting for input that will never come, and the pipe blocks waiting for output that will never come. Deadlock.

## Solution

**For paths**: Normalize at the boundary. Every path entering the system gets backslash-converted before anything else happens:

```csharp
string NormalizePath(string path) => path.Replace('/', '\\');
```

Simple, but it has to be the **first** thing that happens to any path. If validation runs before normalization, the bug reappears.

**For dangerous commands**: Block before sending. We maintain a pattern list of commands known to hang pipes:

```csharp
bool IsUnsafeForPipe(string command)
{
    // Commands that request interactive input
    if (Regex.IsMatch(command, @"\bdel\s+/[pP]\b")) return true;
    if (Regex.IsMatch(command, @"\bchoice\b")) return true;
    if (Regex.IsMatch(command, @"\bpause\b")) return true;
    // ... more patterns
    return false;
}
```

**Two rules for AI-to-shell systems**:
1. The AI learned from Linux. Normalize everything at the system boundary.
2. The AI doesn't know what "interactive" means in a pipe context. Filter before sending.
