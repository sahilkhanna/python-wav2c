from os.path import dirname, join as pjoin
import wave, struct
import matplotlib.pyplot as plt
import numpy as np

def decode_wav(wav_file_name:str, endian = 'big'):
    with wave.open(wav_file_name, mode = 'rb') as audio:
        channel, sampleWidth, rate, sampleLength, _ , _  = audio.getparams()
        bits = sampleWidth * 8
        data = audio.readframes(sampleLength)
        print(f'channel = {channel}, bits = {bits}, ' 
              f'rate = {rate}Hz, length = {sampleLength}')
        if endian == 'big':
            endianess = ">"
        else:
            endianess = "<"
        if sampleWidth == 1:
            chunkSize = f'{sampleLength}B'
        elif sampleWidth == 2:
            chunkSize = f'{sampleLength}h'
        elif sampleWidth == 3:
            chunkSize = f'{sampleLength}i'
        unpack_format = endianess+chunkSize
        d = struct.unpack(unpack_format, data)
        return d, sampleLength, bits, rate, channel

def wav_to_c(wav_data: list, len:int, bits:int, samplerate: int, channel=1 ):
    with open("sound_file.c", 'w') as sound_file:
        sound_file.write("#include <stdint.h>\n\n")
        sound_file.write("static const uint8_t wave_array[];\n")
        sound_file.write("char *wave_get(void){return (char*)wave_array;}\n")
        sound_file.write("uint32_t wave_get_size(void){return %d;}\n" % (len))
        sound_file.write("uint32_t wave_get_framerate(void){return %d;}\n" % samplerate)
        sound_file.write("uint32_t wave_get_bits(void){return %d;}\n" % (bits))
        sound_file.write("uint32_t wave_get_ch(void){return %d;}\n" % channel)
        sound_file.write("/* size : %d */\n" % (len))
        sound_file.write("static const uint8_t wave_array[]={\n")
        for bytes in wav_data:
            bytes
            sound_file.write("%d," % (bytes))
        sound_file.write("};\n")
    pass

def plot_wav(wav_data: list, length=100, rate=8000):
    time = np.linspace(0., length/rate, length)
    plt.plot(time, wav_data[:length], label="Left channel")
    plt.legend()
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.show()
    pass

def main():
    data_dir = pjoin(dirname(__file__))
    wav_fname = pjoin(data_dir, 'beep.wav')
    data, sampleLength, bits, rate, channel = decode_wav(wav_fname, 'little')
    wav_to_c(wav_data = data, len = sampleLength, bits = bits, samplerate = rate, channel = channel)
    plot_wav(data,sampleLength,rate)
    pass

if __name__ == "__main__":
    main()
