from math import modf
import numpy as np
import music21 as m21
from user.mmm_terroir.uis.generated import roll_view
from PySide6 import QtWidgets
from user.mmm_terroir.terroir.music_symbols import *
from user.mmm_terroir.terroir.object_manipulations import *

class Roll():
    events: list
    clef: str
    onsets: np.ndarray
    pitches: np.ndarray
    durations: np.ndarray
    velocities: np.ndarray
    scale: float
    tone_division: int
    def __init__(self, onsets:list=[], pitches: list=[], durations: list=[], velocities: list=[], metadata: list=[]):
        self.onsets = np.array(onsets)
        self.pitches = np.array(pitches)
        self.durations = np.array(durations)
        self.velocities = np.array(velocities)
        self.m21_stream = m21.stream.Stream()
            
            
        
        self.tone_division = 1
        self.events = []
        
        if len(metadata) == 0:
            metadata = [[] for _ in range(len(onsets))]
        for i in range(len(onsets)):
            
            pitch = [pitches[i]]
            duration = [durations[i]]
            velocity = [velocities[i]]
            data = [metadata[i]]
            
            self.events.append([
                onsets[i], [
                    pitch,
                    duration,
                    velocity,
                    data
                ]])
            
        self.format_events()
    
    def set_onsets(self, new_onsets):
        
        for i in range(len(self.events)):
            
            self.events[i][0] = new_onsets[i]
        
        self.format_events()

    def set_pitches(self, new_pitches):
            
            for i in range(len(self.events)):
                
                self.events[i][1][0] = new_pitches[i]
            
            self.format_events()
    
    def set_durations(self, new_durations):
                
                for i in range(len(self.events)):
                    
                    self.events[i][1][1] = new_durations[i]
                
                self.format_events()
    
    def set_velocities(self, new_velocities):
            
            for i in range(len(self.events)):
                
                self.events[i][1][2] = new_velocities[i]
            
            self.format_events()
    
    def set_metadata(self, new_metadata):
                
                for i in range(len(self.events)):
                    
                    self.events[i][1][3] = new_metadata[i]
                
                self.format_events()
    
    def play(self, scheduler, mmm_audio_instance, offset=0.0, start=0.0, data_handling=None):
        """
        Schedules events to be played by an MMMAudio instance. Sends the following messages to MMMAudio:
            send_floats("poly_pitches")
            send_floats("poly_durations")
            send_floats("poly_velocites")
            send_bool("note_on_poly")
            send_floats("note_on") - For monophonic sounds
        """
        from mmm_python import PolyPal
        import asyncio
        
        self.mmm_audio_instace = mmm_audio_instance
        poly_pal = PolyPal(self.mmm_audio_instace, "poly", 128)
        
            
        async def play_poly(onset, event):
            
            data_arr = []
            
            if data_handling:
                
                for dic in event[3]:
                    data_arr.append(data_handling(dic))
                    
            else:
                data_arr += [0.0 for pitch in range(len(event[0]))]
            
            await asyncio.sleep(onset + offset - start)
            
            
            for i in range(len(event[0])):
                
        
                poly_pal.send_floats([
                    event[0][i],
                    event[1][i],
                    event[2][i]
                ] + data_arr[i])
            
            asyncio.current_task().cancel()
                        
       
        
        for event in self.events:
            
            
            if event[0] >= start:
                
                scheduler.sched(play_poly(event[0], event[1]))
                pass
        
        pass
    
    
    
    
    def play_midi(self, tempo=60):
        import music21 as m21
                
        score = m21.stream.Stream()
        score.insert(0.0, m21.tempo.MetronomeMark(number=tempo))
        tempo_adjustment = tempo/60
        for event in self.events:
            
            onset = event[0]
            pitch = event[1][0]
            duration = event[1][1]
            velocity = event[1][2]
            voices = [m21.stream.Voice() for i in range(4)]
            if isinstance(pitch, list):
                notes = []
                if not isinstance(duration, list):
                    dur = duration
                    duration = [dur for x in pitch]
                if not isinstance(event[1][2], list):
                    vel = velocity
                    velocity = [vel for x in pitch]
                    
                chord = m21.chord.Chord()
                for i, midi in enumerate(pitch):
                    new_note = m21.note.Note(midi)
                    new_note.duration = m21.duration.Duration(duration[i] * tempo_adjustment)
                    chord.add(new_note)
                
                chord.duration = m21.duration.Duration(duration[0] * tempo_adjustment)
                
                    
                score.insert(onset * tempo_adjustment, chord)
                pass
            else:
                note = m21.note.Note(pitch)
                note.duration = m21.duration.Duration(duration * tempo_adjustment)
                score.insert(onset * tempo_adjustment, note)
        # [score.insert(0, voice) for voice in voices]
        score.show('midi')

    def export_midi(self, file_name):
        from midiutil import MIDIFile
        from numpy import interp
        new_file = MIDIFile(1)
        
        
        new_file.addTempo(0, 0, 60)

        for event in self.events:
            if not isinstance(event[1][0], list):
                new_file.addNote(0, 0, event[1][0], event[0], event[1][1], int(interp(event[1][2], [0, 1], [0, 127])))
            else:
                onset = event[0]
                pitches = event[1][0]
                durations = event[1][1]
                velocities = event[1][2]
                
                
                if not isinstance(event[1][1], list):
                    dur = event[1][1]
                    durations = [dur for x in pitches]
                if not isinstance(event[1][2], list):
                    vel = event[1][2]
                    velocities = [int(interp(vel, [0, 1], [0, 127])) for x in pitches]
                
                for i, pitch in enumerate(pitches):
                        new_file.addNote(0, 0, pitch, onset, durations[i], velocities[i])
        
        with open(file_name + ".mid", "wb") as output_file:
            new_file.writeFile(output_file)

            pass
    
    def set_events(self, events) -> Roll:
        self.events = events
        self.format_events()
        return self
    
    def format_events(self):
        self.events.sort()
        combined_events = []
        unique_onsets = list(set([event[0] for event in self.events]))
        
        for onset in unique_onsets:
            combo_pitch = []
            combo_dur = []
            combo_vel = []
            combo_data = []
            for event in self.events:
                
                if event[0] == onset:
                    if isinstance(event[1][0], list):
                        combo_pitch += event[1][0]
                    else:
                        combo_pitch += [event[1][0]]
                    
                    if isinstance(event[1][1], list):
                        combo_dur += event[1][1]
                    else:
                        combo_dur += [event[1][1]]
                        
                    if isinstance(event[1][2], list):
                        combo_vel += event[1][2]
                    else:
                        combo_vel += [event[1][2]]
                    
                    if isinstance(event[1][3], list):
                        [combo_data.append(sub_dict) for sub_dict in event[1][3]]
                    else:
                        combo_data.append([event[1][3]][0])
            combined_events.append([onset, [combo_pitch, combo_dur, combo_vel, combo_data]])
        
        self.events = combined_events
        self.events.sort()
        pass
    
    def quantize(self, divisors : list = [4,], tempo=60) -> Roll:
        copy = self.copy()
        copy._quantize(divisors, tempo)
        return copy
    
    def _quantize(self, divisors : list = [4,], tempo=60):
        beat_dur = 60/tempo
        dur = self.events[len(self.events) - 1][0]
        
        for beat in range(int(dur/(beat_dur)) + 1):
            closest_div = []
            for event in self.events:
                if event[0] >= beat * beat_dur and event[0] < (beat + 1) * beat_dur:
                    min_div = [event[0] - (beat * beat_dur)/div for div in divisors]
                    closest_div.append(min_div)
                
            agg_divs = [0 for _ in range(len(divisors))]
            for divs in closest_div:
                agg_divs = np.add(agg_divs, divs)

            min_div = divisors[np.where(agg_divs == np.min(agg_divs))[0][0]]
            
            for event in self.events:
                if event[0] >= beat * beat_dur and event[0] < (beat + 1) * beat_dur:
                    
                    event[0] = round(event[0] * (min_div/beat_dur)) / min_div
                    
            
    def show(self, clefs=[Clef.TREBLE, Clef.BASS], mmm_audio_instance=None, data_handling=None):
        default = False
        if not mmm_audio_instance:
            mmm_audio_instance = MMMAudio(256 * 4, num_output_channels=2, graph_name="TerPlayerOsc", package_name="user.TerPlayers")
            mmm_audio_instance.start_audio()
            default = True
        
        if not data_handling:
            def custom_handling(data:dict):
                arr = [0.05, 0.6, 1.0]
                return arr
            data_handling = custom_handling
        
        if not QApplication.instance():
                app = QApplication([])
                
                window = QtWidgets.QMainWindow()
                ui = roll_view.Ui_MainWindow()
                ui.setupUi(window)
                ui.draw_notation(self.events, clefs)
                ui.draw_playhead()
                ui.roll = self
                ui.data_handling = data_handling
                ui.mmm_audio_instance = mmm_audio_instance
                window.show()
                ui.score_view.horizontalScrollBar().setValue(0)
                ui.score_view.verticalScrollBar().setValue(ui.score_view.verticalScrollBar().maximum() // 2)
                ui.default = True
                
                
                app.exec()
        else:
            app = QApplication.instance()
            window = QtWidgets.QMainWindow()
            ui = roll_view.Ui_MainWindow()
            ui.setupUi(window)
            ui.draw_notation(self.events, clefs)
            ui.draw_playhead()
            ui.data_handling = data_handling
            ui.roll = self
            ui.mmm_audio_instance = mmm_audio_instance
            window.show()
            ui.score_view.horizontalScrollBar().setValue(0)
            ui.score_view.verticalScrollBar().setValue(ui.score_view.verticalScrollBar().maximum() // 2)
            ui.default = True
            
            
            app.exec() #type: ignore
        pass
    
    
    def show_score(self, quantization = (2,3,4,5,6,7,8), tempo = 60):
        """
        Uses music21 to generate a score. Opens in Musescore3.
        """
        
        self.to_m21(quantization, tempo)
        score = m21.stream.Part()
        
        for element in self.m21_stream:
            score.append(element)
        score.flatten().chordify()
        m21.stream.makeNotation.splitElementsToCompleteTuplets(score)
        m21.stream.makeNotation.makeTupletBrackets(score, inPlace=True)
        m21.stream.makeNotation.consolidateCompletedTuplets(score)
        m21.stream.makeNotation.makeMeasures(score)
        # score.append(m21.meter.TimeSignature())
        # score.append(m21.key.KeySignature())
        score.show(makeNotation=True)
        
        pass
    
    
    
    def to_m21(self, quantization=(4,3), tempo=60) -> Roll:
        """
        Converts the Roll into a music21 stream.
        """
        quantized_roll = self.quantize(quantization, tempo)
        self.m21_stream = m21.stream.Stream()
        self.m21_stream.insert(0.0, m21.tempo.MetronomeMark(number=tempo))
        tempo_adjustment = tempo/60
        for event in quantized_roll.events:
            for i, pitch in enumerate(event[1][0]):
                note = m21.note.Note(pitch)
                note.duration = m21.duration.Duration(quarterLength=event[1][1][i] * tempo_adjustment)
                self.m21_stream.insert(event[0] * tempo_adjustment, note)
                # [self.m21_stream.insert(0, voice) for voice in voices]
        self.m21_stream.flatten().chordify()
        self.m21_stream.quantize(quarterLengthDivisors=quantization, processOffsets=True, processDurations=True, inPlace=True)
        self.m21_stream.makeNotation(inPlace=True)
        return self
    
    def copy(self):
        import types
        new_roll = Roll()
        new_roll.set_events(self.events.copy())
        
        return new_roll

    def to_json(self, filepath):
        """
        Saves the roll in a json file that can be played using NRT.
        """
        
        import json
        
        json_arr = []
        
        for event in self.events:
            
            json_arr.append({
                "time": event[0],
                "message": "mmm_audio_instance.send_floats",
                "key": "poly_pitches",
                "value": event[1][0]
            })
            
            json_arr.append({
                "time": event[0],
                "message": "mmm_audio_instance.send_floats",
                "key": "poly_durations",
                "value": event[1][1]
            })
            
            json_arr.append({
                "time": event[0],
                "message": "mmm_audio_instance.send_floats",
                "key": "poly_velocities",
                "value": event[1][2]
            })
            
            
            
            
            
            pass
        with open(filepath, "w") as file:
            json.dump(json_arr, file, indent=4)
        pass

    def save(self, filepath):
        """
        Saves a roll as a json that can be reloaded to another roll.
        """
        
        import json
        json_arr = []
        for event in self.events:
            json_arr.append({
                "onset": event[0],
                "pitches": event[1][0],
                "durations": event[1][1],
                "velocities": event[1][2],
                "metadata": event[1][3]
            })
        
        with open(filepath, "w") as file:
            json.dump(json_arr, file, indent=4)
    
    def load(self, filepath):
        import json

        # Open the file and load the JSON content
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Now 'data' is a standard Python dictionary or list
        new_events = []
        for dic in data:
            new_events.append(dic["onset"])
            
        new_events = list(set(new_events))
        new_events = [[onset, [[], [], [], []]] for onset in new_events]
        
        for onset in new_events:
            for dic in data:
                if dic["onset"] == onset[0]:
                    onset[1][0] += dic["pitches"]
                    onset[1][1] += dic["durations"]
                    onset[1][2] += dic["velocities"]
                    onset[1][3] += dic["metadata"]
        
        
        self.set_events(new_events)
        return self

    def legato(self) -> Roll:
        self.events.sort()
        for i, event in enumerate(self.events[:len(self.events)-1]):
            for j, dur in enumerate(event[1][1]):
                event[1][1][j] = self.events[i + 1][0] - event[0]
                
                
            
            
            
        
        return self

    def transpose(self: Roll, transposition: float) -> Roll:
        new_events = []
        
        for event in self.events:
            if isinstance(event[1][0], list):
                new_pitches = [x + transposition for x in event[1][0]]
                new_events.append([event[0],[new_pitches, event[1][1], event[1][2], event[1][3]]])

            else:
                new_events.append([event[0], [event[1][0] + transposition, event[1][1], event[1][2], event[1][3]]])
        # for event in self.pitches:
        #     if not isinstance(event, list):
        #         new_pitches.append(event + transposition)
        #     else:
        #         new_pitches.append([x + transposition for x in event])
        

        self.set_events(new_events)
        
        return self


    def onset_stretch(self:Roll, stretch_factor: float) ->Roll:
        

        
        for i in range(len(self.events)):
            self.events[i][0] *= stretch_factor
    
        
    
            
        return self


    def duration_stretch(self:Roll, stretch_factor: float) ->Roll:
        """
        Stretch the durations of an self. 

        Args:
            self: The self to be manipulated.
            stretch_factor: How much to stretch the durations.
        
        Returns:
            Returns the self.
        """
        # new_durations = [x * stretch_factor for x in self.durations]
        
        for event in self.events:
            for i, dur in enumerate(event[1][1]):
                if not isinstance(dur, list):
                    event[1][1][i] = dur * stretch_factor
                else:
                    event[1][1][i] = [subdur * stretch_factor for subdur in dur]
        # self.set_durations(new_durations)
        
        return self


    def pitch_stretch(self:Roll, stretch_factor: float, center_pitch: float) ->Roll:
        # new_pitches = []

        for i, event in enumerate(self.events):
            pitches = event[1][0]
            
            for pitch in pitches:
                if not isinstance(pitch, list):
                    self.events[i][1][0] = [ ((pitch - center_pitch) * stretch_factor) + center_pitch]
                    
                else:
                    self.events[i][1][0] = [(x - center_pitch) * stretch_factor + center_pitch for x in pitch]
                    

        
        # self.set_pitches(new_pitches)
        return self


    def pitch_stretch_hz(self:Roll, stretch_factor: float, center_pitch: float) ->Roll:
        new_pitches = []
        center_freq = midicps(center_pitch)
        for event in self.pitches:

            if not isinstance(event, list):
                new_event = (midicps(event) - center_freq) * stretch_factor
                new_pitches.append(cpsmidi(new_event + center_freq))
            else:
                new_event = [cpsmidi((midicps(x) - center_freq) * stretch_factor + center_freq) for x in event]
                new_pitches.append(new_event)
                
    
        self.set_pitches(new_pitches)
        return self


    def gliss(self:Roll, interval: float) ->Roll:
        from numpy import interp
        new_pitches = []
        for i in range(len(self.pitches)):
            event = self.pitches[i]
            
            interp_interval = interp(float(i), [float(0), float(len(self.pitches) - 1)] ,[0.0, interval])
            
            if not isinstance(event, list):
                new_pitches.append(event + interp_interval)
            else:
                new_pitches.append([x + interp_interval for x in event])

        
        self.set_pitches(new_pitches)
        return self



    def skew(self:Roll, factor: float) ->Roll:

        new_onsets = []
        np_onsets = np.array(self.onsets)
        min_val = np_onsets.min()
        max_val = np_onsets.max()
        range_val = max_val - min_val

        if factor != 0:
            shifted = np_onsets - min_val + 1
            log_values = np.log(shifted) / np.log(factor) 
            result = (log_values /log_values.max()) * range_val + min_val
            return result
        
        
    
        self.set_onsets(new_onsets)
        return self

    def dynamics(self:Roll, start=1.0, end=1.2):
        """
        Applies a change to the dynamics. This is proportional to the current dynamic.
        """
        new_dyns = []
        for i, event in enumerate(self.events):
            dynamic = event[1][2]
            new_dyns.append(np.array(dynamic) * (start + ((end - start) * (i/len(self.events)))))

        
        self.set_velocities(new_dyns)
        return self

    def quantize_pitch(self:Roll, pitch_collection: list) ->Roll:


        return self

