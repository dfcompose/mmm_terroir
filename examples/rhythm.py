from mmm_terroir import *
from random import randint
num_events = 2000

mel = [0, 0, 7, 7, 9, 9, 7, 5, 5, 4, 4, 2, 7, 0]
pitches = [60 + [-12, 0,2,4,7,9][randint(0, 5)] for _ in range(num_events)]

rhythms = [
    [0.25, 0.5, -0.25][randint(0, 2)] for _ in range(num_events)
]

onsets, durations = format_rhythm(120, rhythms)


roll = Roll().set_events(
    [[onsets[i], [
        [pitches[i]],
        [durations[i] + 0.1],
        [0.5],
        [{
            "start": midicps(pitches[i]) * 0.5,
            "width": midicps(pitches[i]) * 1.0, 
            "rate": midicps(pitches[i]) * 2.5
            }]
    ]] for i in range(len(onsets))]
)

roll.show(default_player=TerPlayer.FM)

