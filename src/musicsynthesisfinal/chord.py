from abc import ABC, abstractmethod
import music21


class Chord(ABC):
    @abstractmethod
    def generate_chord(self) -> music21.chord.Chord:
        return NotImplemented

    def generate_chord_list(self, beat: list[music21.duration.Duration]) -> list[music21.chord.Chord]:
        dur = 0.0
        offset = 0.0
        ret = []
        for bt in [x.quarterLength for x in beat]:
            if dur.is_integer() and dur != 0:
                if dur > 4:
                    ret.append(self.generate_chord(4))
                    ret.append(self.generate_chord(dur - 4))
                else:
                    ret.append(self.generate_chord(dur))
                dur = 0
            offset += bt
            dur += bt
        ret.append(self.generate_chord(dur))
        return ret
