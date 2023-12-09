from abc import ABC, abstractmethod
import music21


class Beat(ABC): 
    """
    Beat is an abstract base class that defines the interface for generating drum beats and note durations.
    """
    @abstractmethod
    def generate_beat(self, n) -> list[music21.duration.Duration]:
        return NotImplemented

    @abstractmethod
    def generate_bass(self) -> list[music21.note.Note]:
        return NotImplemented

    @abstractmethod
    def generate_hihat(self) -> list[music21.note.Note]:
        return NotImplemented

    @abstractmethod
    def generate_snare(self) -> list[music21.note.Note]:
        return NotImplemented

    @abstractmethod
    def generate_clap(self) -> list[music21.note.Note]:
        return NotImplemented
