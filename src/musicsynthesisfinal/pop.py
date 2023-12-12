import random
import typing
import copy

import music21

import beat
import chord
import melody
import utils


class PopBeat(beat.Beat):
    def __init__(self):
        self.bpm = random.randint(90, 150)
        pass

    def __beat_recursive(self, size: float, part: float) -> list[float]:
        if size <= 0.25:
            return [size]
        if part == 6 and size == 2:
            if random.randint(1, 100) <= 10:
                return [size]
        if size <= 1 and random.random() <= (1 / (2 * size)) ** 0.5:
            return [size]
        return self.__beat_recursive(size / 2, part) + self.__beat_recursive(size / 2, part + size / 2)

    def generate_beat(self, n) -> list[music21.duration.Duration]:
        ret = []
        for i in range(0, n, 8):
            ls = self.__beat_recursive(min(n-i,8), 0)
            for x in ls:
                ret.append(music21.duration.Duration(x))
        return ret

    def get_bpm(self):
        return self.bpm

    def generate_bass(self) -> list[music21.note.Note]:
        pass

    def generate_hihat(self) -> list[music21.note.Note]:
        pass

    def generate_snare(self) -> list[music21.note.Note]:
        pass

    def generate_clap(self) -> list[music21.note.Note]:
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
            this_chord = self.generate_chord()
            length = 8 if random.randint(1, 100) <= 27 else 4
            this_chord.quarterLength = 4
            ret.append(this_chord)
            if length == 8:
                ret.append(copy.deepcopy(this_chord))
            else:
                this_chord = self.generate_chord()
                this_chord.quarterLength = 4
                ret.append(this_chord)
                
            
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
        pitch = -1
        while pitch == -1 or pitch % 12 not in [utils.NOTE_NUMBER_CONV[x] - 12 for x in utils.NATURAL_SCALE[self.tone]]:
            pitch = random.randint(57, 77)
        last_note = music21.note.Note(midi=pitch, quarterLength=4)
        offset = 0
        now_chord = 0
        chord_duration = self._chord[0].quarterLength
        for bt in self._beat:
            # print (chord_duration, now_chord, offset, bt)
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
        self.verse_chord = PopChord(tone)
        self.chorus_chord = PopChord(tone)
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
        
        verse_beat = []
        verse_chordpro = []
        verse_melody = []
        for i in range(2):
            bt = self.beat.generate_beat(32)
            ch = self.verse_chord.generate_chord_list(bt)
            mel = PopMelody(bt, ch, self.tone)
            for b in bt:
                verse_beat.append(b)
            for c in ch:
                verse_chordpro.append(c)
            m = mel.generate_melody()
            for x in m:
                verse_melody.append(x)
                
        chorus_beat = self.beat.generate_beat(16)
        
        chorus_chordpro = self.chorus_chord.generate_chord_list(chorus_beat)
        chorus_melody = PopMelody(chorus_beat, chorus_chordpro, self.tone).generate_melody()
        change_beat = self.beat.generate_beat(4)
        change_chordpro = [chorus_chordpro[-1]]
        change_chordpro[0].quarterLength = 4
        change_melody = PopMelody(change_beat, change_chordpro, self.tone).generate_melody()
        
        intro_beat = utils.cut_front(chorus_beat, 8)

        for i in intro_beat:
            i.quarterLength *=1.5
        intro_beat[-1].quarterLength+=4
            
        intro_chordpro = utils.cut_front(chorus_chordpro, 8)

        # print([x.quarterLength for x in intro_chordpro])
        for i in intro_chordpro:
            # print(i.quarterLength)
            i.quarterLength *=1.5
        intro_chordpro[-1].quarterLength+=4
        intro_melody = utils.cut_front(chorus_melody, 8)
        for i in intro_melody:
            i.quarterLength *=1.5
        intro_melody[-1].quarterLength += 4
        
        chorus_beat+=copy.deepcopy(chorus_beat)
        chorus_chordpro+=copy.deepcopy(chorus_chordpro)
        chorus_melody+=copy.deepcopy(chorus_melody)
        cnt = 0
        while cnt < 4:
            cnt += chorus_beat[-1].quarterLength
            chorus_beat.pop()
        for x in change_beat:
            chorus_beat.append(x)
        cnt = 0
        while cnt < 4:
            cnt += chorus_melody[-1].quarterLength
            chorus_melody.pop()
        for x in change_melody:
            chorus_melody.append(x)
        
        for c in intro_chordpro:
            part_chord.append(copy.deepcopy(c))
        for x in intro_melody:
            part_melody.append(copy.deepcopy(x))
        for _ in range(2):
            for c in verse_chordpro:
                part_chord.append(copy.deepcopy(c))
            for x in verse_melody:
                part_melody.append(copy.deepcopy(x))
            for i in range(2):
                for c in chorus_chordpro:
                    part_chord.append(copy.deepcopy(c))
                for x in chorus_melody:
                    part_melody.append(copy.deepcopy(x))
        # for i in range(2):
        #     bt = self.beat.generate_beat(32)
        #     ch = self.chord.generate_chord_list(bt)
        #     mel = PopMelody(bt, ch, self.tone)
        #     for c in ch:
        #         part_chord.append(c)
        #     m = mel.generate_melody()
        #     for x in m:
        #         part_melody.append(x)
        ret.append(part_melody)
        ret.append(part_chord)
        return ret
