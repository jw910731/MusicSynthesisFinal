import beat, chord, melody
import music21
import random   
class ClassicalBeat(beat.Beat):
    PROBABILITY = {'Allegro' : [2,12,45,30, 9,2], 
                   'Moderato' : [2,14,34,34, 14,2], 
                   'Andante' : [2,10,45,32, 9,2]}
    BPMRANGE = {'Allegro' : (120,168), 
                'Moderato' : (90, 115), 
                'Andante' : (66, 76)}
    def __init__(self):
        self.speed_type, self.prefix = random.choice(list(self.PROBABILITY.items()))
        for i in range(1,len(self.prefix)):
            self.prefix[i] += self.prefix[i-1]
        self.bpm = random.randint(*self.BPMRANGE[self.speed_type])
    def __get_random_beat(self):
        r = random.randint(1,100)
        a = 3
        for p in self.prefix:
            if r <= p:
                return 2 ** (-a)
            a -= 1
        return 2 ** (-1)
    def generate_beat(self, n) -> list[music21.duration.Duration]:
        now = 0
        ret = []
        while now<n:
            choiceBeat = self.__get_random_beat();
            if now+choiceBeat > n:
                choiceBeat = n-now
            ret.append(music21.duration.Duration(choiceBeat))
            now += choiceBeat
        return ret
    def get_bpm(self):
        return self.bpm
    def generate_bass(self):
        pass
    def generate_hihat(self):
        pass
    def generate_snare(self):
        pass

class ClassicalChord(chord.Chord):
    def generate_chord(self) -> music21.chord.Chord:
        pass


class ClassicalMelody(melody.Melody):
    def generate_melody(self) -> music21.stream.Measure:
        pass


class Classical:
    def __init__(self):
        self.melody = ClassicalMelody
        self.chord = ClassicalChord
        self.beat = ClassicalBeat
