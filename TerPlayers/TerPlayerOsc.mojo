from mmm_audio import *
from user.TerPlayers.TerPolys import TerOscPoly
from user.synths.ObjectBasedAudio import *

struct TerPlayerOsc(Movable, Copyable):
    var poly: Poly
    var world: World
    var voices: List[TerOscPoly]
    var messenger: Messenger
    # var spat : SpatialField2D[Panning2D.az, 4, 2, 2]
    
    def __init__(out self, world: World):
        self.world = world
        self.messenger = Messenger(self.world)
        
        self.poly = Poly(self.world, 128, "poly")
        self.voices = [TerOscPoly(self.world) for _ in range(128)]
        var array : Array[Float64, 2] = [-0.25 * pi, 0.25 * pi]
        # self.spat = SpatialField2D[Panning2D.az, 4, 2, 2](
        #     world, array, "spat"
        # )
        
        pass
 
    def next(mut self) -> MFloat[2]:

    
        def callback(mut poly_object: TerOscPoly, mut vals: List[Float64]) capturing -> None:
            if vals[2] > 0:
               
                poly_object.freq = midicps(vals[0])
                poly_object.dur = vals[1]
                poly_object.vol = vals[2] * 0.5
                poly_object.env[1][0] = vals[3]
                poly_object.env[2][0] = vals[4]
                poly_object.env_curve = vals[5]

                
        # _ = self.spat.next()
        self.poly.next_mgate[call_back=callback](self.voices)
        var out = MFloat[2](0.0)

        for ref voice in self.voices:
            out += voice.next()
        # out = self.spat.next()
        
        return out

       

       