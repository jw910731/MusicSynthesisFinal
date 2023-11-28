from abc import ABC, abstractmethod
import music21
class Melody(ABC):
    @abstractmethod
    def generate_melody(self)->music21.stream.Measure|music21.stream.Part:
        '''
        use measure
        '''
        return NotImplemented