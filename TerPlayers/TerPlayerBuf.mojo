from mmm_audio import *
from user.TerPlayers.TerPolys import TerBufPoly


struct TerPlayerBuf(Movable, Copyable):
    var poly: Poly
    var world: World
    var voices: List[TerBufPoly]
    var messenger: Messenger
    var buffer: SIMDBuffer[1]
    def __init__(out self, world: World):
        self.world = world
        self.messenger = Messenger(self.world)
        self.poly = Poly(self.world, 128, "poly")
        self.buffer = SIMDBuffer[1]([0.0], self.world[].sample_rate).load("user/terroir/piano/c4.wav")
        self.voices = [TerBufPoly(self.world, self.buffer.sample_rate, self.buffer.data) for _ in range(128)]

        pass
 
    def next(mut self) -> MFloat[2]:
        
        def callback(mut poly_object: TerBufPoly, mut vals: List[Float64]) capturing -> None:
            if vals[2] > 0:
                print("New voice")
                poly_object.set_voice(vals)
                
        
        self.poly.next_mgate[call_back=callback](self.voices)
        var out = MFloat[2](0.0)

        for ref voice in self.voices:
            out += voice.next()
        return out

       

       