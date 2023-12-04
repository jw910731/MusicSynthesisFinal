import math
import random

import classical
import music21
import data

tone = 'C'
c = classical.Classical(tone)
mus = c.generate_music()
s = music21.stream.Stream()
# print(mus)
for i in mus:
    s.insert(0, i)
s.show()
