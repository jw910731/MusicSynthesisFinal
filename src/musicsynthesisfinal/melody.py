from abc import ABC, abstractmethod
import music21


class Melody(ABC):
    @abstractmethod
    def __init__(self):
        self.__melody_List = []
        self.__genaral_middle = [4,4,3,2,1]
        self.__last_note = -1
    @abstractmethod
    def get_note(self):
        pass
    def generate_melody(self, beat) -> music21.stream.Measure | music21.stream.Part:
        priority_note = []
        """
        use measure
        """
        return NotImplemented
