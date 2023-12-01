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
    def generate_bass(self, instrument: music21.instrument.BassDrum) -> music21.stream.Measure | music21.stream.Part:
        return NotImplemented

    @abstractmethod
    def generate_hihat(self, instrument: music21.instrument.BassDrum) -> music21.stream.Measure | music21.stream.Part:
        return NotImplemented

    @abstractmethod
    def generate_snare(self, instrument: music21.instrument.BassDrum) -> music21.stream.Measure | music21.stream.Part:
        return NotImplemented
