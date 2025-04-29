from dataclasses import dataclass, field
from typing import List
import string

@dataclass
class HangmanGameState:
    word_to_guess: str
    guesses: List[str] = field(default_factory=list)
    incorrect_guesses: List[str] = field(default_factory=list)
    phase: str = "running"  # can be "running" or "finished"

    def __str__(self) -> str:
        return (
            f"Word to guess: {self.word_to_guess}\n"
            f"Guesses: {self.guesses}\n"
            f"Incorrect guesses: {self.incorrect_guesses}\n"
            f"Phase: {self.phase}"
        )

@dataclass
class GuessLetterAction:
    letter: str  # single uppercase letter

class Hangman:
    def __init__(self, initial_word: str):
        # Initialize game state inside __init__
        self._state = HangmanGameState(word_to_guess=initial_word.upper())

    def set_state(self, state: HangmanGameState) -> None:
        """
        Load a new game state.
        """
        self._state = state

    def get_state(self) -> HangmanGameState:
        """
        Return the current game state.
        """
        return self._state

    def print_state(self) -> None:
        """
        Print the current game state using HangmanGameState.__str__.
        """
        print(str(self._state))

    def get_list_action(self) -> List[GuessLetterAction]:
        """
        Return a list of GuessLetterAction for each unguessed letter.
        """
        used = set(self._state.guesses)
        return [GuessLetterAction(letter=ch) for ch in string.ascii_uppercase if ch not in used]

    def apply_action(self, action: GuessLetterAction) -> None:
        """
        Apply a guess action to the game state, updating guesses,
        incorrect_guesses, and phase if finished.
        Raise ValueError if letter was already guessed.
        """
        letter = action.letter.upper()
        if letter in self._state.guesses:
            raise ValueError(f"Letter '{letter}' has already been guessed.")

        # Record guess
        self._state.guesses.append(letter)

        # Check correctness
        if letter not in self._state.word_to_guess:
            self._state.incorrect_guesses.append(letter)

        # Determine if finished
        revealed = all(ch in self._state.guesses or not ch.isalpha() for ch in self._state.word_to_guess)
        if revealed or len(self._state.incorrect_guesses) >= 8:
            self._state.phase = "finished"

    def get_player_view(self) -> HangmanGameState:
        """
        Return a player view game state with masked word_to_guess.
        Correctly guessed letters shown; others as underscore.
        """
        masked = ''.join(
            ch if (not ch.isalpha()) or (ch in self._state.guesses) else '_'
            for ch in self._state.word_to_guess
        )
        return HangmanGameState(
            word_to_guess=masked,
            guesses=list(self._state.guesses),
            incorrect_guesses=list(self._state.incorrect_guesses),
            phase=self._state.phase
        )

    def play(self) -> None:
        """
        Start an interactive command-line game loop.
        """
        while self._state.phase == "running":
            view = self.get_player_view()
            print(view)
            guess = input("Guess a letter: ").strip().upper()
            if len(guess) != 1 or not guess.isalpha():
                print("Bitte einen einzelnen Buchstaben eingeben.")
                continue
            try:
                self.apply_action(GuessLetterAction(letter=guess))
            except ValueError as e:
                print(e)
            print()

        # Spiel beendet
        final = self.get_state()
        print(final)
        word = self._state.word_to_guess
        # Ursprüngliches Wort (unmaskiert) ausgeben
        original = word
        print()
        if all(ch in self._state.guesses or not ch.isalpha() for ch in original):
            print("Glückwunsch, du hast gewonnen!")
        else:
            print(f"Game over, du hast verloren. Das Wort war: {original}")

if __name__ == "__main__":
    secret = input("Wort zum Erraten eingeben: ").strip()
    game = Hangman(secret)
    game.play()
