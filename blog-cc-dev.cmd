@ECHO OFF

@REM model series config
set ANTHROPIC_BASE_URL=http://localhost:4141
set ANTHROPIC_AUTH_TOKEN=dummy
set ANTHROPIC_MODEL=claude-opus-4-6[1m]
set ANTHROPIC_DEFAULT_SONNET_MODEL=claude-sonnet-4-6
set ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-haiku-4-5
set CLAUDE_CODE_SUBAGENT_MODEL=claude-opus-4-6[1m]
set DISABLE_NON_ESSENTIAL_MODEL_CALLS=1

@REM disable telemetry
set CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1
set CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1
set CLAUDE_CODE_ATTRIBUTION_HEADER=0
set CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1
set CLAUDE_CODE_ENABLE_TELEMETRY=0
set DISABLE_TELEMETRY=1
set DISABLE_ERROR_REPORTING=1

@REM set CLAUDE_CODE_NO_FLICKER=1
set CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1
@REM set CLAUDE_CODE_MAX_CONTEXT_LENGTH=168000
set CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=88
@REM max will easy to get request limitation reached for github copilot Endpoint service calling. Adjust to max if possible to maximize CC capabilities.
set CLAUDE_CODE_EFFORT_LEVEL=max
set CLAUDE_CODE_PERMISSION_MODEL=bypassPermissions
set ENABLE_TOOL_SEARCH=true
@REM Resolve real python.exe (skip WindowsApps stub)
set PYTHON_EXECUTABLE=
for /f "delims=" %%P in ('where python 2^>nul') do (
    if not defined PYTHON_EXECUTABLE (
        echo %%P | findstr /i /v "WindowsApps" >nul && set "PYTHON_EXECUTABLE=%%P"
    )
)
if not defined PYTHON_EXECUTABLE set "PYTHON_EXECUTABLE=python"

ECHO [Current Location] is %~dp0
ECHO .
pushd %~dp0

ECHO === Claude starting with Plugin: %~dp0 ===
ECHO === (Ctrl+C to stop Claude only) ===
ECHO Applying plugin CLAUDE.md, path is %~dp0CLAUDE.md
call claude --add-dir %~dp0 --permission-mode %CLAUDE_CODE_PERMISSION_MODEL% --dangerously-skip-permissions --model claude-opus-4-6[1m] --effort %CLAUDE_CODE_EFFORT_LEVEL%
