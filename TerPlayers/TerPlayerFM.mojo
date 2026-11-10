from mmm_audio import *
from user.TerPlayers.TerPolys import TerFMPoly


struct TerPlayerFM(Movable, Copyable):
    var poly: Poly
    var world: World
    var voices: List[TerFMPoly]
    var messenger: Messenger
    def __init__(out self, world: World):
        self.world = world
        self.messenger = Messenger(self.world)
        self.poly = Poly(self.world, 128, "poly")
        self.voices = [TerFMPoly(self.world) for _ in range(128)]

        pass
 
    def next(mut self) -> MFloat[2]:
        
        def callback(mut poly_object: TerFMPoly, mut vals: List[Float64]) capturing -> None:
            if vals[2] > 0:
                
                poly_object.phase[0] = 0.0
                poly_object.active = True
                poly_object.freq = midicps(vals[0])
                poly_object.dur = vals[1]
                poly_object.vol = vals[2] * 0.5
                poly_object.env[1][0] = vals[3]
                poly_object.env[2][0] = vals[4]
                poly_object.env_curve = vals[5]
                poly_object.mod_freq = vals[6]
                poly_object.mod_width = vals[7]
                poly_object.start = vals[8]
                poly_object.pan = vals[9]

                
        
        self.poly.next_mgate[call_back=callback](self.voices)
        var out = MFloat[2](0.0)

        for ref voice in self.voices:
            out += voice.next()
        return out

       

       