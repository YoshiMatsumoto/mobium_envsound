#coding:utf-8
import wave
import numpy as np
import matplotlib.pyplot as plt
import random

#wavデータのロード
def wave_load(filename):
    # open wave file
    wf = wave.open(filename,'r')
    channels = wf.getnchannels()

    # load wave data
    chunk_size = wf.getnframes()
    #amp  = (2**8) ** wf.getsampwidth() / 2
    data = wf.readframes(chunk_size)   # バイナリ読み込み
    data = np.frombuffer(data,'int16') # intに変換

    return data[::2], data[1::2]

#テストデータの作成
def create_test_data(left, right):
    arr = []
    for i in range(0, len(right)-1):
        #複素数のベクトル化
        temp = np.array([])
        temp = np.append(temp, left[i].real)
        temp = np.append(temp, left[i].imag)
        temp = np.append(temp, right[i].real)
        temp = np.append(temp, right[i].imag)
        arr.append(temp)

    return np.array(arr)


def fft_load(count,filename,size,start,end):
    '''
    count = グラフに入れたい数
    instrument = 楽器のディレクトリ
    size = FFTのサンプル数（２＊＊ｎ）
    start　=乱数の開始位置
    end = 乱数の終点位置

    '''
    st = 10000   # サンプリングする開始位置
    hammingWindow = np.hamming(size)    # ハミング窓
    fs = 44100 #サンプリングレート
    d = 1.0 / fs #サンプリングレートの逆数
    freqList = np.fft.fftfreq(size, d)

    for i in range(count):
        n = random.randint(start,end)
        wave = wave_load(filename)[1]
        windowedData = hammingWindow * wave[st:st+size]  # 切り出した波形データ（窓関数あり）
        data = np.fft.fft(windowedData)
        data = data / max(abs(data)) # 0~1正規化
        plt.plot(freqList,abs(data))

    plt.axis([0,fs/16,0,1]) #第二引数でグラフのy軸方向の範囲指定
    plt.xlabel("Frequency[Hz]")
    plt.ylabel("amplitude spectrum")
    plt.show()

    return data

data = wave_load("data/wav/out2.wav")
print(create_test_data(data[0], data[1]))

# fft_load(1,"data/wav/out2.wav",1024,0,1000)
