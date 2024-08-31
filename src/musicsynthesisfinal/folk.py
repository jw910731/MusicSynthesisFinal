import music21

from musicsynthesisfinal import pop, utils


class Folk(pop.Pop):
    def __init__(self, tone):
        super().__init__(tone)

    def gen_part(self):
        return (utils.set_up_part(self.beat.get_bpm(),
                                  self.tone,
                                  music21.instrument.AcousticGuitar()),
                utils.set_up_part(self.beat.get_bpm(),
                                  self.tone,
                                  music21.instrument.AcousticGuitar()))

