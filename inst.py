import pretty_midi

INST_DICT = {"Acoustic Grand Piano":0,
"Electric Grand Piano":2,
"Clavinet":7,
"Celesta":8,
"Music Box":10,
"Vibraphone":11,
"Marimba":12,
"Xylophone":13,
"Tubular Bells":14,
"Dulcimer":15,
"Drawbar Organ":16,
"Percussive Organ":17,
"Rock Organ":18,
"Church Organ":19,
"Reed Organ":20,
"Accordion":21,
"Harmonica":22,
"Tango Accordion":23,
"Acoustic Guitar (steel)":25,
"Guitar Harmonics":31,
"Acoustic Bass":32,
"Slap Bass 1":36,
"Violin":40,
"Viola":41,
"Cello":42,
"Contrabass":43,
"Tremolo Strings":44,
"Pizzicato Strings":45,
"Orchestral Harp":46,
"Timpani":47,
"String Ensemble 1":48,
"Synth Strings 1":50,
"Choir Aahs":52,
"Trumpet":56,
"Trombone":57,
"Tuba":58,
"Muted Trumpet":59,
"French Horn":60,
"Brass Section":61,
"Synth Brass 1":62,
"Oboe":68,
"Bassoon":70,
"Clarinet":71,
"Piccolo":72,
"Flute":73,
"Recorder":74,
"Pan Flute":75,
"Lead 8 (bass + lead)":87,
"Banjo":105,
"Tinkle Bell":112,
"Synth Drum":118,
}

class InstrumentChange:
    def __init__(self):
        pass
    def change_instrument(self, file_name, instrument):
        pm = pretty_midi.PrettyMIDI(file_name)
        program = pretty_midi.instrument_name_to_program(instrument)
        inst = pretty_midi.Instrument(program=program, is_drum=False, name=instrument)
        inst.notes.extend(pm.instruments[0].notes)
        pm.instruments.append(inst)
        pm.write(file_name)

if __name__ == '__main__':
    # inst = InstrumentChange()
    # print(inst.change_instrument('d', 1))
    # for idx, name in enumerate(inst_name):
    #     print('"'+name+'":'+str(idx)+",")

    for i in INST_DICT:
        print(i, end=", ")