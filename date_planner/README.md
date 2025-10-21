# Date Planner CLI (Python-only)

A small, interactive command‑line toolkit to plan low-pressure date nights based on vibe, budget, time, and dietary/accessibility preferences.

## Features
- Interactive prompts (with `questionary`) or non-interactive flags (with `click`)
- Smart suggestions from curated idea banks
- Generates a concrete itinerary with timings, venues (placeholder names), and a polite invite message
- Prints a packing/checklist and conversation starters
- Optional schedule helper to propose time windows based on your week

## Quickstart
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Interactive
python -m date_planner plan

# Non-interactive
python -m date_planner plan --vibe cozy --minutes 75 --budget mid --diet "No preference" --access "Short walking" --city "Budapest"

# Generate only an invite message
python -m date_planner message --plan 'cozy: café + short walk @ 75m'

# Show packing list
python -m date_planner packlist --weather cool
```
