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
drill = InstrumentSet()
drill.bpmrange = (140,150)
trap = InstrumentSet()
trap.bpmrange = (120,170)
boombap = InstrumentSet()
boombap.bpmrange = (80,95)

for i in range(4):
    drill.Snare.append(InstrumentAttribute(random.choice(utils.SNARE_SCALE)))
for i in range(3):
    drill.Bass.append(InstrumentAttribute(random.choice(utils.BASS_SCALE)))
drill.Hihat.append(InstrumentAttribute(random.choice(utils.HIHAT_SCALE)))
drill.Clap.append(InstrumentAttribute(random.choice(utils.CLAP_SCALE)))

drill.Bass[0].Template = [1,0,0,1,0,1,1,0,1,0,0,1,0,1,1,1]
drill.Bass[1].Template = [1,0,0,1,0,0,0,0,1,0,0,1,0,1,1,1]
drill.Bass[2].Template = [1,0,0,1,0,0,0,0,1,0,0,1,0,1,0,1]
drill.Bass[0].TemplateSplitway = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0.25]
drill.Bass[1].TemplateSplitway = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0.25]
drill.Bass[2].TemplateSplitway = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0.25]
drill.Bass[0].Probability = [[0.9],[],[],[0.9],[],[0.9],[0.9],[],[0.9],[],[],[0.9],[],[0.9],[0.9],[0.7,0.4,0.7,0.5]]
drill.Bass[1].Probability = [[0.9],[],[],[0.9],[],[],[],[],[0.9],[],[],[0.9],[],[0.9],[0.9],[0.7,0.4,0.7,0.5]]
drill.Bass[2].Probability = [[0.9],[],[],[0.9],[],[],[],[],[0.9],[],[],[0.9],[],[0.9],[],[0,0.4,0.8,0.5]]
drill.Snare[0].Template = [0,0,1,0,0,0,0,1,0,0,1,0,0,0,0,1]
drill.Snare[1].Template = [0,0,0,1,0,0,1,0,0,0,0,1,0,0,1,0]
drill.Snare[2].Template = [0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,1]
drill.Snare[3].Template = [0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,1]
drill.Snare[0].TemplateSplitway = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0.25]
drill.Snare[1].TemplateSplitway = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,0.25,1]
drill.Snare[2].TemplateSplitway = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0.25]
drill.Snare[3].TemplateSplitway = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0.25]
drill.Snare[0].Probability = [[],[],[0.8],[], [],[],[],[0.8], [],[],[0.8],[], [],[],[],[0.8,0,0.3,0.2]]
drill.Snare[1].Probability = [[],[],[],[0.8], [],[],[0.8],[], [],[0.8],[],[], [],[],[0.8,0,0.3,0.2],[]]
drill.Snare[2].Probability = [[],[0.8],[],[], [],[],[0.8],[], [],[],[],[], [],[],[],[0.8,0,0.3,0.2]]
drill.Snare[3].Probability = [[],[],[0.8],[],[],[],[],[0.8],[],[],[0.8],[],[],[],[],[0.8,0,0.3,0.2]]
drill.Hihat[0].Template = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
drill.Hihat[0].TemplateSplitway = [0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25]
drill.Hihat[0].Probability = [[1,0.4,0,1],[0.4,0,1,0],[1,0.4,0,1],[0.4,0,1,0],[1,0,0,1],[0.4,0,1,0],[1,0.7,1,0],[1,0,1,0],[1,0,0,1],[0,0,1,0],[1,0,0,1],[0,0,1,0],[1,0,0,1],[0,0,1,0],[1,0,1,0],[1,0.6,1,0]]

