from mmm_audio import *


struct PianoNote(Movable, Copyable):
    var world: World
    var active: Bool
    var synth: Play
    var pitch: Int
    var rate: Float64
    var buffer: SIMDBuffer[1]
    var vel: Float64
    def __init__(out self, world: World, buffer: SIMDBuffer[1]):
        self.world = world
        self.synth = Play(world)
        self.active = False
        self.pitch = 0
        self.rate = 1.0
        self.buffer = buffer.copy()
        self.vel = 1.0
        
        pass
    
    def set_active(mut self, pitch: SIMDBuffer[1], rate: Float64, vel: Float64):
        self.buffer = pitch.copy()
        self.rate = rate
        self.vel = vel
        self.active = True
        pass
 
    def next(mut self) -> MFloat[1]:
        if self.active:
            self.world[].print("playing")
            var out = self.synth.next[num_chans=1](self.buffer, self.rate, False)
            return out * self.vel
        else:
            return MFloat[1](0.0)
        


struct TerPlayerPiano(Movable, Copyable):
    var world: World  
    var messenger: Messenger
    var synths: List[PianoNote]
    var index: Int
    var polys: InlineArray[List[Float64],3]
    var pitches: List[Float64]
    var durations: List[Float64]
    var velocities: List[Float64]
    # var buffers: Array[SIMDBuffer[1], 21]
    var buffer: SIMDBuffer[1]
    var tgrains: TGrains[win_type=WindowType.hann]
    var mult: Float64
    def __init__(out self, world: World):
        self.world = world
        # self.tgrains = TGrains
        self.messenger = Messenger(self.world)
        self.synths = List[PianoNote]()
        self.index = 0
        self.polys = [[],[],[]]
        self.pitches = []
        self.durations = []
        self.velocities = []
        self.buffer = SIMDBuffer[1].load("user/terroir/piano/piano_merged.wav")
        self.mult = Float64(len(self.buffer.data) / 21)
        self.tgrains = TGrains[win_type = WindowType.hann](self.world, 128)
        
        pass
    
    @always_inline
    def next(mut self) -> MFloat[2]:

        var new_vals : List[Float64] = [60, 0.0, 1.0, 1.0]
        
        self.messenger.update("poly_pitches", self.pitches)
        self.messenger.update("poly_durations", self.durations)
        self.messenger.update("poly_velocities", self.velocities)
        var grain_num = -1
        if self.messenger.notify_update("note_on", new_vals):
            grain_num = self.tgrains.trig(True)
        
        if grain_num >= 0:
            print(grain_num)
            self.tgrains.grains[grain_num].set_vals(1 + new_vals[1], Int(new_vals[0] * self.mult), new_vals[2], 0, new_vals[3])
        var out = self.tgrains.next_2[2](self.buffer)
        
        return MFloat[2](out[0], out[1])
            
        # if self.messenger.notify_update("note_on_poly", trig):
        #     # self.world[].print(self.pitches, self.durations, self.velocities)
        #     for i in range(len(self.pitches)):
                
        #         # self.synths[self.index].set_active(self.buffers[Int(self.pitches[i])], self.durations[i], self.velocities[i])
        #         self.index += 1
        #         self.index = self.index % 127
        # self.world[].print(self.pitches, self.durations, self.velocities)
        
        # for i in range(128):
            
        #     out += self.synths[i].next()
            
       
        # return out