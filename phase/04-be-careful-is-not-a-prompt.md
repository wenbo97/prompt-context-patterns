# Chapter 4: "Be Careful" Is Not a Prompt

## Problem

Chapters 1-3 built a reliable shell tool. Now we pointed it at real work: migrating .NET Framework projects to .NET Core, 200 at a time, fully automated.

First batch run results:

| Metric | Result |
|--------|--------|
| Projects attempted | 200 |
| Local build pass | **91%** |
| CI build pass | **36%** |

91% pass locally but only 36% pass CI. The AI is producing code that works on the dev machine but breaks in the controlled build environment.

## Thinking

We analyzed the 128 CI failures. They clustered into clear categories:

**Category A: The AI copied from the wrong place (34% of failures)**
```xml
<!-- The AI found this in ProjectB.csproj and copied it to ProjectA.csproj -->
<RuntimeIdentifier>win-x64</RuntimeIdentifier>
<!-- ProjectA doesn't need this. Now CI fails because the build farm is linux-x64 -->
```

Our prompt said: "Look at similar projects for reference." The AI interpreted "similar" very broadly.

**Category B: The AI took shortcuts (28% of failures)**
```csharp
// Original code that doesn't compile under .NET Core:
var cache = HttpRuntime.Cache;

// AI's "fix":
#if NETFRAMEWORK
var cache = HttpRuntime.Cache;
#else
throw new NotImplementedException(); // "I'll fix this later" — no, you won't
#endif
```

The AI jumps to the easiest fix. `NotImplementedException` makes the compiler happy but breaks at runtime.

**Category C: The AI ignored "minor" errors (22% of failures)**

Error codes like `NU1101` (package not found) and `MSB3202` (project reference not found) weren't in our "must fix" list. The AI treated them as warnings and moved on. CI treats them as errors.

## Solution

We replaced every vague instruction with a specific, testable rule:

**Before** (didn't work):
```
Be careful when referencing other projects. Make sure the properties you copy are relevant.
```

**After** (works):
```
RULE: Never copy MSBuild properties from other project files.
RULE: Every property you add must be justified by a specific build error in the current project.
WRONG: Copying <RuntimeIdentifier> from another project "because it has it"
RIGHT: Adding <RuntimeIdentifier> only if error NETSDK1083 explicitly requires it
```

**Before** (didn't work):
```
Try to fix compilation errors appropriately.
```

**After** (works):
```
Fix errors in this order. Exhaust each tier before moving to the next:
  Tier 1: Build file changes (.csproj, .props, .targets)
  Tier 2: #if NETFRAMEWORK conditionals  
  Tier 3: throw new NotImplementedException() — LAST RESORT ONLY
```

**Before** (didn't work):
```
Make sure the build succeeds before submitting.
```

**After** (works):
```
These error codes MUST be resolved (not suppressed): 
CS0246, CS0103, NU1101, NU1702, MSB3202, MSB4184
```

**The rule**: Vague instructions produce vague results. Every failure mode from production becomes a specific prompt rule with WRONG/RIGHT examples.
