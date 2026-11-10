from enum import StrEnum


class Clef(StrEnum):
    TREBLE = ''
    BASS = ''
    BASS_8VB = ''
    TREBLE_8VA = ''
    ALTO = ''
    TENOR = ''
    

    

class Staff(StrEnum):
    FIVELINE = ''
    LEDGER = ''

class Notehead(StrEnum):
    FILLED = ''


class Accidental(StrEnum):
    NATURAL = ''
    SHARP = ''
    FLAT = ''
    THREE_QUARTER_SHARP = ''
    QUARTER_SHARP = ''
    QUARTER_FLAT = ''