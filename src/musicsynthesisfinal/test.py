import math
import random

import pop
import music21
import data

tone = 'C'
c = pop.Pop(tone)
mus = c.generate_music()
s = music21.stream.Stream()
for i in mus:
    s.insert(0, i)
s.show()
