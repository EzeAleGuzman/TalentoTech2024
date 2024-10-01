
from music21 import note, stream, tempo

# Crear un flujo de música (stream) para la melodía
melody = stream.Stream()

# Establecer el tempo (velocidad) de la melodía
bpm = tempo.MetronomeMark(number=120)
melody.append(bpm)

notes = [
    ('E5', 0.25), ('E6', 0.25), ('E5', 0.25), ('E6', 0.25),  # Parte inicial
    ('C6', 0.25), ('E5', 0.25), ('A5', 0.5), ('G#5', 0.25),
    ('E5', 0.25), ('G5', 0.25), ('A5', 0.25), ('F5', 0.25),
    ('G5', 0.5), ('E5', 0.25), ('C5', 0.25), ('D5', 0.25), ('B4', 0.25),
    ('C5', 0.25), ('E5', 0.25), ('G5', 0.25), ('A5', 0.25),  # Parte media
    ('F5', 0.25), ('G5', 0.5), ('E5', 0.25), ('C5', 0.25), 
    ('D5', 0.25), ('B4', 0.25), ('C5', 0.5), ('E5', 0.25), ('A5', 0.25), 
    ('B5', 0.5), ('G5', 0.25), ('B5', 0.25), ('C6', 0.5),

    ('D6', 0.25), ('F6', 0.25), ('E6', 0.25), ('G6', 0.25),  # Final
    ('A6', 0.5), ('F6', 0.25), ('G6', 0.25), ('A6', 0.5),
]

# Añadir las notas a la melodía
for pitch, duration in notes:
    melody.append(note.Note(pitch, quarterLength=duration))

# Reproducir la melodía
melody.show('midi')  # Abre el archivo MIDI en un reproductor asociado
