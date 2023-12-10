import utils, random
class InstrumentAttribute():
    def __init__(self, pitch:int):
        self.Template = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.TemplateSplitway = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        self.Probability = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        self.pitch = pitch
class InstrumentSet():
    def __init__(self):
        self.Bass = []
        self.Hihat = []
        self.Snare = []
        self.Clap = []
        self.bpmrange = (90,120)

class Drill:
    def __init__(self):
        self.drill = InstrumentSet()
        self.drill.bpmrange = (140,150)
        for i in range(4):
            self.drill.Snare.append(InstrumentAttribute(random.choice(utils.SNARE_SCALE)))
        for i in range(3):
            self.drill.Bass.append(InstrumentAttribute(random.choice(utils.BASS_SCALE)))
        self.drill.Hihat.append(InstrumentAttribute(random.choice(utils.HIHAT_SCALE)))
        self.drill.Clap.append(InstrumentAttribute(random.choice(utils.CLAP_SCALE)))

        self.drill.Bass[0].Template = [1,0,0,1,0,1,1,0,1,0,0,1,0,1,1,1]
        self.drill.Bass[1].Template = [1,0,0,1,0,0,0,0,1,0,0,1,0,1,1,1]
        self.drill.Bass[2].Template = [1,0,0,1,0,0,0,0,1,0,0,1,0,1,0,1]
        self.drill.Bass[0].TemplateSplitway = [0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25]
        self.drill.Bass[1].TemplateSplitway = [0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25]
        self.drill.Bass[2].TemplateSplitway = [0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25]
        self.drill.Bass[0].Probability = [[0.8,0.2,0.5,0.1],[],[],[0.8,0.2,0.5,0.1],[],[0.8,0.2,0.5,0.1],[0.8,0.2,0.5,0.1],[],[0.8,0.2,0.5,0.1],[],[],[0.8,0.2,0.5,0.1],[],[0.8,0.2,0.5,0.1],[0.8,0.2,0.5,0.1],[0.7,0.4,0.7,0.5]]
        self.drill.Bass[1].Probability = [[0.8,0.2,0.5,0.1],[],[],[0.8,0.2,0.5,0.1],[],[],[],[],[0.8,0.2,0.5,0.1],[],[],[0.8,0.2,0.5,0.1],[],[0.8,0.2,0.5,0.1],[0.8,0.2,0.5,0.1],[0.7,0.4,0.7,0.5]]
        self.drill.Bass[2].Probability = [[0.8,0.2,0.5,0.1],[],[],[0.8,0.2,0.5,0.1],[],[],[],[],[0.8,0.2,0.5,0.1],[],[],[0.8,0.2,0.5,0.1],[],[0.8,0.2,0.5,0.1],[],[0,0.4,0.8,0.5]]
        self.drill.Snare[0].Template = [0,0,1,0,0,0,0,1,0,0,1,0,0,0,0,1]
        self.drill.Snare[1].Template = [0,0,0,1,0,0,1,0,0,0,0,1,0,0,1,0]
        self.drill.Snare[2].Template = [0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,1]
        self.drill.Snare[3].Template = [0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,1]
        self.drill.Snare[0].TemplateSplitway = [0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25]
        self.drill.Snare[1].TemplateSplitway = [0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25]
        self.drill.Snare[2].TemplateSplitway = [0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25]
        self.drill.Snare[3].TemplateSplitway = [0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25]
        self.drill.Snare[0].Probability = [[],[],[0.8,0.1,0.3,0.1],[], [],[],[],[0.8,0.1,0.3,0.1], [],[],[0.8,0.1,0.3,0.1],[], [],[],[],[0.8,0,0.3,0.2]]
        self.drill.Snare[1].Probability = [[],[],[],[0.8,0.1,0.3,0.1], [],[],[0.8,0.1,0.3,0.1],[], [],[0.8,0.1,0.3,0.1],[],[], [],[],[0.8,0,0.3,0.2],[]]
        self.drill.Snare[2].Probability = [[],[0.8,0.1,0.3,0.1],[],[], [],[],[0.8,0.1,0.3,0.1],[], [],[],[],[], [],[],[],[0.8,0,0.3,0.2]]
        self.drill.Snare[3].Probability = [[],[],[0.8,0.1,0.3,0.1],[],[],[],[],[0.8,0.1,0.3,0.1],[],[],[0.8,0.1,0.3,0.1],[],[],[],[],[0.8,0,0.3,0.2]]
        self.drill.Hihat[0].Template = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        self.drill.Hihat[0].TemplateSplitway = [0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25]
        self.drill.Hihat[0].Probability = [[1,0.4,0,1],[0.4,0,1,0],[1,0.4,0,1],[0.4,0,1,0],[1,0,0,1],[0.4,0,1,0],[1,0.7,1,0],[1,0,1,0],[1,0,0,1],[0,0,1,0],[1,0,0,1],[0,0,1,0],[1,0,0,1],[0,0,1,0],[1,0,1,0],[1,0.6,1,0]]

class Boombap:
    def __init__(self):
        self.boombap = InstrumentSet()
        self.boombap.bpmrange = (80,95)
        self.boombap.Bass.append(InstrumentAttribute(random.choice(utils.BASS_SCALE)))
        self.boombap.Snare.append(InstrumentAttribute(random.choice(utils.SNARE_SCALE)))
        self.boombap.Hihat.append(InstrumentAttribute(random.choice(utils.HIHAT_SCALE)))
        self.boombap.Clap.append(InstrumentAttribute(random.choice(utils.CLAP_SCALE)))
        self.boombap.Bass[0].Template = [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0]
        self.boombap.Bass[0].TemplateSplitway = [0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25]
        self.boombap.Bass[0].Probability = [[1,0.2,0.5,0.2],[],[1,0.2,0.5,0.2],[],[1,0.2,0.5,0.2],[],[1,0.2,0.5,0.2],[],[1,0.2,0.5,0.2],[],[1,0.2,0.5,0.2],[],[1,0.2,0.5,0.2],[],[1,0.2,0.7,0.2],[]]
        self.boombap.Snare[0].Template = [0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1]
        self.boombap.Snare[0].TemplateSplitway = [0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25]
        self.boombap.Snare[0].Probability = [[],[1,0.2,0.1,0.2],[],[1,0.2,0.1,0.2],[],[1,0.2,0.1,0.2],[],[1,0.2,0.1,0.2],[],[1,0.2,0.1,0.2],[],[1,0.2,0.1,0.2],[],[1,0.2,0.1,0.2],[],[1,0.2,0.6,0.2]]
        self.boombap.Hihat[0].Template = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        self.boombap.Hihat[0].TemplateSplitway = [0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25]
        self.boombap.Hihat[0].Probability = [[0.7,0.2,0.5,0.2],[0.7,0.2,0.5,0.2],[0.7,0.2,0.5,0.2],[0.7,0.2,0.5,0.2],[0.7,0.2,0.5,0.2],[0.7,0.2,0.5,0.2],[0.7,0.2,0.5,0.2],[0.7,0.2,0.5,0.2],[0.7,0.2,0.5,0.2],[0.7,0.2,0.5,0.2],[0.7,0.2,0.5,0.2],[0.7,0.2,0.5,0.2],[0.7,0.2,0.5,0.2],[0.7,0.2,0.5,0.2],[0.7,0.2,0.5,0.2],[0.8,0.3,0.6,0.5]]
        self.boombap.Clap[0].Template = [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0]
        self.boombap.Clap[0].TemplateSplitway = [0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25]
        self.boombap.Clap[0].Probability = [[0.7,0.3,0.5,0.2],[],[0.7,0.3,0.5,0.2],[],[0.7,0.3,0.5,0.2],[],[0.7,0.3,0.5,0.2],[],[0.7,0.3,0.5,0.2],[],[0.7,0.3,0.5,0.2],[],[0.7,0.3,0.5,0.2],[],[0.7,0.3,0.5,0.2],[]]
class Trap:
    def __init__(self):
        self.trap = InstrumentSet()
        self.trap.bpmrange = (120,170)
        self.trap.Bass.append(InstrumentAttribute(random.choice(utils.BASS_SCALE)))
        self.trap.Snare.append(InstrumentAttribute(random.choice(utils.SNARE_SCALE)))
        self.trap.Hihat.append(InstrumentAttribute(random.choice(utils.HIHAT_SCALE)))
        self.trap.Clap.append(InstrumentAttribute(random.choice(utils.CLAP_SCALE)))
        self.trap.Bass[0].Template = [1,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0]
        self.trap.Bass[0].TemplateSplitway = [0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25]
        self.trap.Bass[0].Probability = [[0.7,0.3,0.6,0.4],[],[],[],[],[],[],[],[0.7,0.3,0.6,0.4],[],[],[],[],[],[],[]]
        self.trap.Snare[0].Template = [0,1,0,1, 1,0,0,1, 0,0,0,0, 1,0,0,1]