from abc import ABC, abstractmethod
import music21
import beat, chord
import typing
import data
import random
class Melody(ABC):
    @abstractmethod
    def generate_melody(self, beat, chord) -> music21.stream.Measure | music21.stream.Part:
        return NotImplemented

class CommonMelody(Melody):
    def __init__(self, beat:list[music21.duration.Duration], chord:list[music21.chord.Chord], tone):
        #chord had duration
        self.__genaral_middle = [4,4,3,2,1]
        self.__beat = beat
        self.__chord = chord
        self.tone = tone
        #[F3~F5]
    def get_note(self, last_note:music21.note.Note, dur:float, pitch:typing.Iterable[music21.pitch.Pitch]) -> music21.note.Note:
        chord = [p.midi%12 for p in pitch]
        F3 = 53
        F5 = 77
        sz = F5-F3+1
        # print(sz)
        prolist = [1]*(sz)
        chordfactor = [1]*(sz)
        for i in range(sz):
            dis = abs(last_note.pitch.midi-F3-i)
            if dis > 3:
                prolist[i] = 1
            else:
                prolist[i] = self.__genaral_middle[dis]
        for i in range(F3, F5+1):
            if i%12 in [data.NOTE_NUMBER_CONV[x]-12 for x in data.NATURAL_SCALE[self.tone]]:
                if i%12 in chord:
                    for j in range(-3, 3 +1):#-2~2
                        if i+j-F3 >= 0 and i + j-F3 < (sz): #edge
                            chordfactor[i+j-F3] = max(chordfactor[i+j-F3], 4-abs(j)) 
            else:
                chordfactor[i-F3] = 0
                        #replace 1 2 3 4 3 2 1to [i-3 i-2 i-1 i i+1 i+2 i+3](maxmum)
        
        pro = [0]*(sz)
        # print(f'{last_note},{last_note.quarterLength} {dur} {chord}')
        # print(prolist)
        # print(chordfactor)
        cnt = 0
        for i in range(sz):
            pro[i] = prolist[i] ** (2 if last_note.duration.quarterLength + dur <= 0.75 else 1) * chordfactor[i]
        # print(pro)
        return music21.note.Note(midi = data.weight_random_valuable(pro)+F3, quarterLength = dur)
    def generate_melody(self) -> list[music21.note.Note]:
        part_melody = []
        pitch = -1
        while pitch == -1 or pitch%12 not in [data.NOTE_NUMBER_CONV[x]-12 for x in data.NATURAL_SCALE[self.tone]]:
            pitch = random.randint(53,77)
        last_note = music21.note.Note(midi = pitch, quarterLength = 4)
        offset = 0
        now_chord = 0
        chord_duration = self.__chord[0].quarterLength
        for bt in self.__beat:
            n = self.get_note(last_note,bt.quarterLength, self.__chord[now_chord].pitches)
            part_melody.append(n)
            last_note = n
            offset += bt.quarterLength
            if offset >= chord_duration:
                now_chord += 1
                if now_chord < len(self.__chord):
                    chord_duration += self.__chord[now_chord].quarterLength
        """
        use measure
        """
        return part_melody