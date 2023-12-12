import copy
import chord, utils
from hiphoptemplate import *
import random

import music21

import beat
import melody
import pop


class HiphopBeat(beat.Beat):
    def __init__(self):
        self.hiphoptype = random.choice([ Boombap().boombap, Drill().drill,Trap().trap])  # , trap, boombap
        self.bass = random.choice(self.hiphoptype.Bass)
        self.hihat = random.choice(self.hiphoptype.Hihat)
        self.snare = random.choice(self.hiphoptype.Snare)
        self.clap = random.choice(self.hiphoptype.Clap)
        self.bpm = random.randint(*self.hiphoptype.bpmrange)
        self.prefixProbability = [0,0.3,0.3,0.4]
        self.postfixProbability = [0.4,0.3,0.3,0]
    def __beat_recursive(self, size: float, part: float) -> list[float]:
        if size <= 0.25:
            return [size]
        if part == 6 and size == 2:
            if random.randint(1, 100) <= 10:
                return [size]
        if size <= 2 and random.random() <= (1 / (1.8 * size)) ** 0.5:
            return [size]
        return self.__beat_recursive(size / 2, part) + self.__beat_recursive(size / 2, part + size / 2)

    def generate_beat(self, n) -> list[music21.duration.Duration]:
        ret = []
        for i in range(0, n, 8):
            ls = self.__beat_recursive(min(n - i, 8), 0)
            for x in ls:
                ret.append(music21.duration.Duration(x))
        return ret

    def get_bpm(self):
        return self.bpm
    def get_extention(self, original:list[music21.note.Note], pitch)->list[music21.note.Note]:
        cnt = 0
        ret = original
        for i in range(len(ret)):
            if isinstance(cnt, int):
                check = 0
                c = 0
                offset = 0
                while(c <= 1):
                    if(ret[i+offset].isNote):
                        check = 1
                    c+=ret[i+offset].quarterLength
                    offset+=1
                if check:
                    # postfix
                    if random.random() <= abs(cnt-0.75)/10.8:
                        offset2 = 0
                        if(ret[(i+offset+offset2) % len(ret)].quarterLength != 0.25):
                            ret[(i+offset+offset2) % len(ret)].quarterLength = 0.25
                            ret.insert(i+offset+offset2+1, music21.note.Rest(quarterLength = 0.25))
                            ret.insert(i+offset+offset2+1, music21.note.Rest(quarterLength = 0.25))
                            ret.insert(i+offset+offset2+1, music21.note.Rest(quarterLength = 0.25))
                        while ret[(i+offset+offset2) % len(ret)].isRest and offset2<4:
                            if(random.random()<=self.postfixProbability[offset2]):
                                ret[(i+offset+offset2) % len(ret)] = music21.note.Note(pitch, quarterLength = ret[(i+offset+offset2) % len(ret)].quarterLength)
                            offset2+=1
                    #prefix
                    if random.random() <= abs(cnt-0.75)/10.8:
                        offset2 = 0
                        if(ret[(i-offset2+ len(ret)) % len(ret)].quarterLength != 0.25):
                            ret[(i-offset2+ len(ret)) % len(ret)].quarterLength = 0.25
                            ret.insert((i-offset2-1+ len(ret)) % len(ret), music21.note.Rest(quarterLength = 0.25))
                            ret.insert((i-offset2-1+ len(ret)) % len(ret), music21.note.Rest(quarterLength = 0.25))
                            ret.insert((i-offset2-1+ len(ret)) % len(ret), music21.note.Rest(quarterLength = 0.25))
                        while ret[(i-offset2+ len(ret)) % len(ret)].isRest and offset2<4:
                            if(random.random()<=self.prefixProbability[offset2]):
                                ret[(i-offset2+ len(ret)) % len(ret)] = music21.note.Note(pitch, quarterLength = ret[(i-offset2+ len(ret)) % len(ret)].quarterLength)
                            offset2+=1
            cnt += ret[i].quarterLength
        return ret            
    def generate_bass(self) -> list[music21.note.Note]:
        ret = []
        for i in range(16):
            if self.bass.Template[i]:
                # gen_beat
                du = self.bass.TemplateSplitway[i]
                for p in self.bass.Probability[i]:
                    if random.random() <= p:
                        ret.append(music21.note.Note(self.bass.pitch, quarterLength=du))
                    else:
                        ret.append(music21.note.Rest(quarterLength=du))

            else:
                ret.append(music21.note.Rest(quarterLength=1))
        return self.get_extention(ret, self.bass.pitch)

    def generate_hihat(self) -> list[music21.note.Note]:
        ret = []
        for i in range(16):
            if self.hihat.Template[i]:
                # gen_beat
                du = self.hihat.TemplateSplitway[i]
                for p in self.hihat.Probability[i]:
                    if random.random() <= p:
                        ret.append(music21.note.Note(self.hihat.pitch, quarterLength=du))
                    else:
                        ret.append(music21.note.Rest(quarterLength=du))

            else:
                ret.append(music21.note.Rest(quarterLength=1))
        return self.get_extention(ret, self.hihat.pitch)

    def generate_snare(self) -> list[music21.note.Note]:
        ret = []
        for i in range(16):
            if self.snare.Template[i]:
                # gen_beat
                du = self.snare.TemplateSplitway[i]
                for p in self.snare.Probability[i]:
                    if random.random() <= p:
                        ret.append(music21.note.Note(self.snare.pitch, quarterLength=du))
                    else:
                        ret.append(music21.note.Rest(quarterLength=du))

            else:
                ret.append(music21.note.Rest(quarterLength=1))
        return self.get_extention(ret, self.snare.pitch)

    def generate_clap(self) -> list[music21.note.Note]:
        ret = []
        for i in range(16):
            if self.clap.Template[i]:
                # gen_beat
                du = self.clap.TemplateSplitway[i]
                for p in self.clap.Probability[i]:
                    if random.random() <= p:
                        ret.append(music21.note.Note(self.clap.pitch, quarterLength=du))
                    else:
                        ret.append(music21.note.Rest(quarterLength=du))

            else:
                ret.append(music21.note.Rest(quarterLength=1))
        return self.get_extention(ret, self.clap.pitch)


class HiphopChord(pop.PopChord):
    def __init__(self, tone):
        super().__init__(tone)


class Hiphop:
    def __init__(self, tone='F#'):
        self.chord = HiphopChord(tone)
        self.beat = HiphopBeat()
        self.tone = tone

    def generate_music(self):
        part_chord = utils.set_up_part(self.beat.get_bpm(), self.tone)
        part_melody = utils.set_up_part(self.beat.get_bpm(), self.tone)
        part_bass = utils.set_up_part(self.beat.get_bpm(), self.tone, music21.instrument.BassDrum())
        part_hihat = utils.set_up_part(self.beat.get_bpm(), self.tone, music21.instrument.BassDrum())
        part_clap = utils.set_up_part(self.beat.get_bpm(), self.tone, music21.instrument.BassDrum())
        part_snare = utils.set_up_part(self.beat.get_bpm(), self.tone, music21.instrument.BassDrum())
        
        for x in range(4):
            bt = self.beat.generate_beat(8)
            ch = self.chord.generate_chord_list(bt)
            mel = melody.CommonMelody(bt, ch, self.tone)
            m = mel.generate_melody()
            bass = self.beat.generate_bass()
            snare = self.beat.generate_snare()
            clap = self.beat.generate_clap()
            hihat = self.beat.generate_hihat()
            for y in range(2):
                for a, b in zip([part_chord, part_melody], [ch, m]):
                    for r in b:
                        a.append(copy.deepcopy(r))
                for a, b in zip([part_chord, part_melody, part_bass, part_hihat, part_snare, part_clap],
                                [ch, m, bass, hihat, snare, clap]):
                    for r in b:
                        a.append(copy.deepcopy(r))
        # return part_hihat
        # return part_bass, part_snare, part_clap, part_hihat
        return part_melody, part_chord, part_bass, part_snare, part_clap, part_hihat
