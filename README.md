# log-report (fixed)

A small, self-contained **agent-evaluation task**: given a fixed Apache-style access log, the agent under test has to parse it and write a correct JSON summary report. It's built to the common "task.toml" pattern used by coding/terminal-agent benchmark harnesses — one instruction, one sandboxed environment, one reference solution, one automated verifier.

Declared task name (from `task.toml`): `dynamo/log-report`.

## What's in this repo

| Path | What it is |
|---|---|
| `instruction.md` | The exact prompt handed to the agent under test. |
| `environment/Dockerfile` | The container the agent runs in — Python 3.13-slim, pinned by image digest. Only `access.log` is shipped in; no solution or answer file ever reaches the agent. |
| `environment/access.log` | The fixed input fixture: 6 log lines, 3 unique client IPs, `/index.html` requested most often. |
| `solution/solve.py`, `solution/solve.sh` | A reference ("gold") solution that satisfies the task, for comparison against whatever an agent produces. |
| `tests/test_outputs.py` | The verifier — a pytest suite that checks the agent's `/app/report.json` against values independently known to be correct for this fixture (not derived from the agent's own output). |
| `tests/test.sh` | Runs the verifier, emits a CTRF-format test report, and writes a binary `reward.txt` (`1` pass / `0` fail) for a harness to consume. |
| `task.toml` | Machine-readable metadata: category, difficulty rationale, which model/agent this was validated against (`GPT-5.4` / `Terminus-2`), and resource/timeout limits for the environment, agent and verifier. |

## How it works

1. An agent is dropped into the `environment/Dockerfile` container with only `access.log` present, and given `instruction.md` as its task.
2. It must parse the log and write `/app/report.json` with exactly three fields: `total_requests`, `unique_ips`, `top_path`.
3. `tests/test_outputs.py` checks that file against the known-correct values for this fixture (`total_requests=6`, `unique_ips=3`, `top_path="/index.html"`), and `tests/test.sh` turns the result into a pass/fail reward a benchmark harness can score.

## Why this exists

Coding-agent benchmarks are built out of many small tasks like this one: cheap to run, with one unambiguous correct answer, each isolating a narrow skill (here: basic file I/O, a regex, and counting with `Counter`/`set`) so a harness can run the same fixture against many models or agents and compare results directly. This task was authored — and validated against GPT-5.4 running as the Terminus-2 agent — while exploring how these agent-eval tasks are put together.

## How you can use it

- **As a template** for writing your own agent-eval tasks — copy the `instruction.md` / `environment/` / `solution/` / `tests/` / `task.toml` structure and swap in a different problem.
- **As a smoke test** for a coding agent or harness you're building — point it at `environment/Dockerfile` + `instruction.md`, then grade its output with `tests/test_outputs.py`.
- **As a worked example** of the reference-solution + independent-verifier pattern for grading agent output, rather than trusting the agent's own claims of success.

## Running it locally

```bash
# Build the task's sandboxed environment image
docker build -t log-report-task ./environment

# Run the reference solution, then the verifier, inside it
docker run --rm \
  -v "$(pwd)/solution:/solution" \
  -v "$(pwd)/tests:/tests" \
  -v "$(pwd)/logs:/logs" \
  log-report-task bash -c "/solution/solve.sh && /tests/test.sh"
```

This writes `/app/report.json` inside the container and `logs/verifier/reward.txt` on the host (`1` means the verifier passed).
