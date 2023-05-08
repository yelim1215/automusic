chord = 'G:sus4(b7)'

chord = chord.replace(":", "")
chord = chord.split('/')[0]
chord = chord.split('(')[0]
print(chord)  # "C#:7"