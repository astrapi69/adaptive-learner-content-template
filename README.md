# adaptive-learner-content-template

A **GitHub template** for building your own [Adaptive Learner](https://github.com/astrapi69/adaptive-learner)
content: a Git repository of plain lesson files that the app loads
directly and no vendor can lock away.

> Click **“Use this template” → Create a new repository** (not *Fork*) to
> get a fresh, independent copy under your own account, then clone it.

This template is the clean scaffold — schema, validator, CI, authoring
templates, an AI generator, and **one** small example set. It ships **no**
real content: you replace the example with your own.

## What's inside

- `manifest.yaml` — the root manifest listing your sets (one example set to start).
- `sets/en/es-a1/` — one minimal, valid example lesson + its set manifest.
- `schema/` — the pinned [`learn-content-engine`](https://github.com/astrapi69/learn-content-engine)
  schema mirror + `engine-version.txt` (currently `0.4.0`). This is what
  your content is validated against — independent of the app.
- `templates/` — starting-point lessons per domain (language / programming / knowledge).
- `scripts/validate_content.py` — the local validator.
- `scripts/generate_exercises.py` — an optional BYOK AI exercise generator.
- `generated/` — staging area for AI drafts (never shipped directly).
- `.github/workflows/` — CI that validates every push/PR against the pinned engine.
- `docs/` — [GETTING-STARTED.md](docs/GETTING-STARTED.md) and a local
  [LESSON-FORMAT.md](docs/LESSON-FORMAT.md). The **canonical, test-validated**
  format reference is the engine's
  [`docs/lesson-format.md`](https://github.com/astrapi69/learn-content-engine/blob/main/docs/lesson-format.md).

## Quick start

You only need `make` and `python3`. The first `make validate` sets up a
local environment for you (no manual `pip`, no virtualenv, no Poetry):

```bash
# 1. Use this template -> your own repo -> clone it
git clone https://github.com/<you>/<your-content-repo>.git
cd <your-content-repo>

# 2. Validate the example set. First run creates .venv and installs deps;
#    later runs reuse it. Exit 0 == all sets pass.
make validate

# 3. Replace the example with your own lesson, then re-run make validate + commit.
```

No `make` (e.g. Windows without WSL)? Two options: run the validator in a
virtualenv yourself —

```bash
python3 -m venv .venv && . .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python3 scripts/validate_content.py
```

— or just commit and let the GitHub Actions CI validate (it runs the same
checks). Installing the deps globally with a bare `pip install` fails on
modern Debian/Ubuntu/macOS (PEP 668, "externally-managed-environment");
the virtualenv above is why.

Full walkthrough: [docs/GETTING-STARTED.md](docs/GETTING-STARTED.md).

## Generate exercises with AI (optional)

`scripts/generate_exercises.py` turns a topic into a full **language**
lesson with a BYOK model (Anthropic / OpenAI / Gemini) and gates every
draft through the validator before writing it into the `generated/`
staging folder. It is language-focused (target and source differ). For a
**knowledge set** (material written in the same language it teaches,
source == target), the generator is not the right tool; hand-author from
[`templates/knowledge/`](templates/knowledge/) instead.

First set your provider key. It is read from the environment (BYOK) and
never committed:

```bash
export ANTHROPIC_API_KEY="sk-..."   # or OPENAI_API_KEY / GEMINI_API_KEY (Gemini also accepts GOOGLE_API_KEY)
```

**Recommended (via make; reuses the local environment `make validate` set up):**

```bash
make generate ARGS="--topic 'Ordering food in a café' --target-lang fr --source-lang en --level A1 --set-id fr-a1"
```

**Direct (fallback; run it inside the venv from the Quick start):**

```bash
python3 scripts/generate_exercises.py \
  --topic "Ordering food in a café" \
  --target-lang fr --source-lang en --level A1 --set-id fr-a1
```

### Options

| Flag | Default | Meaning |
|------|---------|---------|
| `--topic` | (required) | What the lesson is about. |
| `--target-lang` | (required) | The language the learner studies (BCP-47, e.g. `fr`). |
| `--source-lang` | (required) | The explanation language (BCP-47, e.g. `en`). Must differ from the target. |
| `--level` | `A1` | CEFR level. |
| `--count` | `6` | Exercises to request. The effective minimum is **5** (a smaller value is treated as 5, and the quality gate requires at least 5). |
| `--set-id` | `generated-set` | Staging subfolder under `generated/`. |
| `--provider` | `anthropic` | `anthropic` \| `openai` \| `gemini`. Or set `AL_GEN_PROVIDER`. |
| `--model` | provider default | Override the model (`claude-sonnet-4-5` / `gpt-4o` / `gemini-2.5-flash`). |
| `--retries` | `3` | Extra attempts when a draft fails validation before it is discarded. |
| `--out` | `generated` | Staging directory. |

### What happens, and what you still owe

The script pins the exact lesson-schema JSON in the prompt, parses the
model's reply, and runs it through `validate_content.py`. If validation
fails, the errors go back to the model and it retries (up to `--retries`);
a draft that never validates is discarded, not written. A valid draft
lands in `generated/<set-id>/`, never directly in `sets/`.

Two gates remain after generation, neither of them automatic:

1. **Engine semantic gate** (cloze `___` markers equal the blanks,
   `card_ids` integrity, multiselect disjointness). It runs when the
   pinned `learn-content-engine` is installed, otherwise it is deferred to
   CI. The plain validator does not cover it.
2. **Native-speaker review** for a language you do not speak natively. No
   validator catches an unnatural phrasing or a wrong romanization.
   Machine-generated, then human-verified, is the only trustworthy order.

When a draft is good, move it from `generated/` into your set under
`sets/<source>/<target>-<level>/lessons/`, register it in the set
manifest, and re-run `make validate`.

## How it stays current

Your content is validated against the **pinned** engine version in
`schema/engine-version.txt` on every push and pull request (structural +
semantic + drift gates in `.github/workflows/`). A green CI means your
content is valid for every consumer of that engine release. When the
engine is bumped, it reaches this repository the same way it reaches the
rest of the chain: a deliberate pin-bump PR that the drift gate guards.

Background and prompt recipes: the blog post *Build Your Own Lessons for
Adaptive Learner*. Licensed MIT (see [LICENSE](LICENSE)); your authored
content may carry its own license via each set manifest's `metadata.license`.
