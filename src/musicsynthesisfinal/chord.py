import copy
from abc import ABC, abstractmethod
import music21


def limit_inversion(chord: music21.chord.Chord, octave=3) -> music21.chord.Chord:
    """
    Args:
        chord: Input chord
        octave: The desire octave to squash

    Returns:
        A inversion chord that all note are fit in the octave.
        If the operation fails, then it best effort squash the note into the octave
    """

    def check(_ch: music21.chord.Chord):
        for p in _ch.pitches:
            if p.octave != octave:
                return False
        return True

    ch = copy.deepcopy(chord)
    inv = ch.inversion()  # keep the original inversion
    for i in range(len(chord)):
        ch.inversion(i)
        ch.semiClosedPosition(forceOctave=octave, inPlace=True)
        if check(ch):
            return ch
    ch.inversion(inv)
    return ch


class Chord(ABC):
    @abstractmethod
    def generate_chord(self) -> music21.chord.Chord:
        return NotImplemented
