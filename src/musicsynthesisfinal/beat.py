from abc import ABC, abstractmethod
import music21
class Beat(ABC):
    @abstractmethod
    def generate_beat(self)->list[music21.duration.Duration]:
        return NotImplemented    
    @abstractmethod
    def generate_bass(self, instrument:music21.instrument.BassDrum)->music21.stream.Measure|music21.stream.Part:
        '''
        use measure
        '''
        return NotImplemented
    @abstractmethod
    def generate_hihat(self, instrument:music21.instrument.BassDrum)->music21.stream.Measure|music21.stream.Part:
        '''
        use measure
        '''
        return NotImplemented
    @abstractmethod
    def generate_snare(self, instrument:music21.instrument.BassDrum)->music21.stream.Measure|music21.stream.Part:
        '''
        use measure
        '''
        return NotImplemented
