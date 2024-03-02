import threading
import time, serial
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
def read_serial():
    global ser
    while True:
        data=ser.read().decode()
        if data=='k':
            bass_drum.trigger_once()
        elif data=='s':
            snare_drum.trigger_once()
        elif data=='f':
            hi_hat.trigger_once()
        elif data=='h':
            hi_hat_open.trigger_once()
        elif data=='g':
            hi_hat-foot.trigger_once()
        elif data=='m':
            mid_tom.trigger_once()
        elif data=='n':
            hi_tom.trigger_once()
        elif data=='b':
            floor_tom.trigger_once()
        elif data=='l':
            tom_toms.trigger_once()
        elif data=='q':
            crash_cymbal.trigger_once()
        elif data=='p':
            ride_cymbal.trigger_once()
        elif data=='r':
            side_stick.trigger_once()
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
    def play_haptic_envelope(self, velocity):
        if midiselect.get()=='Internal Audio':
            self.channel.set_volume((volSlider.get()/127)*(velocity/127))
            if root.kit_808:
                if self.name2 is not None:
                    self.channel.play(self.sound2)
            else:
                self.channel.play(self.sound)
        else:
            root.ports[midiselect.get()].send(mido.Message('note_on', channel=9, note=self.note, velocity=int(velocity)))
    def stop(self):
        if midiselect.get()=='Internal Audio':
            self.channel.stop()
    def trigger(self, velocity):
        threading.Thread(target=self.play_haptic_envelope, args=[velocity]).start()
    def note_off(self):
        if not midiselect.get()=='Internal Audio':
            root.ports[midiselect.get()].send(mido.Message('note_off', channel=9, note=self.note, velocity=127))
    def trigger_once(self):
        self.play_haptic_envelope(127)
        self.note_off()
# Create Drum Objects
pygame.mixer.init()
pygame.display.init()
pygame.mixer.set_num_channels(36)
pygame.joystick.init()
bass_drum = HapticDrum('bass_drum','BD', 0, 36)
bass_drum_2 = HapticDrum('kick_2','BD', 30, 35)
snare_drum = HapticDrum('snare_drum','SD', 1, 38)
snare_drum_2 = HapticDrum('snare_2','SD', 28, 40)
floor_tom_2 = HapticDrum('high_floor_tom', 'LT', 29, 43)
low_tom = HapticDrum('low_tom', 'LT', 2, 45)
hi_hat_closed = HapticDrum('hi_hat_closed','CH', 3, 42)
ride_cymbal = HapticDrum('ride_cymbal',None, 4, 51)
ride_cymbal_2 = HapticDrum('ride_cymbal_2',None, 13, 59)
crash_cymbal = HapticDrum('crash_cymbal','CY', 5, 49)
crash_cymbal_2 = HapticDrum('crash_cymbal_2','CY', 12, 57)
low_mid_tom = HapticDrum('mid_tom','MT', 6, 47)
hi_mid_tom = HapticDrum('mid_tom','MT', 31, 48)
hi_tom = HapticDrum('hi_tom','HT', 7, 50)
floor_tom = HapticDrum('low_floor_tom','LT', 11, 41)
hi_hat_open = HapticDrum('hi_hat_open','OH', 8, 46)
hi_hat_foot = HapticDrum('hi_hat_foot','CH', 9, 44)
side_stick = HapticDrum('side_stick','RS', 10, 37)
clap = HapticDrum('clap_2','clap', 32, 39)
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
splash=HapticDrum('splash_cymbal',None, 33, 55)
ride_bell=HapticDrum('ride_bell',None, 34, 53)
tambourine=HapticDrum('tambourine',None, 35, 54)
root = CTk()
root.axis_to_name={'Nintendo Switch Pro Controller':{'A4':'ZL', 'A5': 'ZR'}}
root.button_to_name={'Nintendo Switch Pro Controller': {'0': 'A', '1': 'B', '2':'X', '3':'Y', '7':'LS Press', '8':'RS Press', '9':'L', '10':'R','11':'Dpad Up', '12':'Dpad Down', '13':'Dpad Left', '14':'Dpad Right'},
                     'Xbox 360 Controller':{'0': 'A', '1': 'B', '2':'X', '3':'Y', '4': 'LB', '5':'RB', '8':'LS Press', '9':'RS Press'},
                     'PS4 Controller':{'0':'✕', '1':'○', '2':'◻', '3':'△','7':'L3', '8':'R3', '9':'L1', '10':'R1','11':'Dpad Up', '12':'Dpad Down', '13':'Dpad Left', '14':'Dpad Right'}}
root.name_to_drum={'---':None, 'Kick 2':bass_drum_2, 'Kick 1':bass_drum, 'Side Stick': side_stick, 'Snare 1':snare_drum, 'Clap':clap, 'Snare 2':snare_drum_2, 'Low Floor Tom':floor_tom, 'Closed HiHat':hi_hat_closed, 'High Floor Tom': floor_tom_2, 'Pedal HiHat':hi_hat_foot, 'Low Tom':low_tom, 'Open HiHat':hi_hat_open, 'Low-Mid Tom':low_mid_tom, 'High-Mid Tom':hi_mid_tom, 'Crash 1':crash_cymbal, 'High Tom':hi_tom, 'Ride 1':ride_cymbal, 'Ride Bell':ride_bell, 'Tambourine':tambourine, 'Splash Cymbal':splash, 'Cowbell': low_woodblock, 'Crash 2':crash_cymbal_2, 'Vibraslap':vibraslap, 'Ride 2':ride_cymbal_2, 'High Bongo': hi_bongo, 'Low Bongo':low_bongo, 'High Conga':hi_conga, 'Low Conga':low_conga, 'High Timbale':hi_timbale,'Low Timbale': low_timbale, 'Woodblock':hi_woodblock, 'Claves':claves, 'Shaker':shaker, 'Maracas':maracas, 'Mute Triangle':m_triangle, 'Open Triangle': triangle}
def check_status():
    low_bat_count=0
    crit_bat_count=0
    for event in pygame.event.get():
        default_mapping=None
        if event.type == pygame.JOYDEVICEADDED:
            joy = pygame.joystick.Joystick(event.device_index)
            tabview.add('Cnt'+str(joy.get_instance_id()))
            tab=tabview.tab('Cnt'+str(joy.get_instance_id()))
            root.joysticks[joy.get_instance_id()]=joy
            CTkLabel(tab, text=joy.get_name()).pack()
            CTkLabel(tab, text='Battery:').pack()
            statusLabel=CTkLabel(tab, text='Unknown', text_color=('grey', 'grey'))
            statusLabel.pack()
            root.statuses[joy.get_instance_id()]=statusLabel
            checkbox=CTkSwitch(tab, text='Always bind controller to drums')
            checkbox.pack()
            root.checkboxes[joy.get_instance_id()]=checkbox
            if joy.get_name()=='Nintendo Switch Pro Controller':
                default_mapping={'0':'Snare 1', '1':'Kick 1', '2':'Low Tom', '3':'Pedal HiHat', '7':'Side Stick', '8':'Low Floor Tom', '9':'Ride 2', '10':'Ride 1', '11': 'Open HiHat', '12':'Closed HiHat', '13':'High Tom', '14': 'Low-Mid Tom', 'A4':'Crash 1', 'A5':'Crash 2'}
            elif 'Xbox' in joy.get_name():
                default_mapping={'0':'Snare 1', '1':'Kick 1', '2':'Low Tom', '3':'Pedal HiHat', '8':'Side Stick', '9':'Low Floor Tom', '4':'Crash 1', '5':'Ride 1', 'D_Up': 'Open HiHat', 'D_Down':'Closed HiHat', 'D_Left':'High Tom', 'D_Right': 'Low-Mid Tom'}
            elif 'PS4' in joy.get_name():
                default_mapping={'0':'Snare 1', '1':'Kick 1', '2':'Low Tom', '3':'Pedal HiHat', '7':'Side Stick', '8':'Low Floor Tom', '9':'Crash 1', '10':'Ride 1', '11': 'Open HiHat', '12':'Closed HiHat', '13':'High Tom', '14': 'Low-Mid Tom'}
            elif joy.get_name()=='Sony Interactive Entertainment Wireless Controller':
                default_mapping={'0':'Snare 1', '1':'Kick 1', '2':'Low Tom', '3':'Pedal HiHat', '11':'Side Stick', '12':'Low Floor Tom', '4':'Crash 1', '5':'Ride 1', 'D_Up': 'Open HiHat', 'D_Down':'Closed HiHat', 'D_Left':'High Tom', 'D_Right': 'Low-Mid Tom'}
            else:
                default_mapping={'0':'Snare 1', '1':'Kick 1', '2':'Low Tom', '3':'Pedal HiHat', '4':'Crash 1', '5':'Ride 1','6':'---','7':'---','8':'Side Stick', '9':'Low Floor Tom', '10':'---', '11':'---','12':'---','13':'---','14':'---','15':'---','D_Up':'Open HiHat', 'D_Down':'Closed HiHat', 'D_Left':'High Tom', 'D_Right': 'Low-Mid Tom'} 
            tabview.set('Cnt'+str(joy.get_instance_id()))
            temp={}
            temp2={}
            temp3={}
            fra=CTkFrame(tab)
            fra.pack()
            CTkLabel(fra, text='Button').grid(column=1, row=0)
            CTkLabel(fra, text='Mapping').grid(column=2, row=0)
            CTkLabel(fra, text='Velocity').grid(column=3, row=0)
            for i in range(len(default_mapping)):
                c=root.button_to_name[joy.get_name()][str(list(default_mapping.keys())[i])] if (('D' not in str(list(default_mapping.keys())[i])) and ('A' not in str(list(default_mapping.keys())[i])) and (joy.get_name() in root.button_to_name)) else (root.axis_to_name[joy.get_name()][str(list(default_mapping.keys())[i])] if ('A' in str(list(default_mapping.keys())[i])) else str(list(default_mapping.keys())[i]))
                l=CTkLabel(fra, text=c, text_color=('#000000', '#ffffff'))
                l.grid(column=1, row=i+1)
                o=CTkOptionMenu(fra, values=list(root.name_to_drum.keys()))
                o.grid(column=2, row=i+1)
                o.set(default_mapping[str(list(default_mapping.keys())[i])])
                temp[str(list(default_mapping.keys())[i])]=o
                s=CTkSlider(fra, from_=0, to=127)
                s.set(127)
                s.grid(column=3, row=i+1)
                temp2[str(list(default_mapping.keys())[i])]=s
                temp3[str(list(default_mapping.keys())[i])]=l
            root.dropdowns[joy.get_instance_id()]=temp
            root.sliders[joy.get_instance_id()]=temp2
            root.indicators[joy.get_instance_id()]=temp3
            CTkLabel(tab, text='L Stick X (external MIDI Out only):Pan\n R Stick Y (external MIDI Out only): Pitch').pack()
        if event.type == pygame.JOYDEVICEREMOVED:
            root.checkboxes[event.instance_id].deselect()
            tabview.delete('Cnt'+str(event.instance_id))
            del root.joysticks[event.instance_id]
            del root.statuses[event.instance_id]
            del root.dropdowns[event.instance_id]
            del root.sliders[event.instance_id]
            del root.indicators[event.instance_id]
        if event.type == pygame.JOYBUTTONDOWN and ((root.focus_displayof() is not None) or bool(root.checkboxes[event.instance_id].get())):
            try:
                root.name_to_drum[root.dropdowns[event.instance_id][str(event.button)].get()].trigger(root.sliders[event.instance_id][str(event.button)].get())
                if root.dropdowns[event.instance_id][str(event.button)].get()=='Closed HiHat' or root.dropdowns[event.instance_id][str(event.button)].get()=='Pedal HiHat':
                    hi_hat_open.stop()
                root.indicators[event.instance_id][str(event.button)].configure(text_color=('#00ff00', '#00ff00'))
            except:
                pass
        if event.type == pygame.JOYBUTTONUP:
            name=root.joysticks[event.instance_id].get_name()
            try:
                root.indicators[event.instance_id][str(event.button)].configure(text_color=('#000000', '#ffffff'))
                root.name_to_drum[root.dropdowns[event.instance_id][str(event.button)].get()].note_off()
            except:
                pass
        if event.type == pygame.JOYHATMOTION:
            name=root.joysticks[event.instance_id].get_name()
            if root.joysticks[event.instance_id].get_numhats()>0:
                hatx, haty=root.joysticks[event.instance_id].get_hat(0)
                if haty==-1 and (root.focus_displayof() is not None):
                    try:
                        root.name_to_drum[root.dropdowns[event.instance_id]['D_Down'].get()].trigger(root.sliders[event.instance_id]['D_Down'].get())
                        if root.dropdowns[event.instance_id]['D_Down'].get()=='Closed HiHat' or root.dropdowns[event.instance_id]['D_Down'].get()=='Pedal HiHat':
                            hi_hat_open.stop()
                        root.indicators[event.instance_id]['D_Down'].configure(text_color=('#00ff00', '#00ff00'))
                    except:
                        pass
                elif haty==1 and (root.focus_displayof() is not None):
                    try:
                        root.name_to_drum[root.dropdowns[event.instance_id]['D_Up'].get()].trigger(root.sliders[event.instance_id]['D_Up'].get())
                        if root.dropdowns[event.instance_id]['D_Up'].get()=='Closed HiHat' or root.dropdowns[event.instance_id]['D_Up'].get()=='Pedal HiHat':
                            hi_hat_open.stop()
                        root.indicators[event.instance_id]['D_Up'].configure(text_color=('#00ff00', '#00ff00'))
                    except:
                        pass
                elif haty==0:
                    try:
                        root.indicators[event.instance_id]['D_Up'].configure(text_color=('#000000', '#ffffff'))
                        root.indicators[event.instance_id]['D_Down'].configure(text_color=('#000000', '#ffffff'))
                        root.name_to_drum[root.dropdowns[event.instance_id]['D_Up'].get()].note_off()
                        root.name_to_drum[root.dropdowns[event.instance_id]['D_Down'].get()].note_off()
                    except:
                        pass
                if hatx==-1 and (root.focus_displayof() is not None):
                    try:
                        root.name_to_drum[root.dropdowns[event.instance_id]['D_Left'].get()].trigger(root.sliders[event.instance_id]['D_Left'].get())
                        if root.dropdowns[event.instance_id]['D_Left'].get()=='Closed HiHat' or root.dropdowns[event.instance_id]['D_Left'].get()=='Pedal HiHat':
                            hi_hat_open.stop()
                        root.indicators[event.instance_id]['D_Left'].configure(text_color=('#00ff00', '#00ff00'))
                    except:
                        pass
                elif hatx==1 and (root.focus_displayof() is not None):
                    try:
                        root.name_to_drum[root.dropdowns[event.instance_id]['D_Right'].get()].trigger(root.sliders[event.instance_id]['D_Right'].get())
                        if root.dropdowns[event.instance_id]['D_Right'].get()=='Closed HiHat' or root.dropdowns[event.instance_id]['D_Right'].get()=='Pedal HiHat':
                            hi_hat_open.stop()
                        root.indicators[event.instance_id]['D_Right'].configure(text_color=('#00ff00', '#00ff00'))
                    except:
                        pass
                elif hatx==0:
                    try:
                        root.indicators[event.instance_id]['D_Left'].configure(text_color=('#000000', '#ffffff'))
                        root.indicators[event.instance_id]['D_Right'].configure(text_color=('#000000', '#ffffff'))
                        root.name_to_drum[root.dropdowns[event.instance_id]['D_Left'].get()].note_off()
                        root.name_to_drum[root.dropdowns[event.instance_id]['D_Right'].get()].note_off()
                    except:
                        pass
        if event.type == pygame.JOYAXISMOTION:
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
            if root.joysticks[event.instance_id].get_name()=='Nintendo Switch Pro Controller' and (event.axis==4 or event.axis==5):
                if event.value==1 and ((root.focus_displayof() is not None) or bool(root.checkboxes[event.instance_id].get())):
                    try:
                        root.name_to_drum[root.dropdowns[event.instance_id]['A'+str(event.axis)].get()].trigger(root.sliders[event.instance_id]['A'+str(event.axis)].get())
                        if root.dropdowns[event.instance_id]['A'+str(event.axis)].get()=='Closed HiHat' or root.dropdowns[event.instance_id]['A'+str(event.axis)].get()=='Pedal HiHat':
                            hi_hat_open.stop()
                        root.indicators[event.instance_id]['A'+str(event.axis)].configure(text_color=('#00ff00', '#00ff00'))
                    except:
                        pass
                if event.value!=1:
                    try:
                        root.indicators[event.instance_id]['A'+str(event.axis)].configure(text_color=('#000000', '#ffffff'))
                        root.name_to_drum[root.dropdowns[event.instance_id]['A'+str(event.axis)].get()].note_off()
                    except:
                        pass
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
        elif patch_change.get()=='0' or patch_change.get()=='1':
            root.kit_808=False
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
            bass_drum.trigger(127)
        else:
            try:
                if key.char=='a' or key.char=='s':
                    snare_drum.trigger(127)
                elif key.char=='d':
                    hi_tom.trigger(127)
                elif key.char=='j':
                    low_mid_tom.trigger(127)
                elif key.char=='k':
                    low_tom.trigger(127)
                elif key.char=='l':
                    floor_tom.trigger(127)
                elif key.char=='q':
                    crash_cymbal.trigger(127)
                elif key.char=='o':
                    ride_cymbal.trigger(127)
                elif key.char=='f':
                    hi_hat_closed.trigger(127)
                elif key.char=='g':
                    hi_hat_foot.trigger(127)
                elif key.char=='h':
                    hi_hat_open.trigger(127)
                elif key.char=='w':
                    ride_cymbal_2.trigger(127)
                elif key.char=='p':
                    crash_cymbal_2.trigger(127)
                elif key.char=='x':
                    side_stick.trigger(127)
                elif key.char=='e':
                    hi_bongo.trigger(127)
                elif key.char=='r':
                    low_bongo.trigger(127)
                elif key.char=='t':
                    hi_conga.trigger(127)
                elif key.char=='y':
                    low_conga.trigger(127)
                elif key.char=='u':
                    hi_timbale.trigger(127)
                elif key.char=='i':
                    low_timbale.trigger(127)
                elif key.char=='z':
                    maracas.trigger(127)
                elif key.char=='c':
                    shaker.trigger(127)
                elif key.char=='v':
                    vibraslap.trigger(127)
                elif key.char=='b':
                    claves.trigger(127)
                elif key.char=='n':
                    hi_woodblock.trigger(127)
                elif key.char=='m':
                    low_woodblock.trigger(127)
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
                    low_mid_tom.note_off()
                elif key.char=='k':
                    low_tom.note_off()
                elif key.char=='l':
                    floor_tom.note_off()
                elif key.char=='q':
                    crash_cymbal.note_off()
                elif key.char=='o':
                    ride_cymbal.note_off()
                elif key.char=='f':
                    hi_hat_closed.note_off()
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
def begin_serial():
    global ser
    if not root.serial:
        try:
            ser = serial.Serial(cb.get(), baudrate=9600)
            threading.Thread(target=read_serial, daemon=True).start()
        except Exception as e:
            messagebox.showerror('Error', str(e))
            return
        start.configure(text='Stop Serial In')
        cb.configure(state=DISABLED)
        root.serial=True
    else:
        ser.close()
        start.configure(text='Start Serial In')
        cb.configure(state='readonly')
        root.serial=False
CTkLabel(root, text='Drum Set').pack()
frame0=CTkFrame(root)
frame0.pack()
root.resizable(False, False)
root.title('Drum Set (c) HapticWave Software')
root.indicators={}
root.joysticks={}
root.statuses={}
root.dropdowns={}
root.checkboxes={}
root.sliders={}
root.serial=False
ser=None
root.iconbitmap(get_resource_path('drum.ico'))
bass_drum_button = CTkButton(frame0, text="Kick", command=bass_drum.trigger_once)
snare_drum_button = CTkButton(frame0, text="Snare", command=snare_drum.trigger_once)
tom_toms_button = CTkButton(frame0, text="Low Tom", command=low_tom.trigger_once)
CTkButton(frame0, text="Mid Tom", command=low_mid_tom.trigger_once).grid(column=2, row=4)
CTkButton(frame0, text="High Tom", command=hi_tom.trigger_once).grid(column=3, row=4)
hi_hat_open_button = CTkButton(frame0, text="Open Hi-Hat", command=hi_hat_open.trigger_once)
hi_hat_foot_button = CTkButton(frame0, text="Pedal Hi-Hat", command=hi_hat_foot.trigger_once)
hi_hat_button = CTkButton(frame0, text="Closed Hi-Hat", command=hi_hat_closed.trigger_once)
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
midiselect=CTkOptionMenu(root, values=tuple(root.ports.keys()))
midiselect.pack()
root.kit_808=False
CTkLabel(root, text='MIDI Patch').pack()
frame2=CTkFrame(root)
patch_change=CTkOptionMenu(frame2, values=['0', '1', '8', '16', '24', '25', '26', '32', '40', '48'])
patch_change.pack(side=LEFT)
CTkButton(frame2, command=change_patch, text='Apply Selected Patch').pack()
frame2.pack()
frame=CTkFrame(root)
CTkLabel(frame, text='Number of controllers connected:').pack(side=LEFT)
controller_count=CTkLabel(frame, text='0', text_color=('grey', 'grey'))
controller_count.pack(side=LEFT, padx=5)
frame.pack()
tabview=CTkTabview(root)
tabview.pack()
tabview.add('KB')
tabview.add('COM')
CTkLabel(tabview.tab('COM'), text='Arduino Serial Input').pack()
comframe=CTkFrame(tabview.tab('COM'))
comframe.pack()
cb=CTkOptionMenu(comframe, values=['COM0', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9'])
cb.pack(side=LEFT)
start=CTkButton(comframe, text='Start Serial In', command=begin_serial)
start.pack(side=LEFT, padx=5)
key_enable=CTkSwitch(tabview.tab('KB'), text='Bind keyboard to drums')
key_enable.pack()
CTkLabel(tabview.tab('KB'), text='Mapping:\nSpace: Kick\nA/S: Snare\nD/J/K/L: Toms\nH: Open Hi-Hat\nG: Pedal Hi-Hat\nF: Closed Hi-Hat\nQ: Crash Cymbal 1\nP: Crash Cymbal 2\nO: Ride Cymbal 1\nW: Ride Cymbal 2\nX: Side Stick\nE/R: Bongos\nT/Y: Congas\nU/I: Timbales\nZ: Maracas\nC: Shaker\nV: Vibraslap\nB: Claves\nN: Woodblock\nM: Cowbell').pack()
Hovertip(controller_count, 'A red number indicates a low battery in one or more controllers')
Hovertip(patch_change, "Each patch correlates to a different sound set\n0: Standard Kit\n1: Alt. Kit\n8: Room Kit\n16: Power Kit\n24: Electronic Kit\n25: TR-808\n26: Dance Kit\n32: Jazz Kit\n40: Brush Kit\n48: Orchestral Percussion\nClick 'Apply Selected Patch' for the new patch to take effect.\nIf you're using the internal sampler, only patches 0, 1, and 25 will take effect.\nWARNING: If using patch 48, the drum selections may not match the output sounds.")
Hovertip(midiselect, 'Use to select an output for the program. Some features, like pan or patch selection, only work when an external MIDI output is selected')
root.protocol('WM_DELETE_WINDOW', close)
CTkLabel(tabview.tab('COM'), text='Serial Char Mapping:\nK: Kick\nS: Snare\nF: Closed Hi-Hat\nH: Open Hi-Hat\nG: Pedal Hi-Hat\nB: Floor Tom\nL: Low Tom\nM: Mid Tom\nN: High Tom\nQ: Crash Cymbal\nP: Ride Cymbal\nR: Rimshot').pack()
keyboard.Listener(on_press=on_press, on_release=on_release).start()
check_status()
root.mainloop()
