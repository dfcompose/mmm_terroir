from mmm_audio import *
# from memory import ArcPointer



struct TerOsc(Movable, Copyable):
    var world: World
    var synth: Osc[1, interp=Interp.linear]
    var freq: Float64
    var dur: Float64
    var vol: Float64
    var active: Bool
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
        self.trigger = False
        self.event = List[Float64]()
        self.phase = MFloat[1](0.0)

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
        
        self.active = True

    def next(mut self) -> Float64:
        
        
        
        
        if self.active:
            
            var env = min_env(self.world, self.phase) * self.vol
            var sig = self.synth.next(self.freq)
            
            var out = sig * env 
            self.phase += 1.0/self.world[].sample_rate/self.dur
            self.active = self.phase <= 1.0
            return out
        else:
            
            return 0.0


struct TerOscPoly(PolyObject):
    var world: World
    var synth: Osc[1, interp=Interp.linear]
    var freq: Float64
    var dur: Float64
    var vol: Float64
    var active: Bool
    var triggered : Bool
    var event : List[Float64]
    var phase : Float64
    var messenger : Messenger
    var env : Array[Tuple[Float64, Float64], 4]
    var env_curve: Float64
    
    def check_active(mut self) -> Bool:
        return self.active

    def set_gate(mut self, trigger: Bool):
        
        self.active = trigger
        self.phase = 0.0

    def __init__(out self, world: World, name_space: String=""):
        self.world = world
        self.messenger = Messenger(self.world, name_space)
        self.freq = 440
        self.dur = 1
        self.vol = 0.5
        self.synth  = Osc[1, interp=Interp.linear](self.world)
        self.active = False
        self.triggered = False
        self.event = List[Float64]()
        self.phase = 0.0
        self.env : Array[Tuple[Float64, Float64], 4] = [(0.0, 0.0), (0.01, 1.0), (0.9, 1.0), (1.0, 0.0)]
        self.env_curve : Float64 = 1.0
        

    def next(mut self) -> Float64:

        if self.active:
            
            var env = env[win_type=WindowType.sine, interp=Interp.linear](self.world, self.phase, self.env, self.env_curve) * self.vol
            var sig = self.synth.next(self.freq)
            
            var out = sig * env 
            self.phase += 1.0/self.world[].sample_rate/self.dur
            self.active = self.phase <= 1.0
            return out
        else:
            
            return 0.0


struct TerFMPoly(PolyObject):
    var world: World
    var carrier: Osc[1, interp=Interp.linear]
    var modulator: Osc[1, interp=Interp.linear]
    var freq: Float64
    var mod_freq: Float64
    var mod_width: Float64
    var dur: Float64
    var vol: Float64
    var active: Bool
    var trigger : Bool
    var event : List[Float64]
    var phase : MFloat[1]
    var start : Float64
    var env : Array[Tuple[Float64, Float64], 4]
    var env_curve: Float64
    var pan : Float64
    
    def check_active(mut self) -> Bool:
        return self.active

    def set_gate(mut self, trigger: Bool):
        
        self.active = trigger
        self.phase = 0.0

    def __init__(out self, world: World):
        self.world = world
        self.freq = 440
        self.mod_freq = 20
        self.mod_width = 10
        self.dur = 1
        self.vol = 0.5
        self.carrier  = Osc[1, interp=Interp.linear](self.world)
        self.modulator = Osc[1, interp=Interp.linear](self.world)
        self.active = False
        self.trigger = False
        self.event = List[Float64]()
        self.phase = MFloat[1](0.0)
        self.start = 0.0
        self.env : Array[Tuple[Float64, Float64], 4] = [(0.0, 0.0), (0.01, 1.0), (0.9, 1.0), (1.0, 0.0)]
        self.env_curve : Float64 = 0.0
        self.pan = 0.0
    

    def next(mut self) -> MFloat[2]:
        
        if self.active:
            # var env = self.env.next(self.trigger)
            var env = env[win_type=WindowType.sine, interp=Interp.linear](self.world, self.phase, self.env, self.env_curve) * self.vol
            var mod = self.modulator.next(self.mod_freq) * (self.start + ((self.mod_width - self.start) * self.phase))
            var sig = self.carrier.next(self.freq + mod)
            
            var out = pan2(sig * env, self.pan) 
            self.phase += 1.0/self.world[].sample_rate/self.dur
            self.active = self.phase <= 1.0
            return out
        else:
            
            return MFloat[2](0.0)




struct TerFMVBAP(Movable, Copyable):
    var world: World
    var carrier: Osc[1, interp=Interp.linear]
    var modulator: Osc[1, interp=Interp.linear]
    var freq: Float64
    var mod_freq: Float64
    var mod_width: Float64
    var dur: Float64
    var vol: Float64
    var active: Bool
    var trigger : Bool
    var event : List[Float64]
    var phase : MFloat[1]
    var start : Float64
    var env : Array[Tuple[Float64, Float64], 4]
    var env_curve: Float64
    var pan : Float64
    def check_active(mut self) -> Bool:
        return self.phase <= 1.0

    def set_trigger(mut self, trigger: Bool):
        self.trigger = trigger

    def __init__(out self, world: World):
        self.world = world
        self.freq = 440
        self.mod_freq = 20
        self.mod_width = 10
        self.dur = 1
        self.vol = 0.5
        self.carrier  = Osc[1, interp=Interp.linear](self.world)
        self.modulator = Osc[1, interp=Interp.linear](self.world)
        self.active = False
        self.trigger = False
        self.event = List[Float64]()
        self.phase = MFloat[1](0.0)
        self.start = 0.0
        self.env : Array[Tuple[Float64, Float64], 4] = [(0.0, 0.0), (0.01, 1.0), (0.9, 1.0), (1.0, 0.0)]
        self.env_curve : Float64 = 0.0
        self.pan = 0.0
    def init_voice(mut self, pitch: Float64, dur: Float64, vol: Float64, mod_freq: Float64, mod_width: Float64, start: Float64, head: Float64 = 0.01, tail: Float64 = 0.9, curve: Float64 = 0.0, pan : Float64 = 0.0):
        self.dur = dur
        self.freq = midicps(pitch)
        self.vol = vol * 0.5
        self.phase[0] = 0.0
        self.active = True
        self.mod_freq = mod_freq
        self.mod_width = mod_width
        self.start = start
        self.env[1][0] = head
        self.env[2][0] = tail
        self.env_curve = curve
        self.pan = pan
        
        


        

    def next(mut self) -> MFloat[2]:
        
        
        
        
        if self.active:
            # var env = self.env.next(self.trigger)
            var env = env[win_type=WindowType.sine, interp=Interp.linear](self.world, self.phase, self.env, self.env_curve) * self.vol
            var mod = self.modulator.next(self.mod_freq) * (self.start + ((self.mod_width - self.start) * self.phase))
            var sig = self.carrier.next(self.freq + mod)
            
            var out = pan2(sig * env, self.pan) 
            self.phase += 1.0/self.world[].sample_rate/self.dur
            self.active = self.phase <= 1.0
            return out
        else:
            
            return MFloat[2](0.0)



struct TerBufPoly(PolyObject):
    var world: World
    var buf: SIMDBuffer[1]
    
    var rate: Float64
    var freq: Float64
    var dur: Float64
    var vol: Float64
    var active: Bool
    var trigger : Bool
    var event : List[Float64]
    var phase : MFloat[1]
    var start : Float64
    var env : Array[Tuple[Float64, Float64], 4]
    var env_curve: Float64
    var pan : Float64
    
    def check_active(mut self) -> Bool:
        return self.active

    def set_trigger(mut self, trigger: Bool):
        self.trigger = trigger

    def __init__(out self, world: World, sample_rate: Float64, ref data: List[Float64]):
        self.world = world
        self.freq = 440
        self.rate = 1
        self.dur = 1
        self.vol = 0.5
        self.buf = SIMDBuffer[1](data, sample_rate)
        self.active = False
        self.trigger = False
        self.event = List[Float64]()
        self.phase = MFloat[1](0.0)
        self.start = 0.0
        self.env : Array[Tuple[Float64, Float64], 4] = [(0.0, 0.0), (0.01, 1.0), (0.9, 1.0), (1.0, 0.0)]
        self.env_curve : Float64 = 0.0
        self.pan = 0.0
    
    def set_voice(mut self, vals: List[Float64]):
        print("Set voice")
        self.freq = vals[0]
        self.dur = vals[1]
        self.vol = vals[2]
        
        self.env[1][0] = vals[3]
        self.env[2][0] = vals[4]
        self.env_curve = vals[5]
        self.pan = vals[6]
        self.rate = vals[7]
        self.start = vals[8]
        self.active = True
        self.phase = 0.0
            
        

    def next(mut self) -> MFloat[2]:
        
        if self.active:
            
            var env = env[win_type=WindowType.sine, interp=Interp.linear](self.world, self.phase, self.env, self.env_curve) * self.vol
            
            var sig = self.buf.at_phase(self.world, self.start + (self.phase * self.dur))
            
            var out = pan2(sig * env, self.pan) 
            self.phase += (1.0/self.world[].sample_rate/self.dur) * self.rate
            self.active = self.phase <= 1.0
            return out
        else:
            
            return MFloat[2](0.0)
        

struct TerGrainPoly(PolyObject):
    var world: World
    var buf: SIMDBuffer[1]
    var tgrains: TGrains[win_type=WindowType.hann]
    var rate: Float64
    var freq: Float64
    var dur: Float64
    var vol: Float64
    var active: Bool
    var trigger : Bool
    var dens : Float64
    var trig : Dust[1]
    var phase : MFloat[1]
    var start : Float64
    var env : Array[Tuple[Float64, Float64], 4]
    var env_curve: Float64
    var pan : Float64
    
    def check_active(mut self) -> Bool:
        return self.active

    def set_trigger(mut self, trigger: Bool):
        self.trigger = trigger

    def __init__(out self, world: World, sample_rate: Float64, ref data: List[Float64]):
        self.world = world
        self.freq = 440
        self.trig = Dust[1](self.world)
        self.rate = 1
        self.dur = 1
        self.vol = 0.5
        self.buf = SIMDBuffer[1](data, sample_rate)
        self.active = False
        self.trigger = False
        self.dens = 40.0
        self.phase = MFloat[1](0.0)
        self.start = 0.0
        self.env : Array[Tuple[Float64, Float64], 4] = [(0.0, 0.0), (0.01, 1.0), (0.9, 1.0), (1.0, 0.0)]
        self.env_curve : Float64 = 0.0
        self.pan = 0.0
        self.tgrains = TGrains(self.world, 50)
    
    
    def set_voice(mut self, vals: List[Float64]):
        print("Set voice")
        self.freq = vals[0]
        self.dur = vals[1]
        self.vol = vals[2]
        
        self.env[1][0] = vals[3]
        self.env[2][0] = vals[4]
        self.env_curve = vals[5]
        self.pan = vals[6]
        self.rate = vals[7]
        self.start = vals[8]
        self.active = True
        self.phase = 0.0
            
        

    def next(mut self) -> MFloat[2]:
        
        if self.active:
           
            var env = env[win_type=WindowType.sine, interp=Interp.linear](self.world, self.phase, self.env, self.env_curve) * self.vol
            var impulse = self.trig.next_bool(self.dens, self.dens + 5, True)
            var grain_num = self.tgrains.trig(impulse)
            if grain_num >= 0:
                self.tgrains.grains[grain_num].set_vals(self.rate, Int(self.phase * Float64(self.buf.num_frames)), 0.15, self.pan, self.vol)
            var sig = self.tgrains.next_2[2](self.buf)
            
            var out = MFloat[2](sig[0], sig[1]) * env 
            self.phase += (1.0/self.world[].sample_rate/self.dur) * self.rate
            self.active = self.phase <= 1.0

            # var out = MFloat[2](0.0)
            return out
        else:
            
            return MFloat[2](0.0)

