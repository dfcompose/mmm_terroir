

class Bar:
    def __init__(self, num_beats):
        self.num_beats = num_beats




def format_rhythm(tempo: float, rhythms: list) -> tuple:
    """
    Returns a tuple of onsets and durations for the given rhythm
    """
    out = ([], []) # onsets, durations
    total_dur = 0
    tempo_adjust = 60/tempo
    
    
    for rhythm in rhythms:
        
        if rhythm > 0:
            out[0].append(total_dur)
            out[1].append(rhythm * tempo_adjust)
    
        total_dur += abs(rhythm) * tempo_adjust
    
    return out


def retrograde_rhythm(onsets: list, durs: list) -> tuple:
    out = []
    last = onsets[0]
    rev = onsets.copy()
    rev.reverse()
    dur_rev = durs.copy()
    dur_rev.reverse()
    for i, x in enumerate(onsets):
        if i > 0:
            out.append(
                abs(rev[i] - rev[0] - dur_rev[0])
            )
        else:
            out.append(
                abs(rev[i] - rev[0] )
            )
    
    return (out, dur_rev)