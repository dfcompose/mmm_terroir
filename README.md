# Terroir | An algorithmic composition library for use with the MMMAudio environment

Terroir integrates directly with the MMMAudio environment

## Requirements

Terroir requires MMMAudio and all of its dependencies. Additionally, Terroir uses music21 for displaying scores using MuseScore. You can add music21 to your MMMAudio pixi environment with:

```shell
pixi add --pypi music21
```

## Using Terroir

Terroir its built around the use of Rolls, which store musical events as numpy lists. An event consists of an onset, pitch, duration, velocity, and an optional dictionary of metadata. 

```py
[onset, [[pitches], [durations], [velocities], [{Metadata}]]]
```

You can create a roll by either giving a list of each onsets, pitches, durations, velocities, and metadata, or set the events directly.

```py
onsets = [0, 1, 2, 3, 4]
pitches = [60, 62, 64, 65, 67]
durations = [1, 1, 1, 1, 1]
velocities = [0.5, 0.5, 0.5, 0.5, 0.5]
roll = Roll(onsets, pitches, durations, velocites, [{}]) # Empty metadata

# Or

roll = Roll().set_events(
    [[onsets[i], [[pitches[i]], [durations[i]], [velocities[i]], [{}]]] for i in len(onsets)]
)
```

You can then display the roll by calling the show() method

```py
roll.show()
```

This will open proportional notation of the roll that can be played back using MMMAudio.