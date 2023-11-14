from ai_note_factory import AiNoteFactory
from music21.stream import Stream
import torch


def device_chooser():
    if torch.backends.mps.is_built():
        return "mps"
    if torch.backends.cudnn.is_available():
        return "cudnn"
    if torch.cuda.is_available():
        return "cuda"
    return "cpu"


def main():
    dev_str = device_chooser()
    print("Currently using \"{}\" for inference.".format(dev_str))
    factory = AiNoteFactory(
        "This is a traditional Irish dance music. In G major", device=dev_str)
    stream = Stream()
    part = factory.get_notes()
    if part.isWellFormedNotation():
        stream.append(part)
        stream = stream.flatten()
        stream.show()
    else:
        part.show()


if __name__ == "__main__":
    main()
