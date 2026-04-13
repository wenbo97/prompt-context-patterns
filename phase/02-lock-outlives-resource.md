# Chapter 2: When the Lock Dies Before the Door

## Problem

The persistent shell from Chapter 1 works great — until something goes wrong. A build hangs. A pipe read times out. And then:

```
[AI] Running next build command...
[Error] ObjectDisposedException: The semaphore has been disposed.
[AI] Let me try again...
[Error] ObjectDisposedException: The semaphore has been disposed.
```

Every command after the first error fails. The only fix is restarting the entire server.

## Thinking

When a pipe error occurs, our cleanup code runs:

```csharp
// The broken cleanup
void HandlePipeError() 
{
    _pipeStream.Dispose();   // ✓ clean up the broken pipe
    _semaphore.Dispose();    // ✗ wait — we need this to reconnect!
}
```

The semaphore guards access to the pipe. When the pipe breaks, we need to:
1. **Acquire the semaphore** (so no other thread is using the pipe)
2. **Dispose the old pipe**
3. **Create a new pipe**
4. **Release the semaphore**

But if we dispose the semaphore in step 1, step 4 is impossible. We killed the lock before we finished using it.

We considered:
- **Catch and swallow the exception** → masks race conditions, new bugs
- **Create a new semaphore on reconnect** → two threads could hold different semaphores simultaneously
- **Separate pipe disposal from semaphore disposal** → ✓ clean separation of concerns

## Solution

Split disposal into two layers:

```csharp
// Pipe resources can be disposed and recreated
void DisposePipeResources() 
{
    _pipeStream?.Dispose();
    _pipeStream = null;
}

// Semaphore lives for the entire server lifetime
void Dispose() 
{
    DisposePipeResources();
    _semaphore.Dispose();  // only here, on full shutdown
}

// Reconnection works because the semaphore is alive
async Task Reconnect() 
{
    await _semaphore.WaitAsync();  // ✓ semaphore still exists
    try {
        DisposePipeResources();
        _pipeStream = CreateNewPipe();
    } finally {
        _semaphore.Release();
    }
}
```

**The rule**: In async IPC, the synchronization primitive must **outlive** the resources it protects. If you dispose the lock, you can't use the lock to safely replace what it was guarding.
