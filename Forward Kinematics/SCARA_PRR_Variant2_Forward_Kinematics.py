import numpy as np
import math
import PySimpleGUI as sg
import pandas as pd

# GUI code

sg.theme("DarkPurple2")

# Excel read code

EXCEL_FILE = 'SCARA_PRRV2_Design_Data.xlsx'
df = pd.read_excel(EXCEL_FILE)

# Lay-out code

layout = [
    [sg.Text('GROUP 4 - SCARA-PRR-Variant 2')],
    [sg.Text('Fill out the following fields:')],
     [sg.Text('a1 = '),sg.InputText(key='a1', size=(20,10)),sg.Text('d1 = '),sg.InputText(key='d1', size=(20,10))],
     [sg.Text('a2 = '),sg.InputText(key='a2', size=(20,10)),sg.Text('T2 = '),sg.InputText(key='T2', size=(20,10))],
     [sg.Text('a3 = '),sg.InputText(key='a3', size=(20,10)),sg.Text('T3 = '),sg.InputText(key='T3', size=(20,10))],
     [sg.Text('a4 = '),sg.InputText(key='a4', size=(20,10))],
     [sg.Button('Solve Forward Kinematics')],
     [sg.Frame('Position Vector: ',[[
         sg.Text('X = '),sg.InputText(key='X', size=(10,1)),
         sg.Text('Y = '),sg.InputText(key='Y', size=(10,1)),
         sg.Text('Z = '),sg.InputText(key='Z', size=(10,1))]])],
         [sg.Frame('H0_3 Transformation Matrix = ',[[sg.Output(size=(60,10))]])],
         [sg.Submit(), sg.Button('Clear Input'),sg.Exit()]
    ]

# Window Code
window = sg.Window('SCARA_PRRV2 Manipulator Forward Kinematics (Group4)',layout)

def clear_input():
    for key in values:
        window[key]('')
    return None

while True:
    event,values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Clear Input':
        clear_input()
    if event == 'Solve Forward Kinematics':
        # Forward Kinematic Codes
        a1 = values["a1"]
        a2 = values["a2"]
        a3 = values["a3"]
        a4 = values["a4"]

        d1 = values["d1"]
        T2 = values["T2"]
        T3 = values["T3"]

        T2 = (float(T2)/180.0)*np.pi # Theta 2 in radians
        T3 = (float(T3)/180.0)*np.pi # Theta 3 in radians

        PT = [[(0.0/180.0)*np.pi,(180.0/180.0)*np.pi,float(a2),float(a1)+float(d1)],
            [float(T2),(0.0/180.0)*np.pi,float(a3),0],
            [float(T3),(0.0/180.0)*np.pi,float(a4),0]]
        
        i = 0
        H0_1 = [[np.cos(PT[i][0]),-np.sin(PT[i][0])*np.cos(PT[i][1]),np.sin(PT[i][0])*np.sin(PT[i][1]),PT[i][2]*np.cos(PT[i][0])],
                [np.sin(PT[i][0]),np.cos(PT[i][0])*np.cos(PT[i][1]),-np.cos(PT[i][0])*np.sin(PT[i][1]),PT[i][2]*np.sin(PT[i][0])],
                [0,np.sin(PT[i][1]),np.cos(PT[i][1]),PT[i][3]],
                [0,0,0,1]]

        i = 1
        H1_2 = [[np.cos(PT[i][0]),-np.sin(PT[i][0])*np.cos(PT[i][1]),np.sin(PT[i][0])*np.sin(PT[i][1]),PT[i][2]*np.cos(PT[i][0])],
                [np.sin(PT[i][0]),np.cos(PT[i][0])*np.cos(PT[i][1]),-np.cos(PT[i][0])*np.sin(PT[i][1]),PT[i][2]*np.sin(PT[i][0])],
                [0,np.sin(PT[i][1]),np.cos(PT[i][1]),PT[i][3]],
                [0,0,0,1]]
        
        i = 2
        H2_3 = [[np.cos(PT[i][0]),-np.sin(PT[i][0])*np.cos(PT[i][1]),np.sin(PT[i][0])*np.sin(PT[i][1]),PT[i][2]*np.cos(PT[i][0])],
                [np.sin(PT[i][0]),np.cos(PT[i][0])*np.cos(PT[i][1]),-np.cos(PT[i][0])*np.sin(PT[i][1]),PT[i][2]*np.sin(PT[i][0])],
                [0,np.sin(PT[i][1]),np.cos(PT[i][1]),PT[i][3]],
                [0,0,0,1]]
        
        # print("H0_1=")
        # print(np.matrix(H0_1))
        # print("H1_2=")
        # print(np.matrix(H1_2))
        # print("H2_3=")
        # print(np.matrix(H2_3))

        H0_2 = np.dot(H0_1,H1_2)
        H0_3 = np.dot(H0_2,H2_3)

        print("H0_3=")
        print(np.matrix(H0_3))

        X0_3 = H0_3[0,3]
        print("X = ")
        print(X0_3)

        Y0_3 = H0_3[1,3]
        print("Y = ")
        print(Y0_3)

        Z0_3 = H0_3[2,3]
        print("Z = ")
        print(Z0_3)

    if event == 'Submit':
        df=df.append(values, ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)
        sg.popup('Data saved!')
        clear_input()
window.close()