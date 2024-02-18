import threading
import time
import pygame
import sys
import mido
import mido.backends.pygame
mido.set_backend('mido.backends.pygame')
from tkinter import *
import tkinter.ttk as tk
from customtkinter import *
from tkinter import messagebox
from idlelib.tooltip import Hovertip
import pygame.midi
from pynput import keyboard
def close():
    try:
        root.destroy()
    except:
        pass
    for controller in root.joysticks.values():
        controller.stop_rumble()
    pygame.joystick.quit()
    pygame.quit()
    sys.exit()
def get_resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
class HapticDrum:
    def __init__(self, envelope, env_808,  ch, note_num):
        self.name=envelope
        self.name2=env_808
        self.sound=pygame.mixer.Sound(get_resource_path(self.name+'.wav'))
        if self.name2 is not None:
            self.sound2=pygame.mixer.Sound(get_resource_path(self.name2+'.wav'))
        self.channel=pygame.mixer.Channel(ch)
        self.note=note_num
    def play_haptic_envelope(self):
        if midiselect.get()=='Internal Audio':
            self.channel.set_volume(volSlider.get()/127)
            if root.kit_808:
                if self.name2 is not None:
                    self.channel.play(self.sound2)
            else:
                self.channel.play(self.sound)
        else:
            root.ports[midiselect.get()].send(mido.Message('note_on', channel=9, note=self.note, velocity=127))
    def trigger(self):
        threading.Thread(target=self.play_haptic_envelope).start()
    def note_off(self):
        if not midiselect.get()=='Internal Audio':
            root.ports[midiselect.get()].send(mido.Message('note_off', channel=9, note=self.note, velocity=127))
    def trigger_once(self):
        self.play_haptic_envelope()
        self.note_off()
# Create Drum Objects
pygame.mixer.init()
pygame.display.init()
pygame.mixer.set_num_channels(28)
pygame.joystick.init()
bass_drum = HapticDrum('bass_drum','BD', 0, 36)
snare_drum = HapticDrum('snare_drum','SD', 1, 38)
tom_toms = HapticDrum('low_tom', 'LT', 2, 43)
hi_hat = HapticDrum('hi_hat_closed','CH', 3, 42)
ride_cymbal = HapticDrum('ride_cymbal',None, 4, 51)
ride_cymbal_2 = HapticDrum('ride_cymbal',None, 13, 59)
crash_cymbal = HapticDrum('crash_cymbal','CY', 5, 49)
crash_cymbal_2 = HapticDrum('crash_cymbal','CY', 12, 57)
mid_tom = HapticDrum('mid_tom','MT', 6, 45)
hi_tom = HapticDrum('hi_tom','HT', 7, 48)
floor_tom = HapticDrum('low_tom','LT', 11, 41)
hi_hat_open = HapticDrum('hi_hat_open','OH', 8, 46)
hi_hat_foot = HapticDrum('hi_hat_foot','CH', 9, 44)
side_stick = HapticDrum('side_stick','RS', 10, 37)
hi_bongo=HapticDrum('hi_bongo',None, 14, 60)
low_bongo=HapticDrum('low_bongo',None, 15, 61)
hi_conga=HapticDrum('hi_conga',None, 16, 63)
low_conga=HapticDrum('low_conga',None, 17, 64)
hi_timbale=HapticDrum('hi_timbale',None, 18, 65)
low_timbale=HapticDrum('low_timbale',None, 19, 66)
maracas=HapticDrum('maracas',None, 21, 70)
claves=HapticDrum('claves',None, 22, 75)
hi_woodblock=HapticDrum('hi_woodblock',None, 23, 76)
low_woodblock=HapticDrum('low_woodblock',None, 24, 56)
m_triangle=HapticDrum('m_triangle',None, 25, 80)
triangle=HapticDrum('triangle',None, 26, 81)
shaker=HapticDrum('shaker',None, 20, 82)
vibraslap=HapticDrum('vibraslap',None, 27, 58)
root = CTk()
# Button Functions
def trigger_bass_drum():
    bass_drum.trigger()

def trigger_snare_drum():
    snare_drum.trigger()

def trigger_tom_toms():
    tom_toms.trigger()

def trigger_hi_hat():
    hi_hat.trigger()

def trigger_ride_cymbal():
    ride_cymbal.trigger()

def trigger_crash_cymbal():
    crash_cymbal.trigger()
def check_status():
    low_bat_count=0
    crit_bat_count=0
    for event in pygame.event.get():
        if event.type == pygame.JOYDEVICEADDED:
            joy = pygame.joystick.Joystick(event.device_index)
            tabview.add('Cnt. '+str(joy.get_instance_id()))
            tab=tabview.tab('Cnt. '+str(joy.get_instance_id()))
            root.joysticks[joy.get_instance_id()]=joy
            CTkLabel(tab, text=joy.get_name()).pack()
            CTkLabel(tab, text='Battery:').pack()
            statusLabel=CTkLabel(tab, text='Unknown', text_color=('grey', 'grey'))
            statusLabel.pack()
            root.statuses[joy.get_instance_id()]=statusLabel
            checkbox=CTkSwitch(tab, text='Bind controller to drums')
            checkbox.pack()
            mode=CTkSwitch(tab, text='Use for additional percussion')
            mode.pack()
            root.checkboxes[joy.get_instance_id()]=checkbox
            if 'Nintendo' in joy.get_name():
                checkbox.select()
                root.splitcymbals[joy.get_instance_id()]=bool(check1.get())
                root.swapab[joy.get_instance_id()]=bool(check.get())
                if bool(check.get()) and bool(check1.get()):
                    CTkLabel(tab, text='Trigger kick drum with crash cymbal (drumset mode only)').pack()
                    checkbox1=CTkSegmentedButton(tab, values=['Off', 'L Crash', 'R Crash'])
                    checkbox1.pack()
                    checkbox1.set("Off")
                    CTkLabel(tab, text='Mapping (A/B & X/Y swapped):\nB: Snare/High Bongo\nA: Kick/Low Bongo\nY: Low Tom/Low Conga\nDpad Right: Mid Tom/Low Timbale\nDpad Left: High Tom/High Timbale\nX: Pedal Hi-Hat/High Conga\nDpad Up: Open Hi-Hat/Open Triangle\nDpad Down: Closed Hi-Hat/Mute Triangle\nR: Ride Cymbal 1/Woodblock\nL: Ride Cymbal 2/Cowbell\nZL: Crash Cymbal 1/Vibraslap\nZR: Crash Cymbal 2/Maracas\nL Stick (press): Side Stick/Clave\nR Stick (press): Floor Tom/Shaker\n-/+: Volume\nL Stick Horizontal: Pan (external MIDI out only)\nR Stick Vertical: Pitch Bend (external MIDI out only)').pack()
                elif bool(check.get()) and not bool(check1.get()):
                    checkbox1=CTkSwitch(tab, text='Trigger kick drum with crash cymbal (drumset mode only)')
                    checkbox1.pack()
                    CTkLabel(tab, text='Mapping (A/B & X/Y swapped):\nB: Snare/High Bongo\nA: Kick/Low Bongo\nY: Low Tom/Low Conga\nDpad Right: Mid Tom/Low Timbale\nDpad Left: High Tom/High Timbale\nX: Pedal Hi-Hat/High Conga\nDpad Up: Open Hi-Hat/Open Triangle\nDpad Down: Closed Hi-Hat/Mute Triangle\nR: Ride Cymbal/Woodblock\nL: Crash Cymbal/Cowbell\nL Stick (press): Side Stick/Clave\nR Stick (press): Floor Tom/Shaker\n-/+: Volume\nL Stick Horizontal: Pan (external MIDI out only)\nR Stick Vertical: Pitch Bend (external MIDI out only)').pack()
                elif bool(check1.get()) and not bool(check.get()):
                    CTkLabel(tab, text='Trigger kick drum with crash cymbal (drumset mode only)').pack()
                    checkbox1=CTkSegmentedButton(tab, values=['Off', 'L Crash', 'R Crash'])
                    checkbox1.pack()
                    checkbox1.set("Off")
                    CTkLabel(tab, text='Mapping:\nA: Snare/High Bongo\nB: Kick/Low Bongo\nX: Low Tom/Low Conga\nDpad Right: Mid Tom/Low Timbale\nDpad Left: High Tom/High Timbale\nY: Pedal Hi-Hat/High Conga\nDpad Up: Open Hi-Hat/Open Triangle\nDpad Down: Closed Hi-Hat/Mute Triangle\nR: Ride Cymbal 1/Woodblock\nL: Ride Cymbal 2/Cowbell\nZL: Crash Cymbal 1/Vibraslap\nZR: Crash Cymbal 2/Maracas\nL Stick (press): Side Stick/Clave\nR Stick (press): Floor Tom/Shaker\n-/+: Volume\nL Stick Horizontal: Pan (external MIDI out only)\nR Stick Vertical: Pitch Bend (external MIDI out only)').pack()
                else:
                    checkbox1=CTkSwitch(tab, text='Trigger kick drum with crash cymbal (drumset mode only)')
                    checkbox1.pack()
                    CTkLabel(tab, text='Mapping:\nA: Snare/High Bongo\nB: Kick/Low Bongo\nX: Low Tom/Low Conga\nDpad Right: Mid Tom/Low Timbale\nDpad Left: High Tom/High Timbale\nY: Pedal Hi-Hat/High Conga\nDpad Up: Open Hi-Hat/Open Triangle\nDpad Down: Closed Hi-Hat/Mute Triangle\nR: Ride Cymbal/Woodblock\nL: Crash Cymbal/Cowbell\nL Stick (press): Side Stick/Clave\nR Stick (press): Floor Tom/Shaker\n-/+: Volume\nL Stick Horizontal: Pan (external MIDI out only)\nR Stick Vertical: Pitch Bend (external MIDI out only)').pack()
            elif 'Xbox' in joy.get_name():
                checkbox1=CTkSwitch(tab, text='Trigger kick drum with crash cymbal (drumset mode only)')
                checkbox1.pack()
                CTkLabel(tab, text='Mapping:\nA: Snare/High Bongo\nB: Kick/Low Bongo\nX: Low Tom/Low Conga\nDpad Right: Mid Tom/Low Timbale\nDpad Left: High Tom/High Timbale\nY: Pedal Hi-Hat/High Conga\nDpad Up: Open Hi-Hat/Open Triangle\nDpad Down: Closed Hi-Hat/Mute Triangle\nRB: Ride Cymbal/Woodblock\nLB: Crash Cymbal/Cowbell\nL Stick (press): Side Stick/Clave\nR Stick (press): Floor Tom/Shaker\nL Stick Horizontal: Pan (external MIDI out only)\nR Stick Vertical: Pitch Bend (external MIDI out only)').pack()
            elif 'PS4' in joy.get_name():
                checkbox1=CTkSwitch(tab, text='Trigger kick drum with crash cymbal (drumset mode only)')
                checkbox1.pack()
                checkbox.select()
                CTkLabel(tab, text='Mapping:\nCross: Snare/High Bongo\nCircle: Kick/Low Bongo\nSquare: Low Tom/Low Conga\nDpad Right: Mid Tom/Low Timbale\nDpad Left: High Tom/High Timbale\nTriangle: Pedal Hi-hat\nDpad Up: Open Hi-Hat/Open Triangle\nDpad Down: Closed Hi-Hat/Mute Triangle\nR1: Ride Cymbal/Woodblock\nL1: Crash Cymbal/Cowbell\nL Stick (press): Side Stick/Clave\nR Stick (press): Floor Tom/Shaker\nL Stick Horizontal: Pan (external MIDI out only)\nR Stick Vertical: Pitch Bend (external MIDI out only)').pack()
            elif joy.get_name()=='Sony Interactive Entertainment Wireless Controller':
                checkbox1=CTkSwitch(tab, text='Trigger kick drum with crash cymbal')
                checkbox1.pack()
                checkbox.select()
                CTkLabel(tab, text='Mapping:\nCross: Snare/High Bongo\nCircle: Kick/Low Bongo\nSquare: Low Tom/Low Conga\nDpad Right: Mid Tom/Low Timbale\nDpad Left: High Tom/High Timbale\nTriangle: Pedal Hi-hat\nDpad Up: Open Hi-Hat/Open Triangle\nDpad Down: Closed Hi-Hat/Mute Triangle\nR1: Ride Cymbal/Woodblock\nL1: Crash Cymbal/Cowbell\nL Stick (press): Side Stick/Clave\nR Stick (press): Floor Tom/Shaker\nL Stick Horizontal: Pan (external MIDI out only)\nR Stick Vertical: Pitch Bend (external MIDI out only)').pack()
            else:
                checkbox1=CTkSwitch(tab, text='Trigger kick drum with crash cymbal (drumset mode only)')
                checkbox1.pack()
                if joy.get_numhats()>0:
                    CTkLabel(tab, text='Mapping:\nButton 0: Snare/High Bongo\nButton 1: Kick/Low Bongo\nButton 2: Low Tom/Low Conga\nDpad Right: Mid Tom/Low Timbale\nDpad Left: High Tom/High Timbale\nButton 3: Pedal Hi-Hat/High Conga\nDpad Up: Open Hi-Hat/Open Triangle\nDpad Down: Closed Hi-Hat/Mute Triangle\nButton 4: Crash Cymbal/Cowbell\nButton 5: Ride Cymbal/Woodblock\nButton 8: Side Stick/Clave\nButton 9: Floor Tom/Shaker\nAxis 0: Pan (external MIDI out only)\nAxis 3: Pitch Bend (external MIDI out only)').pack()
                else:
                    CTkLabel(tab, text='Mapping:\nButton 0: Snare/High Bongo\nButton 1: Kick/Low Bongo\nButton 2: Low Tom/Low Conga\nButton 3: Pedal Hi-Hat/High Conga\nButton 4: Crash Cymbal/Low Woodblock\nButton 5: Ride Cymbal/Woodblock\nButton 8: Side Stick/Clave\nButton 14: Closed Hi-Hat/Mute Triangle\nButton 15: Open Hi-Hat/Open Triangle\nAxis 0: Pan (external MIDI out only)').pack()
            root.checkboxes1[joy.get_instance_id()]=checkbox1
            Hovertip(mode, 'Selects drum mode.\nON: Buttons trigger additional percussion, or the second sound in the mapping.\nOFF: Buttons trigger normal drumset sounds, or the first sound in the mapping.')
            root.modes[joy.get_instance_id()]=mode
            if midiselect.get()=='Internal Audio' and root.kit_808:
                mode.configure(state='disabled')
            tabview.set('Cnt. '+str(joy.get_instance_id()))
        if event.type == pygame.JOYDEVICEREMOVED:
            print(event)
            root.checkboxes[event.instance_id].deselect()
            tabview.delete('Cnt. '+str(event.instance_id))
            del root.joysticks[event.instance_id]
            del root.statuses[event.instance_id]
            del root.modes[event.instance_id]
        if event.type == pygame.JOYBUTTONDOWN and (root.focus_displayof() is not None) and bool(root.checkboxes[event.instance_id].get()):
            name=root.joysticks[event.instance_id].get_name()
            perc=bool(root.modes[event.instance_id].get())
            print(event)
            try:
                if name=='Nintendo Switch Pro Controller':
                    if event.button == 0:
                        if root.swapab[event.instance_id]:
                            if perc:
                                low_bongo.trigger()
                            else:
                                trigger_bass_drum()
                        else:
                            if perc:
                                hi_bongo.trigger()
                            else:
                                trigger_snare_drum()
                    elif event.button == 1:
                        if root.swapab[event.instance_id]:
                            if perc:
                                hi_bongo.trigger()
                            else:
                                trigger_snare_drum()
                        else:
                            if perc:
                                low_bongo.trigger()
                            else:
                                trigger_bass_drum()
                    elif event.button == 2:
                        if root.swapab[event.instance_id]:
                            if perc:
                                hi_conga.trigger()
                            else:
                                hi_hat_foot.trigger()
                        else:
                            if perc:
                                low_conga.trigger()
                            else:
                                trigger_tom_toms()
                    elif event.button == 3:
                        if root.swapab[event.instance_id]:
                            if perc:
                                low_conga.trigger()
                            else:
                                trigger_tom_toms()
                        else:
                            if perc:
                                hi_conga.trigger()
                            else:
                                hi_hat_foot.trigger()
                    elif event.button == 10:
                        if perc:
                            hi_woodblock.trigger()
                        else:
                            trigger_ride_cymbal()
                    elif event.button == 9:
                        if perc:
                            low_woodblock.trigger()
                        else:
                            if root.splitcymbals[event.instance_id]:
                                ride_cymbal_2.trigger()
                            else:
                                if bool(root.checkboxes1[event.instance_id].get()):
                                    trigger_bass_drum()
                                trigger_crash_cymbal()
                    elif event.button == 11:
                        if perc:
                            triangle.trigger()
                        else:
                            hi_hat_open.trigger()
                    elif event.button == 12:
                        if perc:
                            m_triangle.trigger()
                        else:
                            trigger_hi_hat()
                    elif event.button == 13:
                        if perc:
                            hi_timbale.trigger()
                        else:
                            hi_tom.trigger()
                    elif event.button == 14:
                        if perc:
                            low_timbale.trigger()
                        else:
                            mid_tom.trigger()
                    elif event.button == 7:
                        if perc:
                            claves.trigger()
                        else:
                            side_stick.trigger()
                    elif event.button == 8:
                        if perc:
                            shaker.trigger()
                        else:
                            floor_tom.trigger()
                    elif event.button==4:
                        volSlider.set(volSlider.get()-4)
                        if not midiselect.get()=='Internal Audio':
                            root.ports[midiselect.get()].send(mido.Message('control_change', channel=9, control=7, value=int(volSlider.get())))
                    elif event.button==6:
                        volSlider.set(volSlider.get()+4)
                        if not midiselect.get()=='Internal Audio':
                            root.ports[midiselect.get()].send(mido.Message('control_change', channel=9, control=7, value=int(volSlider.get())))
                elif 'Xbox' in name:
                    if event.button == 0:
                        if perc:
                            hi_bongo.trigger()
                        else:
                            trigger_snare_drum()
                    elif event.button == 1:
                        if perc:
                            low_bongo.trigger()
                        else:
                            trigger_bass_drum()
                    elif event.button == 2:
                        if perc:
                            low_conga.trigger()
                        else:
                            trigger_tom_toms()
                    elif event.button == 3:
                        if perc:
                            hi_conga.trigger()
                        else:
                            hi_hat_foot.trigger()
                    elif event.button == 5:
                        if perc:
                            hi_woodblock.trigger()
                        else:
                            trigger_ride_cymbal()
                    elif event.button == 4:
                        if perc:
                            low_woodblock.trigger()
                        else:
                            if bool(root.checkboxes1[event.instance_id].get()):
                                trigger_bass_drum()
                            trigger_crash_cymbal()
                    elif event.button == 8:
                        if perc:
                            claves.trigger()
                        else:
                            side_stick.trigger()
                    elif event.button == 9:
                        if perc:
                            shaker.trigger()
                        else:
                            floor_tom.trigger()
                elif name=='PS4 Controller':
                    if event.button == 0:
                        if perc:
                            hi_bongo.trigger()
                        else:
                            trigger_snare_drum()
                    elif event.button == 1:
                        if perc:
                            low_bongo.trigger()
                        else:
                            trigger_bass_drum()
                    elif event.button == 2:
                        if perc:
                            low_conga.trigger()
                        else:
                            trigger_tom_toms()
                    elif event.button == 3:
                        if perc:
                            hi_conga.trigger()
                        else:
                            hi_hat_foot.trigger()
                    elif event.button == 10:
                        if perc:
                            hi_woodblock.trigger()
                        else:
                            trigger_ride_cymbal()
                    elif event.button == 9:
                        if perc:
                            low_woodblock.trigger()
                        else:
                            if bool(root.checkboxes1[event.instance_id].get()):
                                trigger_bass_drum()
                            trigger_crash_cymbal()
                        trigger_crash_cymbal()
                    elif event.button == 11:
                        if perc:
                            triangle.trigger()
                        else:
                            hi_hat_open.trigger()
                    elif event.button == 12:
                        if perc:
                            m_triangle.trigger()
                        else:
                            trigger_hi_hat()
                    elif event.button == 13:
                        if perc:
                            hi_timbale.trigger()
                        else:
                            hi_tom.trigger()
                    elif event.button == 14:
                        if perc:
                            low_timbale.trigger()
                        else:
                            mid_tom.trigger()
                    elif event.button == 7:
                        if perc:
                            claves.trigger()
                        else:
                            side_stick.trigger()
                    elif event.button == 8:
                        if perc:
                            shaker.trigger()
                        else:
                            floor_tom.trigger()
                elif name=='Sony Interactive Entertainment Wireless Controller':
                    if event.button == 0:
                        if perc:
                            hi_bongo.trigger()
                        else:
                            trigger_snare_drum()
                    elif event.button == 1:
                        if perc:
                            low_bongo.trigger()
                        else:
                            trigger_bass_drum()
                    elif event.button == 2:
                        if perc:
                            low_conga.trigger()
                        else:
                            trigger_tom_toms()
                    elif event.button == 3:
                        if perc:
                            hi_conga.trigger()
                        else:
                            hi_hat_foot.trigger()
                    elif event.button == 5:
                        if perc:
                            hi_woodblock.trigger()
                        else:
                            trigger_ride_cymbal()
                    elif event.button == 4:
                        if perc:
                            low_woodblock.trigger()
                        else:
                            if bool(root.checkboxes1[event.instance_id].get()):
                                trigger_bass_drum()
                            trigger_crash_cymbal()
                        trigger_crash_cymbal()
                    elif event.button == 11:
                        if perc:
                            claves.trigger()
                        else:
                            side_stick.trigger()
                    elif event.button == 12:
                        if perc:
                            shaker.trigger()
                        else:
                            floor_tom.trigger()
                else:
                    if event.button == 0:
                        if perc:
                            hi_bongo.trigger()
                        else:
                            trigger_snare_drum()
                    elif event.button == 1:
                        if perc:
                            low_bongo.trigger()
                        else:
                            trigger_bass_drum()
                    elif event.button == 2:
                        if perc:
                            low_conga.trigger()
                        else:
                            trigger_tom_toms()
                    elif event.button == 3:
                        if perc:
                            hi_conga.trigger()
                        else:
                            hi_hat_foot.trigger()
                    elif event.button == 5:
                        if perc:
                            hi_woodblock.trigger()
                        else:
                            trigger_ride_cymbal()
                    elif event.button == 4:
                        if perc:
                            low_woodblock.trigger()
                        else:
                            if bool(root.checkboxes1[event.instance_id].get()):
                                trigger_bass_drum()
                            trigger_crash_cymbal()
                    elif event.button == 15 and root.joysticks[event.instance_id].get_numhats()==0:
                        if perc:
                            triangle.trigger()
                        else:
                            hi_hat_open.trigger()
                    elif event.button == 14 and root.joysticks[event.instance_id].get_numhats()==0:
                        if perc:
                            m_triangle.trigger()
                        else:
                            trigger_hi_hat()
                    elif event.button == 8:
                        if perc:
                            claves.trigger()
                        else:
                            side_stick.trigger()
                    elif event.button == 9:
                        if perc:
                            shaker.trigger()
                        else:
                            floor_tom.trigger()
            except:
                pass
        if event.type == pygame.JOYBUTTONUP and bool(root.checkboxes[event.instance_id].get()):
            name=root.joysticks[event.instance_id].get_name()
            try:
                if name=='Nintendo Switch Pro Controller':
                    if event.button == 0:
                        if root.swapab[event.instance_id]:
                            low_bongo.note_off()
                            bass_drum.note_off()
                        else:
                            hi_bongo.note_off()
                            snare_drum.note_off()
                    elif event.button == 1:
                        if root.swapab[event.instance_id]:
                            hi_bongo.note_off()
                            snare_drum.note_off()
                        else:
                            low_bongo.note_off()
                            bass_drum.note_off()
                    elif event.button == 2:
                        if root.swapab[event.instance_id]:
                            hi_conga.note_off()
                            hi_hat_foot.note_off()
                        else:
                            low_conga.note_off()
                            tom_toms.note_off()
                    elif event.button == 3:
                        if root.swapab[event.instance_id]:
                            low_conga.note_off()
                            tom_toms.note_off()
                        else:
                            hi_conga.note_off()
                            hi_hat_foot.note_off()
                    elif event.button == 10:
                        hi_woodblock.note_off()
                        ride_cymbal.note_off()
                    elif event.button == 9:
                        low_woodblock.note_off()
                        if root.splitcymbals[event.instance_id]:
                            ride_cymbal_2.note_off()
                        else:
                            bass_drum.note_off()
                            crash_cymbal.note_off()
                    elif event.button == 11:
                        triangle.note_off()
                        hi_hat_open.note_off()
                    elif event.button == 12:
                        m_triangle.note_off()
                        hi_hat.note_off()
                    elif event.button == 13:
                        hi_timbale.note_off()
                        hi_tom.note_off()
                    elif event.button == 14:
                        low_timbale.note_off()
                        mid_tom.note_off()
                    elif event.button == 7:
                        claves.note_off()
                        side_stick.note_off()
                    elif event.button == 8:
                        shaker.note_off()
                        floor_tom.note_off()
                elif 'Xbox' in name:
                    if event.button == 0:
                        hi_bongo.note_off()
                        snare_drum.note_off()
                    elif event.button == 1:
                        low_bongo.note_off()
                        bass_drum.note_off()
                    elif event.button == 2:
                        low_conga.note_off()
                        tom_toms.note_off()
                    elif event.button == 3:
                        hi_conga.note_off()
                        hi_hat_foot.note_off()
                    elif event.button == 5:
                        hi_woodblock.note_off()
                        ride_cymbal.note_off()
                    elif event.button == 4:
                        low_woodblock.note_off()
                        bass_drum.note_off()
                        crash_cymbal.note_off()
                    elif event.button == 8:
                        claves.note_off()
                        side_stick.note_off()
                    elif event.button == 9:
                        shaker.note_off()
                        floor_tom.note_off()
                elif name=='PS4 Controller':
                    if event.button == 0:
                        hi_bongo.note_off()
                        snare_drum.note_off()
                    elif event.button == 1:
                        low_bongo.note_off()
                        trigger_bass_drum()
                    elif event.button == 2:
                        low_conga.note_off()
                        tom_toms.note_off()
                    elif event.button == 3:
                        hi_conga.note_off()
                        hi_hat_foot.note_off()
                    elif event.button == 10:
                        hi_woodblock.note_off()
                        ride_cymbal.note_off()
                    elif event.button == 9:
                        low_woodblock.note_off()
                        bass_drum.note_off()
                        crash_cymbal.note_off()
                    elif event.button == 11:
                        triangle.note_off()
                        hi_hat_open.note_off()
                    elif event.button == 12:
                        m_triangle.note_off()
                        hi_hat.note_off()
                    elif event.button == 13:
                        hi_timbale.note_off()
                        hi_tom.note_off()
                    elif event.button == 14:
                        low_timbale.note_off()
                        mid_tom.note_off()
                    elif event.button == 7:
                        claves.note_off()
                        side_stick.note_off()
                    elif event.button == 8:
                        shaker.note_off()
                        floor_tom.note_off()
                elif name=='Sony Interactive Entertainment Wireless Controller' or name=='DualSense Wireless Controller':
                    if event.button == 0:
                        hi_bongo.note_off()
                        snare_drum.note_off()
                    elif event.button == 1:
                        low_bongo.note_off()
                        bass_drum.note_off()
                    elif event.button == 2:
                        low_conga.note_off()
                        tom_toms.note_off()
                    elif event.button == 3:
                        hi_conga.note_off()
                        hi_hat_foot.note_off()
                    elif event.button == 5:
                        ride_cymbal.note_off()
                        hi_woodblock.note_off()
                    elif event.button == 4:
                        low_woodblock.note_off()
                        bass_drum.note_off()
                        crash_cymbal.note_off()
                    elif event.button == 11:
                        claves.note_off()
                        side_stick.note_off()
                    elif event.button == 12:
                        shaker.note_off()
                        floor_tom.note_off()
                else:
                    if event.button == 0:
                        hi_bongo.note_off()
                        snare_drum.note_off()
                    elif event.button == 1:
                        low_bongo.note_off()
                        bass_drum.note_off()
                    elif event.button == 2:
                        low_conga.note_off()
                        tom_toms.note_off()
                    elif event.button == 3:
                        hi_conga.note_off()
                        hi_hat_foot.note_off()
                    elif event.button == 5:
                        ride_cymbal.note_off()
                        hi_woodblock.note_off()
                    elif event.button == 4:
                        bass_drum.note_off()
                        crash_cymbal.note_off()
                        low_woodblock.note_off()
                    elif event.button == 15:
                        hi_hat_open.note_off()
                        triangle.note_off()
                    elif event.button == 14:
                        hi_hat.note_off()
                        m_triangle.note_off()
                    elif event.button == 8:
                        side_stick.note_off()
                        claves.note_off()
                    elif event.button == 9:
                        floor_tom.note_off()
                        shaker.note_off()
            except:
                pass
        if event.type == pygame.JOYHATMOTION and bool(root.checkboxes[event.instance_id].get()):
            name=root.joysticks[event.instance_id].get_name()
            perc=bool(root.modes[event.instance_id].get())
            if root.joysticks[event.instance_id].get_numhats()>0:
                hatx, haty=root.joysticks[event.instance_id].get_hat(0)
                if hatx==-1 and (root.focus_displayof() is not None):
                    if perc:
                        hi_timbale.trigger()
                    else:
                        hi_tom.trigger()
                elif hatx==1 and (root.focus_displayof() is not None):
                    if perc:
                        low_timbale.trigger()
                    else:
                        mid_tom.trigger()
                elif hatx==0:
                    mid_tom.note_off()
                    hi_tom.note_off()
                    hi_timbale.note_off()
                    low_timbale.note_off()
                if haty==-1 and (root.focus_displayof() is not None):
                    if perc:
                        m_triangle.trigger()
                    else:
                        trigger_hi_hat()
                elif haty==1 and (root.focus_displayof() is not None):
                    if perc:
                        triangle.trigger()
                    else:
                        hi_hat_open.trigger()
                elif haty==0:
                    hi_hat_open.note_off()
                    hi_hat.note_off()
                    m_triangle.note_off()
                    triangle.note_off()
        if event.type == pygame.JOYAXISMOTION:
            print(event)
            if event.axis==0 and midiselect.get()!='Internal Audio':
                try:
                    root.ports[midiselect.get()].send(mido.Message('control_change', channel=9, control=10, value=int((event.value+1)*63)))
                except:
                    pass
            if event.axis==3 and midiselect.get()!='Internal Audio':
                try:
                    root.ports[midiselect.get()].send(mido.Message('pitchwheel', channel=9, pitch=int(-event.value*8191)))
                except:
                    pass
            if root.joysticks[event.instance_id].get_name()=='Nintendo Switch Pro Controller' and bool(root.checkboxes[event.instance_id].get()):
                perc=bool(root.modes[event.instance_id].get())
                if root.splitcymbals[event.instance_id]:
                    if event.axis==4 and event.value==1 and (root.focus_displayof() is not None):
                        if perc:
                            vibraslap.trigger()
                        else:
                            trigger_crash_cymbal()
                            if root.checkboxes1[event.instance_id].get()=='L Crash':
                                trigger_bass_drum()
                    if event.axis==4 and event.value!=1:
                        vibraslap.note_off()
                        crash_cymbal.note_off()
                        bass_drum.note_off()
                    if event.axis==5 and event.value==1 and (root.focus_displayof() is not None):
                        if perc:
                            maracas.trigger()
                        else:
                            crash_cymbal_2.trigger()
                            if root.checkboxes1[event.instance_id].get()=='R Crash':
                                trigger_bass_drum()
                    if event.axis==5 and event.value!=1:
                        crash_cymbal_2.note_off()
                        bass_drum.note_off()
                        maracas.note_off()
    for controller in root.joysticks.values():
        battery=controller.get_power_level()
        instance_id=controller.get_instance_id()
        try:
            if battery=='max':
                root.statuses[instance_id].configure(text='Full', text_color=('#00ff00', '#00ff00'))
            elif battery=='full':
                root.statuses[instance_id].configure(text='High', text_color=('#00ff00', '#00ff00'))
            elif battery=='medium':
                root.statuses[instance_id].configure(text='Medium', text_color=('orange', 'orange'))
            elif battery=='low':
                root.statuses[instance_id].configure(text='Low', text_color=('red','red'))
                low_bat_count+=1
            elif battery=='empty':
                if time.time()%1>=0.5:
                    color=('red', 'red')
                else:
                    color=('grey', 'grey')
                root.statuses[instance_id].configure(text='Critical', text_color=color)
                crit_bat_count+=1
            elif battery=='wired':
                root.statuses[instance_id].configure(text='Wired', text_color=('#00ff00', '#00ff00'))
            else:
                root.statuses[instance_id].configure(text='Unknown', text_color=('grey','grey'))
        except:
            pass
    if len(root.joysticks)>0:
        if crit_bat_count>0:
            try:
                controller_count.configure(text=str(len(root.joysticks)), text_color=color)
            except:
                controller_count.configure(text=str(len(root.joysticks)), text_color=('red','red'))
        elif low_bat_count>0:
            controller_count.configure(text=str(len(root.joysticks)), text_color=('red','red'))
        else:
            controller_count.configure(text=str(len(root.joysticks)), text_color=('#00ff00', '#00ff00'))
    else:
        controller_count.configure(text='0', text_color=('grey','grey'))
    root.after(50, check_status)
def stop_all():
    for controller in root.joysticks.values():
        controller.stop_rumble()
def change_patch():
    if midiselect.get()!='Internal Audio':
        root.ports[midiselect.get()].send(mido.Message('program_change', channel=9, program=int(patch_change.get())))
    else:
        if patch_change.get()=='25':
            root.kit_808=True
            if midiselect.get()=='Internal Audio':
                for sw in root.modes.values():
                    sw.deselect()
                    sw.configure(state="disabled")
        elif patch_change.get()=='0' or patch_change.get()=='1':
            root.kit_808=False
            for sw in root.modes.values():
                sw.configure(state="normal")
def all_notes_off():
    if midiselect.get()!='Internal Audio':
        for i in range(36, 83):
            root.ports[midiselect.get()].send(mido.Message('note_off', channel=9, note=i, velocity=127))
def change_volume(n):
    if not midiselect.get()=='Internal Audio':
        root.ports[midiselect.get()].send(mido.Message('control_change', channel=9, control=7, value=int(volSlider.get())))
def on_press(key):
    if (root.focus_displayof() is not None) and bool(key_enable.get()):
        if key==keyboard.Key.space:
            bass_drum.trigger()
        else:
            try:
                if key.char=='a' or key.char=='s':
                    snare_drum.trigger()
                elif key.char=='d':
                    hi_tom.trigger()
                elif key.char=='j':
                    mid_tom.trigger()
                elif key.char=='k':
                    tom_toms.trigger()
                elif key.char=='l':
                    floor_tom.trigger()
                elif key.char=='q':
                    crash_cymbal.trigger()
                elif key.char=='o':
                    ride_cymbal.trigger()
                elif key.char=='f':
                    hi_hat.trigger()
                elif key.char=='g':
                    hi_hat_foot.trigger()
                elif key.char=='h':
                    hi_hat_open.trigger()
                elif key.char=='w':
                    ride_cymbal_2.trigger()
                elif key.char=='p':
                    crash_cymbal_2.trigger()
                elif key.char=='x':
                    side_stick.trigger()
                elif key.char=='e':
                    hi_bongo.trigger()
                elif key.char=='r':
                    low_bongo.trigger()
                elif key.char=='t':
                    hi_conga.trigger()
                elif key.char=='y':
                    low_conga.trigger()
                elif key.char=='u':
                    hi_timbale.trigger()
                elif key.char=='i':
                    low_timbale.trigger()
                elif key.char=='z':
                    maracas.trigger()
                elif key.char=='c':
                    shaker.trigger()
                elif key.char=='v':
                    vibraslap.trigger()
                elif key.char=='b':
                    claves.trigger()
                elif key.char=='n':
                    hi_woodblock.trigger()
                elif key.char=='m':
                    low_woodblock.trigger()
            except AttributeError:
                pass
def on_release(key):
    if bool(key_enable.get()):
        if key==keyboard.Key.space:
            bass_drum.note_off()
        else:
            try:
                if key.char=='a' or key.char=='s':
                    snare_drum.note_off()
                elif key.char=='d':
                    hi_tom.note_off()
                elif key.char=='j':
                    mid_tom.note_off()
                elif key.char=='k':
                    tom_toms.note_off()
                elif key.char=='l':
                    floor_tom.note_off()
                elif key.char=='q':
                    crash_cymbal.note_off()
                elif key.char=='o':
                    ride_cymbal.note_off()
                elif key.char=='f':
                    hi_hat.note_off()
                elif key.char=='g':
                    hi_hat_foot.note_off()
                elif key.char=='h':
                    hi_hat_open.note_off()
                elif key.char=='w':
                    ride_cymbal_2.note_off()
                elif key.char=='p':
                    crash_cymbal_2.note_off()
                elif key.char=='x':
                    side_stick.note_off()
                elif key.char=='e':
                    hi_bongo.note_off()
                elif key.char=='r':
                    low_bongo.note_off()
                elif key.char=='t':
                    hi_conga.note_off()
                elif key.char=='y':
                    low_conga.note_off()
                elif key.char=='u':
                    hi_timbale.note_off()
                elif key.char=='i':
                    low_timbale.note_off()
                elif key.char=='z':
                    maracas.note_off()
                elif key.char=='c':
                    shaker.note_off()
                elif key.char=='v':
                    vibraslap.note_off()
                elif key.char=='b':
                    claves.note_off()
                elif key.char=='n':
                    hi_woodblock.note_off()
                elif key.char=='m':
                    low_woodblock.note_off()
            except AttributeError:
                pass
def update_midi(val):
    if val=='Internal Audio' and root.kit_808:
        for sw in root.modes.values():
            sw.deselect()
            sw.configure(state="disabled")
    else:
        for sw in root.modes.values():
            sw.configure(state="normal")
CTkLabel(root, text='Drum Set').pack()
frame0=CTkFrame(root)
frame0.pack()
root.resizable(False, False)
root.title('Drum Set (c) HapticWave Software')
root.joysticks={}
root.statuses={}
root.checkboxes={}
root.checkboxes1={}
root.splitcymbals={}
root.swapab={}
root.modes={}
root.iconbitmap(get_resource_path('drum.ico'))
bass_drum_button = CTkButton(frame0, text="Kick", command=bass_drum.trigger_once)
snare_drum_button = CTkButton(frame0, text="Snare", command=snare_drum.trigger_once)
tom_toms_button = CTkButton(frame0, text="Low Tom", command=tom_toms.trigger_once)
CTkButton(frame0, text="Mid Tom", command=mid_tom.trigger_once).grid(column=2, row=4)
CTkButton(frame0, text="High Tom", command=hi_tom.trigger_once).grid(column=3, row=4)
hi_hat_open_button = CTkButton(frame0, text="Open Hi-Hat", command=hi_hat_open.trigger_once)
hi_hat_foot_button = CTkButton(frame0, text="Pedal Hi-Hat", command=hi_hat_foot.trigger_once)
hi_hat_button = CTkButton(frame0, text="Closed Hi-Hat", command=hi_hat.trigger_once)
ride_cymbal_button = CTkButton(frame0, text="Ride Cymbal", command=ride_cymbal.trigger_once)
crash_cymbal_button = CTkButton(frame0, text="Crash Cymbal 1", command=crash_cymbal.trigger_once)
side_stick_button = CTkButton(frame0, text="Side Stick", command=side_stick.trigger_once)
CTkButton(frame0, text="Crash Cymbal 2", command=crash_cymbal_2.trigger_once).grid(column=3, row=3)
CTkButton(frame0, text='All Notes OFF', command=all_notes_off).grid(column=2, row=5)
# Place Buttons in UI
bass_drum_button.grid(column=1, row=1)
snare_drum_button.grid(column=2, row=1)
tom_toms_button.grid(column=1, row=4)
hi_hat_button.grid(column=1, row=2)
hi_hat_open_button.grid(column=2, row=2)
hi_hat_foot_button.grid(column=3, row=2)
ride_cymbal_button.grid(column=2, row=3)
crash_cymbal_button.grid(column=1, row=3)
side_stick_button.grid(column=3, row=1)
frame100=CTkFrame(root)
frame100.pack()
CTkLabel(frame100, text='Volume').pack(side=LEFT)
volSlider=CTkSlider(frame100, from_=0, to=127, command=change_volume)
volSlider.pack(side=LEFT, padx=5)
volSlider.set(127)
CTkLabel(root, text='MIDI Out:').pack()
root.ports={'Internal Audio': None}
for i in mido.get_output_names():
    port=mido.open_output(i)
    root.ports[i]=port
midiselect=CTkOptionMenu(root, values=tuple(root.ports.keys()), command=update_midi)
midiselect.pack()
root.kit_808=False
CTkLabel(root, text='MIDI Patch').pack()
frame2=CTkFrame(root)
patch_change=CTkOptionMenu(frame2, values=['0', '1', '8', '16', '24', '25', '26', '32', '40'])
patch_change.pack(side=LEFT)
CTkButton(frame2, command=change_patch, text='Apply Selected Patch').pack()
frame2.pack()
frame=CTkFrame(root)
CTkLabel(frame, text='Number of controllers connected:').pack(side=LEFT)
controller_count=CTkLabel(frame, text='0', text_color=('grey', 'grey'))
controller_count.pack(side=LEFT, padx=5)
check=CTkCheckBox(root, text='Swap A/B & X/Y for newly connected Switch ProCons')
check.pack()
check1=CTkCheckBox(root, text='Enable additional cymbals for newly connected Switch ProCons')
check1.pack()
check1.select()
frame.pack()
tabview=CTkTabview(root)
tabview.pack()
tabview.add('KB')
key_enable=CTkSwitch(tabview.tab('KB'), text='Bind keyboard to drums')
key_enable.pack()
CTkLabel(tabview.tab('KB'), text='Mapping:\nSpace: Kick\nA/S: Snare\nD/J/K/L: Toms\nH: Open Hi-Hat\nG: Pedal Hi-Hat\nF: Closed Hi-Hat\nQ: Crash Cymbal 1\nP: Crash Cymbal 2\nO: Ride Cymbal 1\nW: Ride Cymbal 2\nX: Side Stick\nE/R: Bongos\nT/Y: Congas\nU/I: Timbales\nZ: Maracas\nC: Shaker\nV: Vibraslap\nB: Claves\nN: Woodblock\nM: Cowbell').pack()
Hovertip(check, 'Make the button layout of Nintendo ProCons more like Xbox/PS4')
Hovertip(check1, 'Enables ZL/ZR functionality for ProCons, allowing more drum sounds')
Hovertip(controller_count, 'A red number indicates a low battery in one or more controllers')
Hovertip(patch_change, "Each patch correlates to a different sound set\n0: Standard Kit\n1: Alt. Kit\n8: Room Kit\n16: Power Kit\n24: Electronic Kit\n25: TR-808\n26: Dance Kit\n32: Jazz Kit\n40: Brush Kit\nClick 'Apply Selected Patch' for the new patch to take effect.\nIf you're using the internal sampler, only patches 0, 1, and 25 will take effect.")
Hovertip(midiselect, 'Use to select an output for the program. Some features, like pan or patch selection, only work when an external MIDI output is selected')
root.protocol('WM_DELETE_WINDOW', close)
keyboard.Listener(on_press=on_press, on_release=on_release).start()
check_status()
root.mainloop()
