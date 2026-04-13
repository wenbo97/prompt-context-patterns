# Chapter 9: AI Reviews AI's Work

## Problem

The batch migration now produces hundreds of pull requests. Human reviewers can't keep up. Worse, some merged PRs had a subtle flaw: they successfully added .NET Core support but **accidentally broke the existing .NET Framework build path**.

```xml
<!-- Before migration: works for .NET Framework -->
<PackageReference Include="Legacy.Auth" Version="2.1.0" />

<!-- After AI migration: added .NET Core, but... -->
<PackageReference Include="Legacy.Auth" Version="2.1.0" 
                  Condition="'$(TargetFramework)' == 'net8.0'" />
<!-- Oops — .NET Framework path lost the package entirely -->
```

The AI focused on "make .NET Core work" and forgot "don't break .NET Framework."

## Thinking

We can't hire 10x more reviewers. But we can have **AI review AI's work** — with a different mindset. The migration AI thinks "make it work." The review AI thinks "what could this break?"

The key insight: review prompts should focus on **damage detection**, not correctness validation. We don't ask "is this migration perfect?" We ask "does the original framework still build?"

## Solution

Built a review skill with a **"Do No Harm" checklist**:

```markdown
## Review Checklist

For every modified .csproj:
  ☐ Does every PackageReference still apply to the original framework?
    BLOCKER if: a package's Condition excludes the original framework
    
  ☐ Are all <Compile Include> items preserved?
    BLOCKER if: any explicit source file reference was removed
    
  ☐ Do new Condition attributes use != (exclude) not == (include)?
    WARNING if: condition uses == which may miss future frameworks

For every modified .cs file:
  ☐ Is the #if block structured so the original framework path is the default?
    BLOCKER if: original code is in the #else branch (breaks if flag not set)
```

Output is structured verdicts, not prose:

```json
{
  "verdict": "BLOCKER",
  "file": "src/Auth/Auth.csproj",
  "rule": "PackageReference scope narrowed",
  "detail": "Legacy.Auth now only applies to net8.0. Framework build will lose this dependency.",
  "suggested_fix": "Remove the Condition or add a second reference for the original framework."
}
```

**The rules**:
1. When AI generates code at scale, you need AI-powered review at scale.
2. Review prompts should ask "what could this break?" not "is this correct?"
3. Structured verdicts (BLOCKER/WARNING/CORRECT) with specific rules beat prose reviews.
