from abc import ABC, abstractmethod
import music21
import typing
from musicsynthesisfinal import utils 
import random


class Melody(ABC):
    @abstractmethod
    def generate_melody(self) -> music21.stream.Measure | music21.stream.Part:
        return NotImplemented


class CommonMelody(Melody):
    def __init__(self, beat: list[music21.duration.Duration], chord: list[music21.chord.Chord], tone):
        # chord had duration
        self.__general_middle = [4, 4, 3, 2, 1]
        self._beat = beat
        self._chord = chord
        self.tone = tone
        # [F3~F5]

    def get_note(self, prev_note: music21.note.Note, dur: float,
                 pitch: typing.Iterable[music21.pitch.Pitch]) -> music21.note.Note:
        # Get chord pitch class in equal temperament
        # chord_pitches = [p.midi % 12 for p in pitch]
        scale_obj = music21.scale.MajorScale(str.lower(self.tone)) if str.isupper(
            self.tone) else music21.scale.MinorScale(self.tone)
        scale = scale_obj.getPitches('f3', 'f5')
        sz = len(scale)
        prob_list = [1] * sz
        chord_factor = [1] * sz
        # Construct magic probability factor
        ind_last = utils.index(scale, prev_note.pitch, lambda x, y: x.isEnharmonic(y))
        if ind_last != -1:
            for i in range(len(scale)):
                dis = abs(ind_last - i)
                if dis > 3:
                    prob_list[i] = 1
                else:
                    prob_list[i] = self.__general_middle[dis]
        # TODO: Add explanation to this panda magic
        for idx, scale_pitch in enumerate(scale):
            # Iterate through all pitch in scale
            for chord_pitches in pitch:
                # if the pitch matches the chord -> do magic
                if scale_pitch.pitchClass == chord_pitches.pitchClass:
                    for delta in range(-3, 3 + 1):
                        inner_idx = idx + delta
                        if 0 <= inner_idx < len(scale):
                            chord_factor[inner_idx] = max(chord_factor[inner_idx], 4 - abs(delta))

        prob = [0] * sz
        for i in range(sz):
            prob[i] = prob_list[i] ** (2 if prev_note.duration.quarterLength + dur <= 0.75 else 1) * chord_factor[i]
        ret_note = scale[utils.weight_random_valuable(prob)]
        return music21.note.Note(ret_note, quarterLength=dur)

    def generate_melody(self) -> list[music21.note.Note]:
        part_melody = []
        scale_obj = music21.scale.MajorScale(str.lower(self.tone)) if str.isupper(
            self.tone) else music21.scale.MinorScale(self.tone)
        scale = scale_obj.getPitches('f3', 'f5')
        pitch = random.choice(scale)
        last_note = music21.note.Note(pitch=pitch, quarterLength=4)
        offset = 0
        now_chord = 0
        chord_duration = self._chord[0].quarterLength

        for bt in self._beat:
            n = self.get_note(last_note, bt.quarterLength, self._chord[now_chord].pitches)
            part_melody.append(n)
            last_note = n
            offset += bt.quarterLength
            if offset >= chord_duration:
                now_chord += 1
                if now_chord < len(self._chord):
                    chord_duration += self._chord[now_chord].quarterLength
        return part_melody
