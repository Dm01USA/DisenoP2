import time

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
matplotlib.use('Agg')
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, LogLevels
from brainflow.ml_model import MLModel, BrainFlowMetrics, BrainFlowClassifiers, BrainFlowModelParams
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations, NoiseTypes
import mne
import numpy as np
import pandas as pd
from brainflow.data_filter import DataFilter

fig = plt.figure(figsize=(5, 4), dpi=100)
t = np.arange(0, 3, .01)
fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))
BoardShim.enable_dev_board_logger()
# use synthetic board for demo
params = BrainFlowInputParams()
params.serial_port = "COM3"
#board = BoardShim(BoardIds.SYNTHETIC_BOARD.value, params)
board = BoardShim(BoardIds.GANGLION_BOARD, params)
board.prepare_session()
#matplotlib.use("TkAgg")

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg
# Define the window layout
text="Plot"
errfound=""
err=5
layout = [
    [sg.Text(text)],
    [sg.Multiline(size=(10, 2), key='textbox')],
    [sg.Canvas(key="-CANVAS-")],
    [sg.Button("Calibration"),sg.Button("Start")],[sg.Image(key="-IMAGE-",size=(50,50)),sg.VerticalSeparator(),sg.Image(key="-IMAGE2-")],[sg.Text(key="ERR"),sg.Text(key="ERR1")],
]

# Create the form and show it without the plot
window = sg.Window(
    "Matplotlib Single Graph",
    layout,
    location=(0, 0),
    finalize=True,
    element_justification="center",
    font="Helvetica 18",
    resizable=True,
)

# Add the plot to the window


while True:
    event, values = window.read()
    if event in (None, 'Close Window'): # if user closes window or clicks cancel
        break
    if event=="Calibration":
        maxval_cal=np.array([0,0,0,0])
        minval_cal=np.array([0,0,0,0])
        board.start_stream()
        tiempo=values['textbox']
        time.sleep(int(tiempo))
        data = board.get_board_data()
        DataFilter.write_file(data, 'test2.csv', 'w')
        #eeg_channels = BoardShim.get_eeg_channels(BoardIds.SYNTHETIC_BOARD.value)
        eeg_channels = BoardShim.get_eeg_channels(BoardIds.GANGLION_BOARD)
        eeg_data = data[eeg_channels, :]
        eeg_data = eeg_data / 1000000  # BrainFlow returns uV, convert to V for MNE

        # Creating MNE objects from brainflow data arrays
        ch_types = ['eeg'] * len(eeg_channels)
        #ch_names = BoardShim.get_eeg_names(BoardIds.SYNTHETIC_BOARD.value)
        #sfreq = BoardShim.get_sampling_rate(BoardIds.SYNTHETIC_BOARD.value)
        #ch_names = BoardShim.get_eeg_names(BoardIds.GANGLION_BOARD)
        #sfreq = BoardShim.get_sampling_rate(BoardIds.GANGLION_BOARD)
        sfreq = 200
        #ch_names = ['1','2', '3', '4','5','6', '7', '8','9','10', '11', '12','13','14', '15', '16']
        ch_names = ['1','2', '3', '4']
        info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types=ch_types)
        raw = mne.io.RawArray(eeg_data, info)
        # its time to plot something!
        raw.plot_psd(average=True)
        plt.savefig('psd.png')
        #board_id=BoardIds.SYNTHETIC_BOARD.value
        board_id=BoardIds.GANGLION_BOARD.value
        eeg_channels = BoardShim.get_eeg_channels(board_id)
        DataFilter.remove_environmental_noise(data[0], BoardShim.get_sampling_rate(board_id),
                                                  NoiseTypes.FIFTY.value)
        DataFilter.remove_environmental_noise(data[1], BoardShim.get_sampling_rate(board_id),
                                                  NoiseTypes.FIFTY.value)
        DataFilter.remove_environmental_noise(data[2], BoardShim.get_sampling_rate(board_id),
                                                  NoiseTypes.FIFTY.value)
        DataFilter.remove_environmental_noise(data[3], BoardShim.get_sampling_rate(board_id),
                                                  NoiseTypes.FIFTY.value)
        
        df = pd.DataFrame(np.transpose(data))
        size3=df.shape
        for i in range(1,5):
         for k in range(1,size3[0]):
          if df.iloc[k][i]>maxval_cal[i-1]:
           maxval_cal[i-1]=df.iloc[k][i]
          elif df.iloc[k][i]<maxval_cal[i-1]:
           if df.iloc[k][i]>=minval_cal[i-1]: 
            minval_cal[i-1]=df.iloc[k][i]
        plt.figure()
        df[eeg_channels].plot(subplots=True)
        df.to_csv('CALIB.csv')
        plt.savefig('psd1.png')
        window["-IMAGE-"].update('psd1.png',subsample=1)
        #draw_figure(window["-CANVAS-"].TKCanvas, )
        board.stop_stream()
    if event=="Start":
        num_discrep=np.array([0,0,0,0])
        board.start_stream()
        tiempo=values['textbox']
        time.sleep(int(tiempo))
        data1 = board.get_board_data()
        DataFilter.write_file(data, 'test3.csv', 'w')
        DataFilter.remove_environmental_noise(data[0], BoardShim.get_sampling_rate(board_id),
                                                  NoiseTypes.FIFTY.value)
        DataFilter.remove_environmental_noise(data[1], BoardShim.get_sampling_rate(board_id),
                                                  NoiseTypes.FIFTY.value)
        DataFilter.remove_environmental_noise(data[2], BoardShim.get_sampling_rate(board_id),
                                                  NoiseTypes.FIFTY.value)
        DataFilter.remove_environmental_noise(data[3], BoardShim.get_sampling_rate(board_id),
                                                  NoiseTypes.FIFTY.value)
        
        df1 = pd.DataFrame(np.transpose(data1))
        df1.to_csv('START.csv')
        plt.figure()
        df1[eeg_channels].plot(subplots=True)
        plt.savefig('psd2.png')
        size2=df1.shape

        for i in range(1,5):
         for k in range(1,size2[0]):
          if df1.iloc[k][i]>maxval_cal[i-1]+1:
           num_discrep[i-1]=num_discrep[i-1]+1
           

        window["-IMAGE2-"].update('psd2.png',subsample=1)
        #window["ERR"].update('hanning%s.pdf' %err )
        window["ERR"].update('Se encontraron el siguiente numero de discrepancias en cada canal:')
        window["ERR1"].update(num_discrep)
        board.stop_stream()
    print('You entered in the textbox:')
    print(values['textbox'])  # get the content of multiline via its unique key

window.close()