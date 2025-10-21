from __future__ import annotations
import json
import random
from dataclasses import dataclass
from datetime import datetime, timedelta
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown

from .ideas import IDEA_BANK, VIBES, DIETARY, ACCESS, BUDGETS, DEFAULT_CITY
from .scheduler import propose_slots

console = Console()

@dataclass
class Plan:
    vibe: str
    minutes: int
    budget: str
    diet: str
    access: str
    city: str
    idea: str
    slot: str | None = None

    def title(self) -> str:
        return f"{self.vibe.title()} date · {self.minutes} min · {self.city}"

    def invite(self) -> str:
        core = self.idea.split(\" + \")[0] if \" + \" in self.idea else self.idea
        when = f\" on {self.slot}\" if self.slot else \" soon\"
        return f\"Hey, would you be up for {core.lower()} {when}? We can keep it simple and bail anytime if it's not the vibe.\"

    def checklist(self, weather: str | None = None) -> list[str]:
        base = [\"Wallet/transport\",\"Phone charged\",\"Breath mint\",\"Tissues\",\"Small umbrella\"]  # Budapest realities
        if \"walk\" in self.idea.lower():
            base.append(\"Comfortable shoes\")
        if weather and weather.lower() in (\"cool\",\"cold\"):
            base.append(\"Light jacket or scarf\")
        if self.vibe in (\"adventurous\",\"playful\"):
            base.append(\"Water bottle\")
        return base

def pick_idea(vibe: str, budget: str) -> str:
    bag = IDEA_BANK.get(vibe, [])
    if not bag:
        return \"Coffee + short walk\"
    # naive budget filter: keep all for simplicity, shuffle
    random.seed()
    return random.choice(bag)

def render_plan(plan: Plan) -> None:
    console.rule(f\"[bold]{plan.title()}[/bold]\")
    t = Table(show_header=True, header_style=\"bold\")
    t.add_column(\"Field\", style=\"dim\")
    t.add_column(\"Value\")
    t.add_row(\"Vibe\", plan.vibe)
    t.add_row(\"Idea\", plan.idea)
    t.add_row(\"Duration\", f\"{plan.minutes} min\")
    t.add_row(\"Budget\", plan.budget)
    t.add_row(\"Dietary\", plan.diet)
    t.add_row(\"Accessibility\", plan.access)
    t.add_row(\"City\", plan.city)
    if plan.slot:
        t.add_row(\"Proposed time\", plan.slot)
    console.print(t)
    console.print(Panel(plan.invite(), title=\"Invite message\", border_style=\"green\"))
    cl = \"\\n\".join(f\"• {x}\" for x in plan.checklist())
    console.print(Panel(cl, title=\"Checklist\", border_style=\"cyan\"))

def interactive_prompts(default_city: str) -> tuple[str,int,str,str,str,str | None]:
    try:
        import questionary  # type: ignore
    except Exception:
        # Fallback to click prompts
        vibe = click.prompt(\"Vibe\", type=click.Choice(VIBES), default=\"cozy\")
        minutes = click.prompt(\"Minutes\", type=int, default=75)
        budget = click.prompt(\"Budget\", type=click.Choice(BUDGETS), default=\"mid\")
        diet = click.prompt(\"Dietary\", type=click.Choice(DIETARY), default=\"No preference\")
        access = click.prompt(\"Accessibility\", type=click.Choice(ACCESS), default=\"Short walking\")
        city = click.prompt(\"City\", type=str, default=default_city)
        return vibe, minutes, budget, diet, access, city

    vibe = questionary.select(\"Pick a vibe\", choices=VIBES, default=\"cozy\").ask()
    minutes = int(questionary.select(\"Duration (min)\", choices=[\"45\",\"60\",\"75\",\"90\",\"120\"], default=\"75\").ask())
    budget = questionary.select(\"Budget\", choices=BUDGETS, default=\"mid\").ask()
    diet = questionary.select(\"Dietary\", choices=DIETARY, default=\"No preference\").ask()
    access = questionary.select(\"Accessibility\", choices=ACCESS, default=\"Short walking\").ask()
    city = questionary.text(\"City\", default=default_city).ask()
    return str(vibe), int(minutes), str(budget), str(diet), str(access), str(city)

@click.group(help=\"Interactive date-night utilities. Python-only. Use --help on any command.\")
def cli() -> None:
    pass

@cli.command()
@click.option(\"--vibe\", type=click.Choice(VIBES), help=\"Vibe: cozy/playful/thoughtful/adventurous\") 
@click.option(\"--minutes\", type=int, help=\"Duration in minutes\", default=75)
@click.option(\"--budget\", type=click.Choice(BUDGETS), default=\"mid\")
@click.option(\"--diet\", type=click.Choice(DIETARY), default=\"No preference\")
@click.option(\"--access\", type=click.Choice(ACCESS), default=\"Short walking\")
@click.option(\"--city\", type=str, default=DEFAULT_CITY)
@click.option(\"--autoslot/--no-autoslot\", default=True, help=\"Propose time suggestions automatically\") 
def plan(vibe: str | None, minutes: int, budget: str, diet: str, access: str, city: str, autoslot: bool) -> None:
    \"\"\"Create a plan interactively or via flags.\"\"\"
    if not vibe:
        vibe, minutes, budget, diet, access, city = interactive_prompts(city)
    idea = pick_idea(vibe, budget)
    slot = propose_slots(minutes=minutes)[0] if autoslot else None
    p = Plan(vibe=vibe, minutes=minutes, budget=budget, diet=diet, access=access, city=city, idea=idea, slot=slot)
    render_plan(p)

@cli.command()
@click.option(\"--weather\", type=click.Choice([\"warm\",\"cool\",\"cold\",\"rainy\",\"windy\"]), default=\"cool\")
def packlist(weather: str) -> None:
    \"\"\"Print a general-purpose packing checklist based on weather.\"\"\"
    sample = Plan(vibe=\"cozy\", minutes=75, budget=\"mid\", diet=\"No preference\", access=\"Short walking\", city=DEFAULT_CITY, idea=\"Coffee + short walk\")
    items = sample.checklist(weather)
    console.print(Panel(\"\\n\".join(f\"• {i}\" for i in items), title=f\"Checklist for {weather}\", border_style=\"cyan\"))

@cli.command()
@click.option(\"--plan\", required=True, help=\"Short description, e.g. 'cozy: café + walk @ 75m'\")
@click.option(\"--slot\", default=None, help=\"Optional time window to include\") 
def message(plan: str, slot: str | None) -> None:
    \"\"\"Generate a polite, low-pressure invite message.\"\"\"
    idea = plan.split(\":\", 1)[-1].strip() if \":\" in plan else plan
    p = Plan(vibe=\"cozy\", minutes=75, budget=\"mid\", diet=\"No preference\", access=\"Short walking\", city=DEFAULT_CITY, idea=idea, slot=slot)
    console.print(Panel(p.invite(), title=\"Invite message\", border_style=\"green\"))

@cli.command()
@click.option(\"--minutes\", type=int, default=75, help=\"Desired date length\") 
def slots(minutes: int) -> None:
    \"\"\"Propose five candidate time windows over the next 10 days.\"\"\"
    rows = propose_slots(minutes=minutes)
    table = Table(title=f\"Suggested {minutes}‑minute slots\") 
    table.add_column(\"#\", justify=\"right\"); table.add_column(\"Window\") 
    for i, s in enumerate(rows, 1):
        table.add_row(str(i), s)
    console.print(table)

if __name__ == \"__main__\":
    cli()
