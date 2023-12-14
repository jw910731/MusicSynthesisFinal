# import math
# import random

# import pop
# import music21
# # import pop
# import utils

# chordProcessor = ['C', 'G/B', 'Am', 'Em/G', 'F', 'C/E', 'Dm', 'G']
# chordProcessor2 = ['C', 'G/B', 'Am', 'C/G', 'F', 'C/E', 'Dm', 'G']

# c = music21.chord.Chord()
# tone = 'C'
# bala = []
# for i in range(10):
#     bala.append(pop.PopChord(tone))
# s = music21.stream.Stream()
# s.insert(0, music21.tempo.MetronomeMark(number=95))
# s.insert(0, music21.key.Key(tone))
# for i in bala:
#     for x in range(16):
#         s.append(i.generate_chord())
# print(bala.progressions)
# s.show()

# s = music21.stream.Stream()

# # s.insert(0, music21.instrument.BassDrum())
# s.insert(0, music21.instrument.SnareDrum())
# # s.insert(0, music21.instrument.HiHatCymbal())
# hihat = random.choice(utils.HIHAT_SCALE)
# bass = random.choice(utils.BASS_SCALE)
# snare = random.choice(utils.SNARE_SCALE)
# clap = random.choice(utils.CLAP_SCALE)
# # # boommap
# bassloop = [1,-1,1,-4,1,1,-1,1,-5]
# bassbasicbeat = 0.25
# snareloop = [-1,1]
# snarebasicbeat = 1
# hihatloop = [1,-1]
# hihatbasicbeat = 0.25
# claploop = [1,-1]
# clapbasicbeat = 1
# bpm = 90

# # trap
# bassloop = [4,1,-1,1,-1,-24,4,1,-1,1,-1,-20,-1,1,-1,1]
# bassbasicbeat = 0.25
# snareloop = [-4,1,-1,1,1,-4,1,-3, 4,-8,1,-1,1,1,-12,1,-1,1,1,4,1,-1,1,1,-4,1,-3]
# snarebasicbeat = 0.25
# hihatloop = [1,-1,1,-1,1,1,1,-1,1,-1,1,-1,1,-1,1,-1]
# hihatbasicbeat = 0.25
# claploop = [1,-1,1,-1,-2,1,-1]
# clapbasicbeat = 1
# bpm = 170


# # drill
# bassloop = [4,-4,-4,4,-4,4,-4,4,4, -4,-4,4,-4,4,4,1,1,-2]
# bassbasicbeat = 0.25
# snareloop = [-1,-1,1,-1,-1,-1,-1,1,-1,-1,1,-1,-1,-1,1,1]
# snarebasicbeat = 1
# hihatloop = [1,-1,-1,1, -1,-1,1,-1, 1,-1,-1,1, -1,-1,1,-1, 1,-1,-1,1, -1,-1,1,-1, 1,-1,1,-1, 1,-1,1,-1]
# hihatbasicbeat = 0.25
# claploop = [-4]
# clapbasicbeat = 1
# bpm = 140

# def gen(loop, basicbeat, total, pitch, bpm):
#     now = 0
#     idx = 0
#     part = music21.stream.Part()
#     part.insert(0,music21.tempo.MetronomeMark(number=bpm))
#     part.insert(0, music21.instrument.BassDrum())
#     while now < total:
#         if loop[idx]>0:
#             thisnote = music21.note.Note(pitch, quarterLength=loop[idx]*basicbeat)
#             now += loop[idx]*basicbeat
#         else:
#             thisnote = music21.note.Rest(quarterLength=-loop[idx]*basicbeat)
#             now -= loop[idx]*basicbeat
#         idx += 1
#         idx %= len(loop)
#         part.append(thisnote)
#     return part
# part_bass = gen(bassloop, bassbasicbeat, 32, bass, bpm)
# part_snare = gen(snareloop, snarebasicbeat, 32, snare, bpm)
# part_hihat = gen(hihatloop, hihatbasicbeat, 32, hihat, bpm)
# part_clap = gen(claploop, clapbasicbeat, 32, clap, bpm)
# s.insert(0, part_bass)
# s.insert(0, part_snare)
# s.insert(0, part_clap)
# s.insert(0, part_hihat)
# # for i in data.HIHAT_SCALE:
# #     s.append(music21.note.Note(i, quarterLength = 0.25))
# s.show()

# bpm = 140
# import random
# import music21
# def beat_recursive(size:float, part:float)->list[int]:
#     if size <= 0.25:
#         return [size]
#     if part == 6 and size == 2:
#         if random.randint(1,100) <= 10:
#             return [size]
#     if size <= 1 and random.random() <= (1/(4*size))**0.5:
#         return [size]
#     return beat_recursive(size/2, part) + beat_recursive(size/2, part+size/2)

# ls = beat_recursive(8,0)
# m = music21.stream.Stream()
# m.insert(0, music21.tempo.MetronomeMark(number=bpm))
# for i in ls:
#     m.append(music21.note.Note(1, quarterLength = i))
# print(ls)
# m.show()
import music21
import hiphop, pop
dri = hiphop.Hiphop('E')
song = dri.generate_music()
# bala = pop.Pop('E')
# song  = bala.generate_music()
s = music21.stream.Stream()
for x in song:
    s.insert(0, x)
s.show()
