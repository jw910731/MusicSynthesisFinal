import music21
import pop, classical, folk, hiphop
def get_stream(style):
    p = style.generate_music()
    ret = music21.stream.Stream()
    for pt in p:
        ret.insert(0, pt)
    return ret
def main():
    st = input('(1)classical\n(2)pop\n(3)folk\n(4)hiphop\nyour style:')
    t = input('your tone?')
    if st == 'classical':
        stream = get_stream(classical.Classical(tone=t))
    elif st == 'pop':
        stream = get_stream(pop.Pop(tone=t))
    elif st == 'folk':
        stream = get_stream(folk.Folk(tone=t))
    elif st == 'hiphop':
        stream = get_stream(hiphop.Hiphop(tone=t))
    stream.show()
if __name__ == "__main__":
    main()
