import asyncio 
from mmm_python import *
from enum import Enum 
# from user.Terroir.TerObject import *

player = None

class TerInstruments(Enum):
     SYNTH = 0
     PIANO = 1

class TerPlayer:
    SYNTH = 0
    PIANO = 1
    _instance = None
    _mmm_audio_instance = MMMAudio(1024, num_output_channels=2, graph_name="TerPlayer", package_name="user.terroir")
    scheduler = Scheduler()
    # def __new__(cls):
    #     if cls._instance is None:
    #         cls._instance = super().__new__(cls)
    #         # cls.start()
    #         # cls._mmm_audio_instance = MMMAudio(128, num_output_channels=2, graph_name="TerPlayer", package_name="user.Terroir")
    #     return cls._instance

    def __init__(self):
        

        if not hasattr(self, "initialised"):
            self.start()
            self.initialised = True

    def stop(self):
        self._mmm_audio_instance.stop_audio()

    def start(self):
        
        self._mmm_audio_instance.start_audio()

    async def play_note(self, onset, pitches, durations, velocities):
            print("playing note", onset, pitches, durations, velocities)
            
            await asyncio.sleep(onset)
          
            self._mmm_audio_instance.send_floats("note_on", [pitches, durations, velocities])
            
            asyncio.current_task().cancel()
            
    async def play_poly(self, onset, pitches, durations, velocities):
        
        await asyncio.sleep(onset)
        
        self._mmm_audio_instance.send_floats("poly_pitches", pitches)
        self._mmm_audio_instance.send_floats("poly_durations", durations)
        self._mmm_audio_instance.send_floats("poly_velocities", velocities)

        self._mmm_audio_instance.send_bool("note_on_poly", True)
        asyncio.current_task().cancel()



player = TerPlayer()
