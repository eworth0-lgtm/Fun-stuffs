"""Interactive whimsical adventure game."""

from __future__ import annotations

import logging
import random
from dataclasses import dataclass
from typing import Dict, List, Sequence

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class AdventureOutcome:
    """Represents a possible outcome of the adventure."""

    title: str
    description: str

    def format(self) -> str:
        """Return a nicely formatted description for the player."""
        return f"\n*** {self.title} ***\n{self.description}\n"


class AdventureEngine:
    """Core logic for the fantasy micro-adventure."""

    _choices: Dict[int, AdventureOutcome]
    _twists: Sequence[str]

    def __init__(self, rng: random.Random | None = None) -> None:
        self.rng = rng or random.Random()
        self._choices = {
            1: AdventureOutcome(
                title="Marshmallow Mountain",
                description=(
                    "You scale a sugary summit, greeted by singing cocoa clouds "
                    "that sprinkle confetti snow."
                ),
            ),
            2: AdventureOutcome(
                title="Bubblegum Bay",
                description=(
                    "A fleet of bubble boats set sail, and you become captain of the "
                    "cheeriest chewing-crew afloat."
                ),
            ),
            3: AdventureOutcome(
                title="Starlight Arcade",
                description=(
                    "Nebula pinballs and comet skee-ball light up as you master every "
                    "game with cosmic style."
                ),
            ),
        }
        self._twists = [
            "A tiny dragon offers high-fives for every brave decision.",
            "You discover a portal leading to an encore adventure waiting tomorrow.",
            "Confetti fireworks spell out your name across the sky.",
            "A friendly robot DJ remixes your footsteps into a celebratory beat.",
        ]
        LOGGER.debug("AdventureEngine initialised with %d choices and %d twists", len(self._choices), len(self._twists))

    def available_choices(self) -> List[int]:
        """Return the list of available doors to explore."""
        choices = sorted(self._choices.keys())
        LOGGER.debug("Available choices requested: %%s", choices)
        return choices

    def explore(self, choice: int) -> AdventureOutcome:
        """Return the outcome for the selected choice."""
        LOGGER.info("Player selected door %s", choice)
        try:
            outcome = self._choices[choice]
        except KeyError as exc:
            LOGGER.warning("Invalid choice attempted: %s", choice)
            raise ValueError("Choice must be one of the available doors.") from exc

        twist = self.rng.choice(self._twists)
        LOGGER.debug("Random twist selected: %s", twist)

        combined_description = f"{outcome.description} {twist}"
        LOGGER.debug("Combined description generated for choice %s", choice)

        return AdventureOutcome(outcome.title, combined_description)


def play() -> None:
    """Run the interactive adventure via the CLI."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
    engine = AdventureEngine()

    print("Welcome to the Whimsy Door Adventure!")
    print("Choose a door to open and see what delightful surprise awaits you.")
    print("Doors available:", ", ".join(str(num) for num in engine.available_choices()))

    try:
        choice_str = input("Pick a door (1-3): ")
        choice = int(choice_str)
    except ValueError:
        LOGGER.error("Non-numeric input received: %s", choice_str, exc_info=True)
        print("Oops! That wasn't a number. Let's imagine you found a secret nap room instead.")
        return

    try:
        outcome = engine.explore(choice)
    except ValueError as exc:
        print("That door isn't on this corridor, but you do find a friendly map gremlin.")
        LOGGER.exception("Player chose an invalid door.")
        return

    print(outcome.format())
    print("Thanks for playing! Press play again for a fresh twist whenever you like.")
