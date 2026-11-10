from mmm_python import *
from user.terroir import graphics_helpers
from math import modf
class TerPlayerPiano():
    _instance = None
    _mmm_audio_instance = MMMAudio(1024, num_output_channels=2, graph_name="TerPlayerPiano", package_name="user.terroir")
    scheduler = Scheduler()
    def __init__(self):

        if not hasattr(self, "initialised"):
            self.start()
            self.initialised = True
        pass

    def start(self):
        self._mmm_audio_instance.start_audio()

    def stop(self):
        self._mmm_audio_instance.start_audio()


    async def play_note(self, onset, pitches, durations, velocities):
        
        
        await asyncio.sleep(onset)
        print("playing note")
        cents, midicent = modf(pitches)
        pitch_class = midicent % 12
        octave = divmod(midicent, 12)[0]
        buffer_start = 0
        pitch_bend = pow(2, cents/12)
        match pitch_class:
            case 0:
                buffer_start = 5 + octave

        print(pitch_bend)
        self._mmm_audio_instance.send_floats("note_on", [pitches, pitch_bend, durations, velocities])
        
        asyncio.current_task().cancel() #type:ignore
                
    async def play_poly(self, onset, pitches, durations, velocities):
        
        await asyncio.sleep(onset)
        
        self._mmm_audio_instance.send_floats("poly_pitches", pitches)
        self._mmm_audio_instance.send_floats("poly_durations", durations)
        self._mmm_audio_instance.send_floats("poly_velocities", velocities)

        self._mmm_audio_instance.send_bool("note_on_poly", True)
        asyncio.current_task().cancel() #type:ignore


# start_player()
player = TerPlayerPiano()
player.start()
player.scheduler.sched(player.play_note(0.5, 2.0, 3.0, 1.0))
player.scheduler.sched(player.play_note(1.5, 4.0, 3.0, 1.0))