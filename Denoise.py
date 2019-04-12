from scipy import signal
import numpy as np
import wave
import struct
# 時系列のサンプルデータ作成
dt = 0.01                       # サンプリング間隔
f = 1                           # 周波数
fn = 1/(2*dt)                   # ナイキスト周波数
# パラメータ設定
fp = 2                          # 通過域端周波数[Hz]
fs = 3                          # 阻止域端周波数[Hz]
gpass = 1                       # 通過域最大損失量[dB]
gstop = 40                      # 阻止域最小減衰量[dB]
# 正規化
Wp = fp/fn
Ws = fs/fn

N = 256
step = 2 ** 8 #512
steps = 128
batch = 32
start = 416500
frames = 200
samples = 32

wavfile = 'data/input/190411160527.wav'
wr = wave.open(wavfile, "rb")
ch = wr.getnchannels()
width = wr.getsampwidth()
fr = wr.getframerate()
fn = wr.getnframes()

origin = wr.readframes(wr.getnframes())
data = origin[start:start+N * samples * (steps + 1) * 4]
wr.close()

X = np.frombuffer(data, dtype="int16") /  32768.0
# left = X[::2]
# right = X[1::2]

N, Wn = signal.buttord(Wp, Ws, gpass, gstop)
b1, a1 = signal.butter(N, Wn, "low")
X = signal.filtfilt(b1, a1, X)


outf = 'output/denoise.wav'
X = X.astype('int16')
outd = struct.pack("h" * len(X), *X)
ww = wave.open(outf, 'w')
ww.setnchannels(ch)
ww.setsampwidth(width)
ww.setframerate(fr)
ww.writeframes(outd)
ww.close()
