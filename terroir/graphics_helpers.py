from mmm_terroir.terroir.music_symbols import *

import mmm_terroir.terroir.ter_theme as theme
from math import modf


def get_pitch_class(in_pitch, in_cents) -> tuple:
    line = 0
    accidental = Accidental.NATURAL
    pitch_class = in_pitch % 12
    cents = round(in_cents * 2)/2
    match pitch_class:
                case 0:
                    line = 0
                    if cents == 0.50:
                        accidental = Accidental.QUARTER_SHARP
                case 1:
                    line = 0
                    accidental =  Accidental.SHARP
                    if cents == 0.50:
                        accidental = Accidental.THREE_QUARTER_SHARP
                case 2:
                    line = 0.5
                    if cents == 0.50:
                        accidental = Accidental.QUARTER_SHARP
                case 3:
                    line = 0.5
                    accidental =  Accidental.SHARP
                    if cents == 0.50:
                        accidental = Accidental.THREE_QUARTER_SHARP
                case 4:
                    line = 1.0
                    if cents == 0.50:
                        accidental = Accidental.QUARTER_SHARP
                case 5:
                    line = 1.5
                    if cents == 0.50:
                        accidental = Accidental.QUARTER_SHARP
                case 6:
                    line = 1.5
                    accidental =  Accidental.SHARP
                    if cents == 0.50:
                        accidental = Accidental.THREE_QUARTER_SHARP
                case 7:
                    line = 2.0
                    if cents == 0.50:
                        accidental = Accidental.QUARTER_SHARP
                case 8:
                    line = 2.0
                    accidental =  Accidental.SHARP
                    if cents == 0.50:
                        accidental = Accidental.THREE_QUARTER_SHARP
                case 9: 
                    line = 2.5
                    if cents == 0.50:
                        accidental = Accidental.QUARTER_SHARP
                case 10:
                    line = 2.5
                    accidental =  Accidental.SHARP
                    if cents == 0.50:
                        accidental = Accidental.THREE_QUARTER_SHARP
                case 11:
                    line = 3.0
                    if cents == 0.50:
                        accidental = Accidental.QUARTER_SHARP
   
    return (line, accidental)







def place_ledgers(onset, midicent, clefs):
    ledgers = []
    sorted_clefs = sorted(clefs)
    cents, pitch = modf(midicent)
    octave = divmod(midicent, 12)[0]
    line, accidental = get_pitch_class(pitch, cents)
    octave_displacement = (octave - 5) * 3.5
    cast_note = line + octave_displacement
    line_spacing = 10
    match sorted_clefs:
        case [Clef.TREBLE]:
            
            
            if cast_note >= 402 and cast_note % line_spacing == 0:
                
                y_pos = cast_note;
                while y_pos >= 402:
                    
                    ledgers.append(
                        [onset, y_pos]
                        )
                    y_pos -= line_spacing
            elif cast_note - 6 >= 402:
                y_pos = cast_note - 6
                while y_pos >= 402:
                                    
                    ledgers.append(
                        [onset, y_pos]
                                )
                    y_pos -= line_spacing

            if cast_note <= 348 and cast_note % line_spacing == 0:
                
                y_pos = cast_note;
                while y_pos <= 348:
                    
                    ledgers.append(
                        [onset, y_pos]
                                )
                    y_pos += line_spacing
            elif cast_note + 6 <= 348:
                y_pos = cast_note + 6
                while y_pos <= 348:
                                    
                    ledgers.append(
                            [onset, y_pos]
                                    )
                    y_pos += line_spacing


        case [Clef.TREBLE, Clef.TREBLE_8VA]:


            if cast_note >= 462:
                y_pos = cast_note;
                if y_pos % line_spacing != 0:
                    y_pos -= 6
                while y_pos >= 462:
                                    
                    ledgers.append(
                        [onset, y_pos]
                                )
                    y_pos -= line_spacing
            
            if cast_note >= 402 and cast_note <= 432 and cast_note % line_spacing == 0:
                
                y_pos = cast_note;
                while y_pos >= 402:
                    
                    ledgers.append(
                        [onset, y_pos]
                                )
                    
                    y_pos -= line_spacing
            elif cast_note - 6 >= 402 and cast_note - 6 <= 420:
                y_pos = cast_note - 6
                while y_pos >= 402:
                                    
                    ledgers.append(
                        [onset, y_pos]
                                )
                    
                    y_pos -= line_spacing

            if cast_note <= 348 and cast_note % line_spacing == 0:
                
                y_pos = cast_note;
                while y_pos <= 348:
                    
                    ledgers.append(
                        [onset, y_pos]
                                )
                    
                    y_pos += line_spacing
            elif cast_note + 6 <= 348:
                y_pos = cast_note + 6
                while y_pos <= 348:
                                    
                    ledgers.append(
                        [onset, y_pos]
                                )
                    
                    y_pos += line_spacing

        case [Clef.TREBLE, Clef.TREBLE_8VA, Clef.BASS]:

            # 8va
            if cast_note >= 462:
                y_pos = cast_note;
                if y_pos % line_spacing != 0:
                    y_pos -= 6
                while y_pos >= 462:
                                    
                    ledgers.append(
                        [onset, y_pos]
                                )
                    
                    y_pos -= line_spacing

            # Treble Clef
            if cast_note >= 402 and cast_note <= 432 and cast_note % line_spacing == 0:
                            
                y_pos = cast_note;
                if y_pos % line_spacing != 0:
                    y_pos -= 6
                while y_pos >= 402:
                    
                    ledgers.append(
                        [onset, y_pos]
                                )
                    y_pos -= line_spacing


            
            # Middle C
            if cast_note == 348:
                
                y_pos = cast_note;
                while y_pos <= 348:
                    
                    ledgers.append(
                        [onset, y_pos]
                                )
                    
                    y_pos += line_spacing

            # Bass Clef
            y_pos = cast_note
            if cast_note % line_spacing != 0:
                cast_note += 6
            if cast_note <= 308:
                
                y_pos = cast_note;
                while y_pos <= 308:
                    
                    ledgers.append(
                        [onset, y_pos]
                                )
                    
                    y_pos += line_spacing

        case [Clef.BASS]:
            pass

        case [Clef.BASS, Clef.BASS_8VB]:
            pass

        case [Clef.TREBLE, Clef.BASS]:
            
            # Treble Clef
            y_pos = cast_note
            if y_pos % 1.0 != 0:
                y_pos -= 0.5
        
            while y_pos >= 6.0:
                
                ledgers.append(
                    [onset, y_pos * line_spacing]
                            )
                y_pos -= 1

            # Middle C
            
            
            if cast_note == 0:
                
                    
                ledgers.append(
                    [onset, 0]
                            )
                    

            # Bass Clef
            y_pos = cast_note
            if y_pos % 1.0 != 0:
                y_pos += 0.5
            
            while y_pos <= -6:
                
                ledgers.append(
                    [onset, y_pos * line_spacing]
                            )
                y_pos += 1
            
            pass


    # [print(ledger.y) for ledger in ledgers]
    return ledgers     



# def place_accidental(acc, line, window, onset):
#     x_offset = 83
#     accidental = None
    
#     match acc:
#         case 'sharp':
#             accidental = pyglet.text.Label(Accidental.SHARP,
#                                                         font_name='Bravura',
#                                                         font_size=36,
#                                                         x=onset + x_offset, y=line,
#                                                         anchor_x='center', anchor_y='center',
#                                                         color=theme.ledger_lines)
#         case 'qsharp':
#             accidental = pyglet.text.Label(Accidental.QUARTER_SHARP,
#                                                         font_name='Bravura',
#                                                         font_size=36,
#                                                         x=onset + x_offset, y=line,
#                                                         anchor_x='center', anchor_y='center',
#                                                         color=theme.ledger_lines)
#         case 'tqsharp':
#             accidental = pyglet.text.Label(Accidental.THREE_QUARTER_SHARP,
#                                                         font_name='Bravura',
#                                                         font_size=36,
#                                                         x=onset + x_offset, y=line,
#                                                         anchor_x='center', anchor_y='center',
#                                                         color=theme.ledger_lines)
            

#     if accidental == None:
#         return
#     else:
#         return accidental
