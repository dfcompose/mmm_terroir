import music21 as m21
import numpy as np


# Goals: 
#  Swap out self made tools for music21 tools when possible
# 


class Territory():
    
    def __init__(self, objects : list):
        self.objects = objects
        self.components = {
            "continuity": {
                "intra": {
                    "average": 0.65,
                    "min": 0.49,
                    "max": 1.07,
                    "std": 0.0
                    },
                "inter": {
                    1.676                    
                    }
                        },
            "density": {
                "temporal": {
                    "mean": 0.0,
                    "min": 0.0,
                    "max": 1.0
                    },
                "harmonic": {
                    "mean": 0.0,
                    "min": 0.0,
                    "max": 1.0
                    },
                "inter": {
                    "temporal": 0.517,
                    "harmonic": 0.591
                }
            },
            "pitch structure": {
                "vertical": [],
                "horizontal": [],
                "spread": 0.0,
                "hierarchy": 0.0
                },
            "dynamics": {},
            "register": {
                "bounds": [],
                "center": 60,
                "skewness": 0.0
                },
            "metricity": {},
            "periodicity": {
                "intra": {
                    "mean": 0.44,
                    "min": 0.00,
                    "max": 1.0
                },
                "inter": 0.0
                },
            "recursiveness": {
                "intra": "medium",
                "inter": "low"
                },
            "multiplicity": 1,
            "timbre": {
                "spread": 5,
                "skewness": 0.0,
                "harmonicity": 1.0
                },
            "tuning": {}
            
        }
        
        
        self.obj_aggs = {}
        
        self.obj_aggs["density.harmonic"] = []
        self.obj_aggs["density.temporal"] = []
        self.obj_aggs["periodicity"] = []
        
        for i in range(len(self.objects)):
            self.obj_aggs["obj_" + str(i)] = {
                "density.harmonic": 0,
                "density.temporal": 0,
                "periodicity": 0,
                "pitch_structure.horizontal": [],
                "pitch_structure.vertical": []
            }
        
        self._calc_temporal_densities()
        self._calc_harmonic_densities()
        self._calc_periodicity()
        self._calc_pitch_structure()
        
    def _calc_temporal_densities(self) -> None:
        
            intra_temporal = []
            object_densities = []
            
            for idx, object in enumerate(self.objects):
                timespan = object.asTimespans(classList=(m21.note.Note, m21.chord.Chord))
                onsets = sorted(list(set(ts.offset for ts in timespan)))
                
                r = 0
                deltas = []
                for i in range(len(onsets) - 1):
                    deltas.append(onsets[i + 1] - onsets[i])
                
                r = np.sum(deltas)/(len(onsets) - 1)
                
                d = 1 - (np.log10(((r * 1000 - 50)/1950) * 90 + 10) - 1) 
                self.obj_aggs["obj_" + str(idx)]["density.temporal"] = d
                intra_temporal.append(d)

            
            self.components["density"]["temporal"]["mean"] = np.mean(intra_temporal)
            self.components["density"]["temporal"]["min"] = np.min(intra_temporal)
            self.components["density"]["temporal"]["max"] = np.max(intra_temporal)
            self.components["density"]["temporal"]["std"] = np.std(intra_temporal)
            
    
    def _calc_harmonic_densities(self) -> None:
        intra_harmonic = []
        
        for idx, object in enumerate(self.objects):
            timespan = object.asTimespans(flatten=True)
            d = []
            for vert in timespan.iterateVerticalities():
                if len(vert.pitchSet) != 0:
                    d.append(len(vert.pitchSet))
            
            intra_harmonic.append(np.log(np.mean(d))/np.log(7)) 
            self.obj_aggs["obj_" + str(idx)]["density.harmonic"] = np.log(np.mean(d))/np.log(7)
            
        
        self.components["density"]["harmonic"]["mean"] = np.mean(intra_harmonic)
        self.components["density"]["harmonic"]["min"] = np.min(intra_harmonic)
        self.components["density"]["harmonic"]["max"] = np.max(intra_harmonic)
        self.components["density"]["harmonic"]["std"] = np.std(intra_harmonic)
        pass
    
    def _calc_pitch_structure(self) -> None:
        horizontal_pitches = []
        vertical_pitches = []
        all_pitches = []
        skewness = []
        self.obj_aggs["pitch_structure.horizontal"] = []
        self.obj_aggs["pitch_structure.vertical"] = []
        for idx, object in enumerate(self.objects):
            timespan = object.asTimespans(flatten=True)
            obj_vert = []
            
            for vert in timespan.iterateVerticalities():
                if len(vert.pitchSet) > 1:
                    chord = list(vert.pitchSet)
                    for i in range(len(chord) - 1):
                        obj_vert.append(abs(chord[i + 1].ps - chord[i].ps) % 12)
                        vertical_pitches.append(abs(chord[i + 1].ps - chord[i].ps) % 12)
            
            
            notes = object.flatten().notes
            for note in notes:
                all_pitches.append(note.pitch.ps)
            
            obj_int_vec = []
            for i in range(len(notes) - 1):
                
                interval = abs(notes[i + 1].pitch.ps - notes[i].pitch.ps)
                obj_int_vec.append(interval)
                horizontal_pitches.append(interval)
            
            exp_int_vec = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            vert_exp_vec = [0 for _ in range(24)]
            
            for i in list(set(obj_int_vec)):
                exp_int_vec[int((i*2) % 24)] = 1
            
            for i in list(set(obj_vert)):
                vert_exp_vec[int((i*2) % 24)] = 1
            
            self.obj_aggs["obj_" + str(idx)]["pitch_structure.horizontal"]= exp_int_vec
            self.obj_aggs["obj_" + str(idx)]["pitch_structure.vertical"]= vert_exp_vec
            
            pass
    
        for pitch in all_pitches:
            skewness.append(np.median(all_pitches) - pitch)
        
    
        self.components["pitch structure"]["vertical"] = set(vertical_pitches)
        self.components["pitch structure"]["horizontal"] = set(horizontal_pitches)
        self.components["register"]["bounds"] = [np.min(all_pitches), np.max(all_pitches)]
        self.components["register"]["center"] = np.median(all_pitches)
        self.components["register"]["skewness"] = np.mean(skewness)
        pass

    def _calc_periodicity(self):
        intra_periodicity = []
        
        for idx, object in enumerate(self.objects):
            timespan = object.asTimespans(classList=(m21.note.Note, m21.chord.Chord))
            onsets = sorted(list(set(ts.offset for ts in timespan)))
            
            p = 0
            deltas = []
            for i in range(len(onsets) - 1):
                deltas.append(onsets[i + 1] - onsets[i])
                
            for i in range(len(deltas) - 1):
                if deltas[i] == deltas[i + 1]:
                    p += 1
                elif deltas[i] % deltas[i + 1] == 0 or deltas[i + 1] % deltas[i] == 0:
                    p += 0.5
                else:
                    pass
            intra_periodicity.append(p/(len(deltas) - 1))
            self.obj_aggs["obj_" + str(idx)]["periodicity"] = p/(len(deltas) - 1)
        
        self.components["periodicity"]["intra"]["mean"] = np.mean(intra_periodicity)
        self.components["periodicity"]["intra"]["min"] = np.min(intra_periodicity)
        self.components["periodicity"]["intra"]["max"] = np.max(intra_periodicity)
        self.components["periodicity"]["intra"]["std"] = np.std(intra_periodicity)

    def get_aggs(self) -> list:
        vals = []
        for i in range(len(self.objects)):
            obj_list = []
            for component in self.obj_aggs["obj_" + str(i)]:
                if component != "pitch_structure.horizontal" and component != "pitch_structure.vertical":
                    
                    obj_list.append(self.obj_aggs["obj_" + str(i)][component])

            vals.append(obj_list)
        return vals

class Rhizome():
    def __init__(self, territories):
        self.agg_components = {}
        
        self.agg_components["density.harmonic.max"] = []
        self.agg_components["density.harmonic.mean"] = []
        self.agg_components["density.harmonic.min"] = []
        self.agg_components["density.harmonic.std"] = []
        self.agg_components["density.temporal.max"] = []
        self.agg_components["density.temporal.mean"] = []
        self.agg_components["density.temporal.min"] = []
        self.agg_components["density.temporal.std"] = []
        self.agg_components["periodicity.intra.max"] = []
        self.agg_components["periodicity.intra.mean"] = []
        self.agg_components["periodicity.intra.min"] = []
        self.agg_components["periodicity.intra.std"] = []
        
        self.territories = territories
        self._aggregate_territories()
        pass
    
    def _aggregate_territories(self):
        
        for territory in self.territories:
            ## Harmonic density
            self.agg_components["density.harmonic.max"].append(territory.components["density"]["harmonic"]["max"])
            self.agg_components["density.harmonic.mean"].append(territory.components["density"]["harmonic"]["mean"])
            self.agg_components["density.harmonic.min"].append(territory.components["density"]["harmonic"]["min"])
            self.agg_components["density.harmonic.std"].append(territory.components["density"]["harmonic"]["std"])
            
            ## Temporal Density
            self.agg_components["density.temporal.max"].append(territory.components["density"]["temporal"]["max"])
            self.agg_components["density.temporal.mean"].append(territory.components["density"]["temporal"]["mean"])
            self.agg_components["density.temporal.min"].append(territory.components["density"]["temporal"]["min"])
            self.agg_components["density.temporal.std"].append(territory.components["density"]["temporal"]["std"])
            
            ## Periodicity
            self.agg_components["periodicity.intra.max"].append(territory.components["periodicity"]["intra"]["max"])
            self.agg_components["periodicity.intra.mean"].append(territory.components["periodicity"]["intra"]["mean"])
            self.agg_components["periodicity.intra.min"].append(territory.components["periodicity"]["intra"]["min"])
            self.agg_components["periodicity.intra.std"].append(territory.components["periodicity"]["intra"]["std"])
            pass
        
        
        pass

    def get_aggs(self) -> list:
        vals = []
        for key in self.agg_components:
            vals.append(self.agg_components[key])
        return vals