import builtins
import logging
from typing import List

import pytest

from funventures.game import AdventureEngine, AdventureOutcome, play


class StubRandom:
    def __init__(self) -> None:
        self.selections: List[str] = []

    def choice(self, options):
        self.selections.append(options[0])
        return options[0]


def test_adventure_outcome_format():
    outcome = AdventureOutcome("Treasure", "Sparkling gems await.")
    formatted = outcome.format()
    assert "*** Treasure ***" in formatted
    assert "Sparkling gems await." in formatted


def test_available_choices_are_sorted():
    engine = AdventureEngine(rng=StubRandom())
    assert engine.available_choices() == [1, 2, 3]


def test_explore_combines_outcome_with_twist():
    rng = StubRandom()
    engine = AdventureEngine(rng=rng)
    result = engine.explore(2)
    assert result.title == "Bubblegum Bay"
    assert "bubble boats" in result.description
    assert rng.selections, "Expected the stub random to record a selection."


def test_explore_rejects_invalid_choice():
    engine = AdventureEngine(rng=StubRandom())
    with pytest.raises(ValueError):
        engine.explore(9)


def test_play_handles_non_numeric_input(monkeypatch, capsys):
    monkeypatch.setattr(builtins, "input", lambda _: "banana")
    play()
    captured = capsys.readouterr()
    assert "Welcome to the Whimsy Door Adventure!" in captured.out
    assert "Oops! That wasn't a number" in captured.out


def test_play_reports_invalid_door(monkeypatch, capsys):
    class StubEngine:
        def __init__(self):
            self._choices = [1, 2, 3]

        def available_choices(self):
            return self._choices

        def explore(self, choice):
            raise ValueError("nope")

    monkeypatch.setattr("funventures.game.AdventureEngine", StubEngine)
    monkeypatch.setattr(builtins, "input", lambda _: "5")

    # Ensure logging does not interfere with test output
    logging.getLogger("funventures.game").handlers.clear()

    play()
    captured = capsys.readouterr()
    assert "map gremlin" in captured.out


def test_play_successful_path(monkeypatch, capsys):
    class HappyEngine:
        def __init__(self):
            self._choices = [1, 2, 3]

        def available_choices(self):
            return self._choices

        def explore(self, choice):
            assert choice == 2
            return AdventureOutcome("Joyful", "A parade of penguins applauds you.")

    monkeypatch.setattr("funventures.game.AdventureEngine", HappyEngine)
    monkeypatch.setattr(builtins, "input", lambda _: "2")

    play()
    captured = capsys.readouterr()
    assert "Joyful" in captured.out
    assert "penguins applauds" in captured.out
