from abc import ABC, abstractmethod
import music21
class Chord(ABC):
    @abstractmethod
    def generate_chord(self)->music21.chord.Chord:
        return NotImplemented    