from mmm_terroir import *

roll = Roll()

roll.set_events(
    [
        [i, [[60 + i], [1], [0.5], [{}]]] for i in range(12)
    ]
)

roll.show()
