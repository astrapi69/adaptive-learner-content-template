# Getting started — your first lesson in 10 minutes

This walkthrough takes you from zero to a validated lesson. You'll copy a
template, edit it, register it, and run the validator.

For the full field reference, see [LESSON-FORMAT.md](LESSON-FORMAT.md).

## Before you start

You need:

- **Git** and a **GitHub account**.
- **Python 3** with PyYAML (`pip install pyyaml`) to run the validator.
- A text editor.

### Start your own content repository

Create your repository from this template — **“Use this template” → Create
a new repository** (not *Fork*), then clone your new repo:

> <https://github.com/astrapi69/adaptive-learner-content-template> → **Use
> this template**. You get a fresh, independent repository (no fork
> relationship, no inherited history).

Everything you need ships in the copy: the domain **templates** under
[`templates/`](../templates/), one small **example set** under
[`sets/en/es-a1/`](../sets/en/es-a1/), the validator, and CI.

## 1. Copy a template (1 min)

Pick the template for your domain and copy it into a set's `lessons/` folder:

```bash
mkdir -p sets/en/my-set/lessons
cp templates/language/lesson.json sets/en/my-set/lessons/01-greetings.json
```

(There are also `templates/knowledge/` and `templates/programming/` templates.)

## 2. Edit the lesson (5 min)

Open `sets/en/my-set/lessons/01-greetings.json` and change:

- **`id`** → `01-greetings` (match the filename, kebab-case).
- **`title`**, **`description`**, **`target_language`** / **`source_language`**.
- **`cards`** → your words/terms. Keep ids unique and kebab-case.
- **`steps`** → at least one **theory** step and **five** exercises across at
  least two of the five types (matching, free_text, cloze, word_tiles,
  picture_choice).

Keep these or the validator will complain:

- `free_text` needs **≥ 2 accepts** and at least one **distractor**.
- `matching` needs **≥ 3 pairs**.
- `picture_choice` needs **distractors** and exactly one `is_correct: "true"`.

## 3. Register the lesson (2 min)

Create `sets/en/my-set/manifest.yaml`:

```yaml
schema_version: '1.3'
name: My Set
sets:
  - id: my-set-from-en
    title: My Set
    target_language: es
    source_language: en
    level: A1
    path: sets/en/my-set
    version: '1.0.0'
    lesson_count: 1
    domain: language
    description: >-
      My first set.
metadata:
  author: your-handle
  license: CC-BY-SA-4.0
  lessons:
    - 01-greetings.json
```

Then add the **same set block** to the root `manifest.yaml` under `sets:`.

## 4. Validate (1 min)

```bash
python scripts/validate_content.py
```

You want:

```
All N set(s) passed validation.
```

If it fails, the message names the lesson and the rule (e.g.
`free_text '…' needs distractors`). Fix and re-run.

## 5. Use your lessons

Two ways to publish:

- **In the app:** connect your repository under **Settings → Content**
  (*Einstellungen → Inhalte*). The app reads your root `manifest.yaml`.
- **Contribute back:** open a pull request to
  <https://github.com/astrapi69/adaptive-learner-content>. Keep
  `validate_content.py` green and update the README table + totals.

## Next steps

- Read the shipped example lesson:
  [`sets/en/es-a1/lessons/01-example.json`](../sets/en/es-a1/lessons/01-example.json)
  (theory + the common exercise types, kept minimal).
- Skim [LESSON-FORMAT.md](LESSON-FORMAT.md) for every field and option; the
  canonical, test-validated reference is the engine's
  [`docs/lesson-format.md`](https://github.com/astrapi69/learn-content-engine/blob/main/docs/lesson-format.md).
- Generate drafts with AI (optional): `python3 scripts/generate_exercises.py --help`.
