import PySimpleGUI as sg
import vlc
from sys import platform as PLATFORM
import os, io
from PIL import Image


inst = vlc.Instance()
list_player = inst.media_list_player_new()
media_list = inst.media_list_new([])
list_player.set_media_list(media_list)
player = list_player.get_media_player()


#------- GUI definition & setup --------#

sg.theme('DarkBlue')

def btn(name):  # a PySimpleGUI "User Defined Element" (see docs)
    return sg.Button(name, size=(10, 3), pad=(1, 1))

def make_player_window(player):    
    layout = [[sg.Image('', size=(300, 170), key='-VID_OUT-')],
              [btn('previous'), btn('play'), btn('next'), btn('pause'), btn('stop'), btn('show decision'), btn('show explanation'), btn('back')],
              [sg.Text('Load media to start', key='-MESSAGE_AREA-')], [sg.Text('filename: ', key='-FILE_NAME-')]]

    window = sg.Window('Mini Player', layout, element_justification='center', finalize=True, resizable=True)
    window['-VID_OUT-'].expand(True, True)     
    
    if PLATFORM.startswith('linux'):
        player.set_xwindow(window['-VID_OUT-'].Widget.winfo_id())
    else:
        player.set_hwnd(window['-VID_OUT-'].Widget.winfo_id())
             
    return window


def make_welcome_window():
    layout = [[sg.Text("Welcome to UEFA viewer", justification='center')],
              [sg.Text("Please enter or browse to path for the Resource folder of the RAP files and press Enter", justification='center')],
        [sg.Input(default_text='C:/Users/jpowe/Desktop/UEFA-2020-1/UEFA-2020-1/Resource', size=(60, 1), key='-FOLDER_LOCATION-'), sg.FolderBrowse(), sg.Button('Start')]]

    return sg.Window("Start", layout, location=(800,600), finalize=True, keep_on_top=True)


def make_index_window(layout):
   
    layout = [[sg.Text("Index window", key = "AA", size=(100,1))],
              layout,
              [btn("back")]]
    
    return sg.Window("index", layout, finalize=True, resizable = True)

def splitList(x):
    dictionary = dict()
    for word in x:
       f = word[0]
       if f in dictionary.keys():
            dictionary[f].append(word)
       else:
            dictionary[f] = [word]
    return dictionary


def make_decision_window():
    layout = [[sg.Image(key="-IMAGE-")],
              [btn("back"), btn("show explanation")]]
    
    return sg.Window("index", layout,element_justification='center', finalize=True, resizable = True)

def make_explanation_window():
    layout = [[sg.Image(key="-IMAGE-")],
              [btn("back"), btn("show decision")]]
    
    return sg.Window("index", layout, finalize=True,element_justification='center', resizable = True)


def Collapsible(layout, key, title='', arrows=(sg.SYMBOL_DOWN, sg.SYMBOL_UP), collapsed=False):
    """
    User Defined Element
    A "collapsable section" element. Like a container element that can be collapsed and brought back
    :param layout:Tuple[List[sg.Element]]: The layout for the section
    :param key:Any: Key used to make this section visible / invisible
    :param title:str: Title to show next to arrow
    :param arrows:Tuple[str, str]: The strings to use to show the section is (Open, Closed).
    :param collapsed:bool: If True, then the section begins in a collapsed state
    :return:sg.Column: Column including the arrows, title and the layout that is pinned
    """
    return sg.Column([[sg.T((arrows[1] if collapsed else arrows[0]), enable_events=True, k=key+'-BUTTON-'),
                       sg.T(title, enable_events=True, key=key+'-TITLE-')],
                      [sg.pin(sg.Column(layout, key=key, visible=not collapsed, metadata=arrows))]], pad=(0,0))


welcome_window, index_window, player_window, decision_window, explanation_window = make_welcome_window(), None, None, None, None
clipsPlayedInPlayer = 0
curr_clip = None
while True:
    window, event, values = sg.read_all_windows()
    
    
    if window == welcome_window:
        if event == "Start":
            welcome_window.hide()
            
            resource_path = values['-FOLDER_LOCATION-']
            clips_path = resource_path + "/medias/clips"
            decisions_path = resource_path + "/medias/images/decisions"
            explanations_path = resource_path + "/medias/images/explanations"
            try:            
                clips = os.listdir(clips_path)
                decisions = os.listdir(decisions_path)
                explanations = os.listdir(explanations_path)
            except:
                print("Bad path!")
                pass    
            
            clips_names = [x[:-4] for x in clips]
            clips_names = sorted(clips_names, key=lambda x: int(x[1:]))
            clips_names = splitList(clips_names)
            
            section_names = list(clips_names.keys())
            section_values = list(clips_names.values())
            
            # section objects
            sections = [[[sg.Button(y) for y in clips_names[x]]] for x in section_names ]
            
            layout = []
            
            for i, section in enumerate(sections):
                layout.append([Collapsible(section, str(i), str(section_names[i]),collapsed=True)])
            
            index_window = make_index_window(layout)
            index_window['AA'].update("Folder path: " + values['-FOLDER_LOCATION-'])
            index_window.maximize()
          
    if window == index_window:
        clipsPlayedInPlayer = 0

        if event in (sg.WIN_CLOSED, "back"):
            index_window.close()
            welcome_window.un_hide()
        
        for i in range(len(section_names)):
            if event.startswith(str(i)):
                window[str(i)].update(visible=not window[str(i)].visible)
                window[str(i)+'-BUTTON-'].update(window[str(i)].metadata[0] if window[str(i)].visible else window[str(i)].metadata[1])

        for values in section_values:
            if event in values:
                clipsPlayedInPlayer += 1
                index_window.hide()
                player_window = make_player_window(player)
                curr_clip = event
                loc = clips_path + "/" + curr_clip + ".mp4"   
                
                  
                index_of_clip = clips_names[curr_clip[0]].index(curr_clip)          
                media_list = inst.media_list_new([])
                media_list.add_media(loc)
                list_player.set_media_list(media_list)
                player_window.maximize()
                list_player.play()       
                # if values['-VIDEO_LOCATION-'] and not 'Video URL' in values['-VIDEO_LOCATION-']:
                
       
    if window == player_window:   

        if event in (sg.WIN_CLOSED, "back"):
            list_player.stop()
            player_window.close()
            index_window.un_hide() 
        
        if event == 'show decision':
            list_player.pause()            
            player_window.hide()
            
            filename = decisions_path + "/" + curr_clip + ".png"
            decision_window = make_decision_window()  
            
            if os.path.exists(filename):
                image = Image.open(filename)
                bio = io.BytesIO()
                image.save(bio, format="PNG")
                decision_window["-IMAGE-"].update(data=bio.getvalue())
                decision_window.maximize()                                             
        
        if event == 'show explanation':
            list_player.pause() 
            player_window.hide()
            filename = explanations_path + "/" + curr_clip + ".png"
            explanation_window = make_explanation_window()
            if os.path.exists(filename):
                image = Image.open(filename)
                bio = io.BytesIO()
                image.save(bio, format="PNG")
                explanation_window["-IMAGE-"].update(data=bio.getvalue())
                explanation_window.maximize()          
            
            
            
        if event == 'play':
            list_player.play()
        if event == 'pause':
            list_player.pause()
        if event == 'stop':
            list_player.stop()
        if event == 'next':
            list_player.stop()  
            
            num_of_clips_in_section = len(clips_names[curr_clip[0]]) 
                    
            index = clips_names[curr_clip[0]].index(curr_clip)             
            next_index = 0 if index + 1 + clipsPlayedInPlayer >= num_of_clips_in_section else index + 1
            
            # next_index += clipsPlayedInPlayer
            if clipsPlayedInPlayer != None:
                clipsPlayedInPlayer+= 1 
            next_event = clips_names[curr_clip[0]][next_index]            
            new_loc = clips_path + "/" + next_event + ".mp4"                            
            media_list = inst.media_list_new([])
            media_list.add_media(new_loc)
            list_player.set_media_list(media_list)             
            list_player.play()
            list_player.play()
            curr_clip = next_event

        if event == 'previous':
            list_player.previous()      # first call causes current video to start over
            list_player.previous()      # second call moves back 1 video from current
            list_player.play()
        if player.is_playing():
            window['-FILE_NAME-'].update(curr_clip)
            window['-MESSAGE_AREA-'].update("{:02d}:{:02d} / {:02d}:{:02d}".format(*divmod(player.get_time()//1000, 60),
                                                                     *divmod(player.get_length()//1000, 60)))
        # else:
        #     window['-MESSAGE_AREA-'].update('Load media to start' if media_list.count() == 0 else 'Ready to play media' )

    
    if window == decision_window:
        if event in (sg.WIN_CLOSED, "back"):
            decision_window.close()
            player_window.un_hide()
            player_window.maximize()
            
        if event == 'show explanation':
            decision_window.hide()
            filename = explanations_path + "/" + curr_clip + ".png"
            explanation_window = make_explanation_window()
            if os.path.exists(filename):
                image = Image.open(filename)
                bio = io.BytesIO()
                image.save(bio, format="PNG")
                explanation_window["-IMAGE-"].update(data=bio.getvalue())
                explanation_window.maximize()          
    
    if window == explanation_window:
        if event in (sg.WIN_CLOSED, "back"):
            explanation_window.close()
            player_window.un_hide()   
            player_window.maximize()
            
        if event == 'show decision':
            explanation_window.hide()
            
            filename = decisions_path + "/" + curr_clip + ".png"
            decision_window = make_decision_window()  
            
            if os.path.exists(filename):
                image = Image.open(filename)
                bio = io.BytesIO()
                image.save(bio, format="PNG")
                decision_window["-IMAGE-"].update(data=bio.getvalue())
                decision_window.maximize()                
          
    
    # event, values = window.read(timeout=1000)       # run with a timeout so that current location can be updated
    if event == sg.WIN_CLOSED:
        break
    
    
    
    
window.close()
window_back.close()