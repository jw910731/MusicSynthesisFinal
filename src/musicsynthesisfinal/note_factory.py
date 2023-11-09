from abc import ABC, abstractmethod
import music21
import random


class NoteFactory(ABC):
    """
    This is the base class of note factories which can generate notes from scale or other method
    """

    @abstractmethod
    def get_note(self) -> music21.note.Note:
        return NotImplemented

    def __iter__(self):
        return self

    def __next__(self):
        return self.getNote()


class RandomNoteFactory(NoteFactory):
    """
    A simple implementation of NoteFactory which generate note randomly
    """
    SCALE = ['C', "C#", "D", "D#", "E", "F", "G", "G#", "A", "A#", "B"]

    def __init__(self, lower_bound, upper_bound):
        """
        Lower bound and upper bound represent the lowest and highest possible octave can this factory generate
        """
        self._lower_bound = lower_bound
        self._upper_bound = upper_bound

    def get_note(self) -> music21.note.Note:
        noteStr = random.choice(
            self.SCALE) + str(random.randint(self._lower_bound, self._upper_bound))
        return music21.note.Note(noteStr)
