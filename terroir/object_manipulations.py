import numpy as np
from mmm_python import *
import user.terroir as ter
from user.terroir.music_symbols import Clef


# [onset, [pitch, velocity, duration]]
class RollSeq:
    """
    A collection of Rolls.

    Args:
        rolls: A list of rolls.
        onsets: A list of onsets.
    """
    rolls: list
    seq_roll: ter.Roll
    events: list
    def __init__(self, onsets, rolls, callback=None):
        self.rolls = rolls
        self.offsets = onsets
        self.events = []
        
        for i, roll in enumerate(rolls):
            self.events.append([
                onsets[i], roll
            ])
            
        self._concat_rolls()
        
        if callback:
            import types
            self.seq_roll._handle_metadata = types.MethodType(callback, self.seq_roll)
            
        
    
    def play(self, mmm_audio_instance, collection_offset=0.0):
        scheduler = Scheduler()
        
        self.seq_roll.play(scheduler, mmm_audio_instance, collection_offset)
        
        # for roll in self.rolls:
        #     roll[1].play(scheduler, mmm_audio_instance, offset=roll[0] + collection_offset)
    
    def _concat_rolls(self):
        
        unique_onsets = []
        
        for i, roll in enumerate(self.rolls):
            for event in roll.events:
                unique_onsets.append(event[0] + self.offsets[i])
        unique_onsets = list(set(unique_onsets))
        unique_onsets.sort()
        new_events = []
        
        for onset in unique_onsets:
            combo_pitch = []
            combo_dur = []
            combo_vol = []
            combo_meta = []
            
            for i, roll in enumerate(self.rolls):
                for event in roll.events:
                    if event[0] + self.offsets[i]  == onset:
                        combo_pitch += event[1][0]
                        combo_dur += event[1][1]
                        combo_vol += event[1][2]
                        
                        [combo_meta.append(sub_dict) for sub_dict in event[1][3]]
                        
            
               
            new_events.append([onset, [combo_pitch, combo_dur, combo_vol, combo_meta]])
            
                    
        self.seq_roll = ter.Roll()
        self.seq_roll.set_events(new_events)
        
        pass
    
    def show(self, clefs=[Clef.TREBLE, Clef.BASS], mmm_audio_instance=None, data_handling=None):
        
        self.seq_roll.show(clefs, mmm_audio_instance, data_handling)
        
    
    def to_json(self, filename):
        
        pass


