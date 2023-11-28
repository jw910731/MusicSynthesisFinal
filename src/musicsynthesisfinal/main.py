from note_factory import RandomNoteFactory
from music21.stream import Stream

def main():
    factory = RandomNoteFactory(4, 5)
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
