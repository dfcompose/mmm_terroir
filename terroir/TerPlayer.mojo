from mmm_audio import *


struct TerOsc(Movable, Copyable):
    var world: World
    var synth: Osc[1, interp=Interp.linear]
    var freq: Float64
    var dur: Float64
    var vol: Float64
    var active: Bool
    var env: Env
    # var env_params: EnvParams
    var trigger : Bool
    var event : List[Float64]
    var phase : MFloat[1]
    
    def check_active(mut self) -> Bool:
        return self.phase <= 1.0

    def set_trigger(mut self, trigger: Bool):
        self.trigger = trigger

    def __init__(out self, world: World):
        self.world = world
        self.freq = 440
        self.dur = 1
        self.vol = 0.5
        self.synth  = Osc[1, interp=Interp.linear](self.world)
        self.active = False
        self.env = Env(world)
        self.env.params = EnvParams([0.0, self.vol, self.vol, 0.0], [0.05, self.dur - 0.1, 0.05])
        self.trigger = False
        self.event = List[Float64]()
        self.phase = MFloat[1](0.0)

    def next(mut self) -> Float64:
        
        
        
        
        if self.active:
            # var env = self.env.next(self.trigger)
            var env = min_env(self.world, self.phase) * self.vol
            var sig = self.synth.next(self.freq)
            
            var out = sig * env 
            self.phase += 1.0/self.world[].sample_rate/self.dur
            self.active = self.phase <= 1.0
            return out
        else:
            
            return 0.0

    def init_voice(mut self, pitch: Float64, dur: Float64, vol: Float64):
        self.dur = dur
        self.freq = midicps(pitch)
        self.vol = vol * 0.5
        self.phase[0] = 0.0
        self.active = True
        

    def set_active(mut self, pitch: Float64, dur: Float64, vel: Float64):
        self.freq = midicps(pitch)
        self.dur = dur
        self.vol = vel
        self.env.params.times = [0.05, dur - 0.1, 0.05]
        self.env.params.values = [0.0, self.vol, self.vol, 0.0]
        
        
        self.active = True

struct TerPlayer(Movable, Copyable):
    var world: World  
    var messenger: Messenger
    var synths: List[TerOsc]
    var index: Int
    var polys: InlineArray[List[Float64],3]
    var pitches: List[Float64]
    var durations: List[Float64]
    var velocities: List[Float64]

    def __init__(out self, world: World):
        self.world = world
        # self.tgrains = TGrains
        self.messenger = Messenger(self.world)
        self.synths = List[TerOsc]()
        self.index = 0
        self.polys = [[],[],[]]
        self.pitches = []
        self.durations = []
        self.velocities = []
       
        for _ in range(128):
            self.synths.append(TerOsc(self.world))
       
    
    def next(mut self) -> MFloat[2]:
        var new_vals : List[Float64] = [60, 1.0, 1.0]
        var trig = True

        
        self.messenger.update("poly_pitches", self.pitches)
        self.messenger.update("poly_durations", self.durations)
        self.messenger.update("poly_velocities", self.velocities)
        
        



        if self.messenger.notify_update("note_on", new_vals):
            self.synths[self.index].init_voice(new_vals[0], new_vals[1], new_vals[2])
            self.index += 1
            self.index = self.index % 127
            
        if self.messenger.notify_update("note_on_poly", trig):
            # self.world[].print(self.pitches, self.durations, self.velocities)
            for i in range(len(self.pitches)):
                
                self.synths[self.index].init_voice(self.pitches[i], self.durations[i], self.velocities[i])
                self.index += 1
                self.index = self.index % 127
        # self.world[].print(self.pitches, self.durations, self.velocities)
        var out = MFloat[2](0.0)
        for i in range(128):
            if self.synths[i].active:
                
                out += self.synths[i].next()
        
        return out
        
        
