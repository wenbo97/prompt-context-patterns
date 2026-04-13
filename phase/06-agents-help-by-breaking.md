# Chapter 6: The AI "Helps" by Breaking Things

## Problem

We had two specialized agents:
- **Migrator Agent**: modifies project files (`.csproj`, adds target frameworks, conditions packages)
- **Build Agent**: runs builds, analyzes errors, applies fixes

Clear separation. But we kept finding cases where the Migrator Agent had run build commands, and its "verification builds" modified files that the Build Agent later also modified — producing merge conflicts with itself.

```
[Migrator] Modified ProjectA.csproj — added net8.0 target
[Migrator] Let me verify this works... running build...
[Migrator] Build failed! Let me fix this error too...
[Migrator] Modified ProjectA.csproj — added <NoWarn> for NU1701
           ↑ This fix belongs to the Build Agent's phase
           
[Build Agent] Starting build phase...
[Build Agent] I see NU1701 — adding <NoWarn>...
[Build Agent] ERROR: merge conflict in ProjectA.csproj
```

## Thinking

The problem is that **AI agents are helpful by default**. If the Migrator Agent can run a build to check its work, it will. This seems reasonable! But in a multi-agent pipeline, each agent operating outside its scope creates unpredictable state for the next agent.

We told the Migrator: "Your job is to modify project files." That's what it does — plus everything else it thinks might help.

## Solution

**Explicit prohibitions**. Not just "your job is X" but also "you are PROHIBITED from Y":

```markdown
## Your Role
Modify .csproj files to add multi-target framework support.

## You Are PROHIBITED From
- Running `build`, `quickbuild`, or `msbuild` commands
- Creating code files (.cs)
- Modifying any file outside the target .csproj
- Running any verification steps — that is the Build Agent's job
```

We also set **turn limits** per agent to prevent infinite loops:

```yaml
migrator_agent:
  max_turns: 60   # enough for complex projects, but has a ceiling
build_agent:
  max_turns: 80   # build-fix cycles need more turns
integration_agent:
  max_turns: 30   # simple ADO operations
```

Without turn limits, an agent in an error-fix loop will consume the entire context window and stop functioning — but it won't stop itself.

**The rules**:
1. In multi-agent systems, "you do X" is half the instruction. "You do NOT do Y" is the other half.
2. Without explicit prohibitions, agents expand their scope.
3. Without turn limits, agents in error loops consume infinite context.
