from ai_note_factory import AiNoteFactory
from music21.stream import Stream


def main():
    factory = AiNoteFactory(
        "a uk drill mix boombap.", device="cpu")
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
