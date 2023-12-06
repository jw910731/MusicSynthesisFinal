import random
import typing

import music21

import beat
import chord
import melody
import data


class PopBeat(beat.Beat):
    def __init__(self):
        pass

    def __get_random_beat(self):
        pass

    def generate_beat(self, n) -> list[music21.duration.Duration]:
        pass

    def get_bpm(self):
        return self.bpm

    def generate_bass(self):
        pass

    def generate_hihat(self):
        pass

    def generate_snare(self):
        pass


class PopChord(chord.Chord):
    AVAILABLE_PROGRESSION = [
        ["I", "V", "vi", "iii", "IV", "I", "IV", "V"],
        ["I", "V", "vi", "VI"],
        ["vi", "VI", "I", "V"],
        ['IV', "V", "iii", "vi"],
        ['IV', "V", "iii", "vi", "ii", "V", "I"],
    ]

    def __init__(self, tone) -> None:
        self.progressions = random.choice(self.AVAILABLE_PROGRESSION)
        self.pivot = 0
        self.tone = tone

    def generate_chord(self) -> music21.chord.Chord:
        chrd = music21.roman.RomanNumeral(self.progressions[self.pivot], self.tone)
        chrd.semiClosedPosition(forceOctave=3, inPlace=True)
        self.pivot = (self.pivot + 1) % len(self.progressions)
        return chrd


class PopMelody(melody.CommonMelody):
    def __init__(self, beat: list[music21.duration.Duration], chord: list[music21.chord.Chord], tone):
        super().__init__(beat, chord, tone)
        self.__general_middle = [12, 12, 4, 3, 1]

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
        ind_last = data.index(scale, prev_note.pitch, lambda x, y: x.isEnharmonic(y))
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
                if scale_pitch.isEnharmonic(chord_pitches):
                    for delta in range(-3, 3 + 1):
                        inner_idx = idx + delta
                        if 0 <= inner_idx < len(scale):
                            chord_factor[inner_idx] = max(chord_factor[inner_idx], 4 - abs(delta))
                break


class Pop:
    def __init__(self, tone):
        self.chord = PopChord(tone)
        self.beat = PopBeat()
        self.tone = tone

    def generate_music(self):
        part_chord = music21.stream.Part()
        part_chord.insert(0, music21.tempo.MetronomeMark(number=self.beat.get_bpm()))
        part_chord.insert(0, music21.key.Key(self.tone))
        part_melody = music21.stream.Part()
        part_melody.insert(0, music21.tempo.MetronomeMark(number=self.beat.get_bpm()))
        part_melody.insert(0, music21.key.Key(self.tone))
        ret = []
        for i in range(16):
            bt = self.beat.generate_beat(6)
            ch = self.chord.generate_chord_list(bt)
            mel = PopMelody(bt, ch, self.tone)
            for c in ch:
                part_chord.append(c)
            m = mel.generate_melody()
            for x in m:
                part_melody.append(x)
        ret.append(part_melody)
        ret.append(part_chord)
        return ret
