from abc import ABC, abstractmethod
import music21
import random


class NoteFactory(ABC):
    """
    This is the base class of note factories which can generate notes from scale or other method
    """

    @abstractmethod
    def get_notes(self) -> music21.stream.base.Score | music21.stream.base.Part | music21.stream.base.Opus:
        return NotImplemented

    def __iter__(self):
        return self

    def __next__(self):
        return self.get_notes()


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

    def get_notes(self) -> music21.note.Note:
        ret = music21.stream.base.Part()
        for _ in range(8):
            noteStr = random.choice(
                self.SCALE) + str(random.randint(self._lower_bound, self._upper_bound))
            ret.append(music21.note.Note(noteStr))
        return ret
