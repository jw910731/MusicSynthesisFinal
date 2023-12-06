import random
import typing
import copy

import music21

import beat
import chord
import melody
import data


class PopBeat(beat.Beat):
    def __init__(self):
        self.bpm = random.randint(90, 120)
        pass

    def __beat_recursive(self, size: float, part: float) -> list[int]:
        if size <= 0.25:
            return [size]
        if part == 6 and size == 2:
            if random.randint(1, 100) <= 10:
                return [size]
        if size <= 1 and random.random() <= (1 / (4 * size)) ** 0.5:
            return [size]
        return self.__beat_recursive(size / 2, part) + self.__beat_recursive(size / 2, part + size / 2)

    def generate_beat(self, n) -> list[music21.duration.Duration]:
        ret = []
        for i in range(0, n, 8):
            ls = self.__beat_recursive(8, 0)
            for x in ls:
                ret.append(music21.duration.Duration(x))
        return ret

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
        chrd.quarterLength = 4
        chrd.semiClosedPosition(forceOctave=3, inPlace=True)
        self.pivot = (self.pivot + 1) % len(self.progressions)
        return chrd

    def generate_chord_list(self, beat: list[music21.duration.Duration]) -> list[music21.chord.Chord]:
        ret = []
        cnt = 0
        for bt in beat:
            cnt += bt.quarterLength
        for i in range(int(cnt) // 8):
            thisChord = self.generate_chord()
            length = 8 if random.randint(1, 100) <= 27 else 4
            thisChord.quarterLength = length
            ret.append(thisChord)
            if length == 4:
                ret.append(copy.deepcopy(thisChord))
        return ret


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
        scale = scale_obj.getPitches('a3', 'f5')
        sz = len(scale)
        prob_list = [1] * sz
        chord_factor = [1] * sz
        # Construct magic probability factor
        # print(prev_note)
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
        prob = [0] * sz
        for i in range(sz):
            prob[i] = prob_list[i] ** (2 if prev_note.duration.quarterLength + dur <= 0.75 else 1) * chord_factor[i]
        ret_note = scale[data.weight_random_valuable(prob)]
        return music21.note.Note(ret_note, quarterLength=dur)

    def generate_melody(self) -> list[music21.note.Note]:
        part_melody = []
        pitch = -1
        while pitch == -1 or pitch % 12 not in [data.NOTE_NUMBER_CONV[x] - 12 for x in data.NATURAL_SCALE[self.tone]]:
            pitch = random.randint(57, 77)
        last_note = music21.note.Note(midi=pitch, quarterLength=4)
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
            bt = self.beat.generate_beat(32)
            ch = self.chord.generate_chord_list(bt)
            mel = PopMelody(bt, ch, self.tone)
            # for c in ch:
            #     print(c.quarterLength, end = ' ')
            # print()
            for c in ch:
                # print(c.quarterLength)
                part_chord.append(c)
            m = mel.generate_melody()
            for x in m:
                part_melody.append(x)
        ret.append(part_melody)
        ret.append(part_chord)
        return ret
