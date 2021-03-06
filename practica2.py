import matplotlib
import time
import pyaudio
import wave
import os
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
import numpy as np
import scipy.io
import scipy.io.wavfile

def saveAudio(filename, data):
    waveFile = wave.open(filename, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(data)
    waveFile.close()
    stream.stop_stream()

def recordAudio(archivo, stream):
    stream.start_stream()
    print("grabando...")
    frames=[]
    for i in range(0, int(RATE/CHUNK*duracion)):
        data=stream.read(CHUNK)
        frames.append(data)
    print("Grabación finalizada")
    saveAudio(archivo, b''.join(frames))

def playAudio(filename):
    wf = wave.open(filename, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format =
                    p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = wf.getframerate(),
                    output = True)
    # read data (based on the chunk size)
    data = wf.readframes(CHUNK)
    # play stream (looping from beginning of file to the end)
    while data:
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream() 
    stream.close()    
    p.terminate()

def plotTresAudios(archivo1, archivo2, archivo3):
    sampleRate, audioBuffer1 = scipy.io.wavfile.read(archivo1)
    sampleRate, audioBuffer2 = scipy.io.wavfile.read(archivo2)
    sampleRate, audioBuffer3 = scipy.io.wavfile.read(archivo3)

    print('Longitud del arreglo de datos de cada audio: ',len(audioBuffer1))
    duration = len(audioBuffer1)/sampleRate
    time = np.arange(0,duration,1/sampleRate) #time vector
    originalPlot = plt.figure(1)

    plt.subplot(3, 1, 1)
    plt.plot(time,audioBuffer1, '#e36b2c', label="Audio 1")
    plt.ylabel('Amplitud')
    plt.title("Audio 1, Audio 2 & Resultado")

    plt.subplot(3, 1, 2)
    plt.plot(time,audioBuffer2, '#6dc36d', label="Audio 2")
    plt.ylabel('Amplitud')

    plt.subplot(3, 1, 3)
    plt.plot(time,audioBuffer3, '#109dfa', label="Resultado")

    plt.legend()
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Amplitud')
    plt.show()

def plotDosAudios(archivo1, archivo2):
    sampleRate, audioBuffer1 = scipy.io.wavfile.read(archivo1)
    sampleRate, audioBuffer2 = scipy.io.wavfile.read(archivo2)

    print('Longitud del arreglo de datos de cada audio: ',len(audioBuffer1))
    duration = len(audioBuffer1)/sampleRate
    time = np.arange(0,duration,1/sampleRate) #time vector
    originalPlot = plt.figure(1)

    plt.subplot(2, 1, 1)
    plt.plot(time,audioBuffer1,'#6dc36d', label="Audio 1")
    plt.ylabel('Amplitud')
    plt.title("Audio 1 & Resultado")

    plt.subplot(2, 1, 2)
    plt.plot(time,audioBuffer2, '#109dfa', label="Audio 2")

    plt.legend()
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Amplitud')
    plt.show()

def plotAudios(archivo1, archivo2):
    sampleRate, audioBuffer1 = scipy.io.wavfile.read(archivo1)
    sampleRate, audioBuffer2 = scipy.io.wavfile.read(archivo2)
    print('Longitud del arreglo de datos de cada audio: ',len(audioBuffer1))
    duration = len(audioBuffer1)/sampleRate
    time = np.arange(0,duration,1/sampleRate) #time vector
    originalPlot = plt.figure(1)
    plt.plot(time,audioBuffer1, label="Audio 1")
    plt.plot(time,audioBuffer2, label="Audio 2")
    plt.legend()
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Amplitud')
    plt.title("Audio 1 & Audio 2")
    plt.show()

def plotAudio(archivo):
    global figureIndex
    figureIndex+=1
    sampleRate, audioBuffer = scipy.io.wavfile.read(archivo)
    print('Longitud del arreglo de datos: ',len(audioBuffer))
    duration = len(audioBuffer)/sampleRate
    time = np.arange(0,duration,1/sampleRate) #time vector
    figure = plt.figure(figureIndex)
    plt.plot(time,audioBuffer, label="Audio")
    plt.legend()
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Amplitud')
    plt.title("Audio")
    plt.title(os.path.basename(archivo))
    plt.show()

def opReflejo(archivo,filename):
    sampleRate, data1 = scipy.io.wavfile.read(archivo)
    wave = np.int16([0 for i in range(len(data1))])
    j = len(data1);
    for i in range(0, j):
        wave[i] = data1[j-1]
        j-=1    
    scipy.io.wavfile.write(filename, sampleRate, wave.astype(np.int16))

def opSumaResta(archivo1, archivo2, filename, factor):
    sampleRate, data1 = scipy.io.wavfile.read(archivo1)
    sampleRate, data2 = scipy.io.wavfile.read(archivo2)
    wavesSum = np.int16([0 for i in range(len(data1))])
    for i in range(0, len(data1)):
        ### read 1 frame and the position will updated ###
        wavesSum[i] = data1[i]+factor*data2[i]
    scipy.io.wavfile.write(filename, sampleRate, wavesSum.astype(np.int16))

def opAmplificacion(archivo1, filename, factor):
    sampleRate, data = scipy.io.wavfile.read(archivo1)
    newWave = np.int16([0 for i in range(len(data))])
    for i in range(0, len(data)):
        newWave[i] = factor*data[i]

    scipy.io.wavfile.write(filename, sampleRate, newWave.astype(np.int16))

def opDiezmacion(archivo1, filename, factor):
    sampleRate, data = scipy.io.wavfile.read(archivo1)
    leng = int(len(data)/factor)+ len(data)%factor
    newWave = np.int16([0 for i in range(leng)])
    index = 0
    for i in range(0, len(data)):
        if(i%factor==0):
            newWave[index] = data[i]
            index+=1
    scipy.io.wavfile.write(filename, sampleRate, newWave.astype(np.int16))

def opInterpolacion(archivo1, filename, factor, tipo):
    sampleRate, data = scipy.io.wavfile.read(archivo1)
    leng = int(len(data)*factor)
    newWave = np.int16([0 for i in range(leng)])
    index = 0

    increment = 0
    for i in range(0, leng):
        if(i%factor==0):
            newWave[i] = data[index]
            if(index==len(data)-1):
                sign = 1 if(data[index]<0) else -1
                increment = sign*int(data[index]/factor)
            else:
                sign = 1 if(data[index]<data[index+1]) else -1
                increment = sign*int(abs(data[index+1]-data[index])/factor)
            index+=1
        else:
            if(tipo==0):
                newWave[i] = 0
            elif(tipo==1):
                newWave[i] = data[index-1]
            elif(tipo==2):
                newWave[i] = newWave[i-1]+increment
                
    scipy.io.wavfile.write(filename, sampleRate, newWave.astype(np.int16))

def opDesplazamiento(archivo1, filename, factor):
    sampleRate, data = scipy.io.wavfile.read(archivo1)
    newWave = np.int16([0 for i in range(len(data))])
    index = 0
    if(factor>=0):
        for i in range(factor, len(data)):
            newWave[i] = data[index]
            index+=1
    else:
        index=abs(factor)
        for i in range(0, len(data)+factor-1):
            newWave[i] = data[index]
            index+=1

    scipy.io.wavfile.write(filename, sampleRate, newWave.astype(np.int16))

def opConvol(archivo1,archivo2,filename):
    sampleRate, data1 = scipy.io.wavfile.read(archivo1)
    sampleRate, data2 = scipy.io.wavfile.read(archivo2)
    waveConv = np.int16([0 for i in range(len(data1)+len(data2)-1)])
    tempSignal = np.int16([0 for i in range(len(data2))])
    #Atenuacion de señales
    for l in range(0,len(data1)):
        data1[l] = data1[l]/1200

    for k in range(0,len(data2)):
        data2[k] = data2[k]/1200

    waveConv = np.convolve(data1,data2,'full')

    ######################################################
    #Implementacion del algoritmo
    #Reflejo de la señal    
    
    """lenA2 = len(data2)
    for i in range(0,lenA2):
        tempSignal[i] = data2[lenA2-1]
        lenA2-=1
    data2=tempSignal;

    lenA1 = len(data1)
    lenA2 = len(data2)
    totLen = lenA1+lenA2-1
    #Algoritmo
    for i in range(0,totLen):
        a2_start = max(0,i-lenA1+1)
        a2_end = min(i+1,lenA2)
        a1_start = min(i,lenA1-1)
        for j in range(a2_start,a2_end):
            temp=data1[a1_start]*data2[j]
            waveConv[i] += temp 
     
            a1_start-=1"""
    ##########################################################

    print("Finalizado")
    scipy.io.wavfile.write(filename, sampleRate, waveConv.astype(np.int16))

FORMAT=pyaudio.paInt16
CHANNELS=1
RATE=44100
CHUNK=1025
duracion=3
dirname = os.path.dirname(__file__)
archivo1= os.path.join(dirname, "audio1.wav")
archivo2= os.path.join(dirname, "audio2.wav")
suma= os.path.join(dirname, "suma.wav")
resta= os.path.join(dirname, "resta.wav")
amplificacion= os.path.join(dirname, "amplificacion.wav")
atenuacion= os.path.join(dirname, "atenuacion.wav")
diezmacion= os.path.join(dirname, "diezmacion.wav")
interpolacion= os.path.join(dirname, "interpolacion.wav")
desplazamiento= os.path.join(dirname, "desplazamiento.wav")
conv= os.path.join(dirname, "convol.wav")
ref= os.path.join(dirname, "reflejo.wav")

audio=pyaudio.PyAudio()
stream=audio.open(format=FORMAT,channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
figureIndex = 1

seleccion = int(input("Selecciona: \n 1. Grabar audios \n 2. Utilizar audio1.wav y audio2.wav de carpeta \n"))
if seleccion==1:
    #Se graban dos audios para realizar operaciones
    input("Presione Enter para grabar el primer audio...")
    recordAudio(archivo1, stream)
    input("Presione Enter para grabar el segundo audio...")
    recordAudio(archivo2, stream)

#Cierra flujos de grabacion
stream.close()
audio.terminate()

menuMain = int(input("Menu O.B. \n 1.Suma\n 2.Resta\n 3.Amplificación\n 4.Atenuación\n 5.Reflejo\n 6.Desplazamiento\n 7.Diezmacion\n 8.Interpolación\n 9.Convolucion\n 0.Salir\n"))

while menuMain != 0:  
    if menuMain == 1: #Suma
        print("Reproduciendo audios...")
        playAudio("audio1.wav")        
        time.sleep(1)
        playAudio("audio2.wav")        
     #   plotAudios(archivo1, archivo2)

        opSumaResta(archivo1, archivo2, suma, 1)
     #   plotAudio(suma)
        plotTresAudios(archivo1, archivo2, suma)
        time.sleep(1)
        playAudio("suma.wav")
    elif menuMain == 2: #Resta
        print("Reproduciendo audios...")
        playAudio("audio1.wav")        
        time.sleep(1)
        playAudio("audio2.wav")        
        #plotAudios(archivo1, archivo2)

        opSumaResta(archivo1, archivo2, resta, -1)
        #plotAudio(resta)
        plotTresAudios(archivo1, archivo2, resta)
        time.sleep(1) #Para que no se reproduzcan inmediatamente
        playAudio("resta.wav")
    elif menuMain == 3: #Amplificación
        print("Reproduciendo audios...")
        playAudio("audio1.wav")        
       # plotAudio(archivo1)
        factor = int(input("Ingrese el factor de amplificación: "))
        opAmplificacion(archivo1, amplificacion, factor)
        #plotAudio(amplificacion)
        plotDosAudios(archivo1, amplificacion)
        playAudio("amplificacion.wav")
    elif menuMain == 4: #Atenuacion
        print("Reproduciendo audios...")
        playAudio("audio1.wav")        
        #plotAudio(archivo1)
        factor = int(input("Ingrese el factor de atenuacion: "))
        factor=1/factor     
        opAmplificacion(archivo1, atenuacion, factor)
        #plotAudio(atenuacion)
        plotDosAudios(archivo1, atenuacion)
        playAudio("atenuacion.wav")
    elif menuMain == 5: #Reflejo
        print("Reproduciendo audio...")
        playAudio("audio1.wav")
        #plotAudio(archivo1)

        opReflejo(archivo1,ref)
        #plotAudio(ref)
        plotDosAudios(archivo1, ref)        
        playAudio("reflejo.wav")
    elif menuMain == 6: #Desplazamiento
        print("Reproduciendo audio...")
        playAudio("audio1.wav")
        #plotAudio(archivo1)
        factor = int(input("Ingrese el factor de desplazamiento: "))
        
        opDesplazamiento(archivo1, desplazamiento, factor)
        #plotAudio(desplazamiento)
        plotDosAudios(archivo1, desplazamiento)
        playAudio("desplazamiento.wav")
    elif menuMain == 7: #Diezmacion
        print("Reproduciendo audio...")   
        playAudio("audio1.wav")
        plotAudio(archivo1)
        factor = int(input("\nIngrese el factor de diezmacion: "))
        
        opDiezmacion(archivo1, diezmacion, factor)
        plotAudio(diezmacion)
       
        playAudio("diezmacion.wav")
    elif menuMain == 8: #Interpolacion
        print("Reproduciendo audio...")
        playAudio("audio1.wav")   
        plotAudio(archivo1) 
        factor = int(input("\nIngrese el factor de interpolacion "))
        tipo = int(input("Ingrese el tipo de interpolacion (0=cero, 1=escalon, 2=lineal) "))   

        opInterpolacion(archivo1, interpolacion, factor, tipo)
        plotAudio(interpolacion)
        playAudio("interpolacion.wav")
    elif menuMain == 9: #Convolucion
        print("Reproduciendo audios...")
        playAudio("audio1.wav")        
        time.sleep(1)
        playAudio("audio2.wav")  
        plotAudios(archivo1, archivo2)

        opConvol(archivo1, archivo2, conv)
        plotAudio(conv)
        playAudio("convol.wav")
    else:
        print("Ingrese una opcion valida");

    menuMain = int(input("Menu O.B. \n 1.Suma\n 2.Resta\n 3.Amplificación\n 4.Atenuación\n 5.Reflejo\n 6.Desplazamiento\n 7.Diezmacion\n 8.Interpolación\n 9.Convolucion\n 0.Salir\n"))
    plt.show()