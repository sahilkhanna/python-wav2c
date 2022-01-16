from os.path import dirname, join as pjoin
from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np

def wav_to_c(wav_data: list, samplerate: int, len:int):
    with open("sound_file.c", 'w') as sound_file:
        sound_file.write("#include <stdint.h>\n\n")
        sound_file.write("static const uint8_t wave_array[];\n")
        sound_file.write("char *wave_get(void){return (char*)wave_array;}\n")
        sound_file.write("uint32_t wave_get_size(void){return %d;}\n" % (len))
        sound_file.write("uint32_t wave_get_framerate(void){return %d;}\n" % samplerate)
        sound_file.write("uint32_t wave_get_bits(void){return %d;}\n" % (16))
        sound_file.write("uint32_t wave_get_ch(void){return %d;}\n" % 1)
        sound_file.write("/* size : %d */\n" % (len))
        sound_file.write("static const uint8_t wave_array[]={\n")
        
        # print(wav_data[10:20])
        # wav_data = np.array(wav_data) - 0x7F
        
        # print(wav_data[10:20])
        for bytes in wav_data:
            bytes
            sound_file.write("%d," % (bytes))
        sound_file.write("};\n")
    pass

def main():
    data_dir = pjoin(dirname(__file__))
    wav_fname = pjoin(data_dir, 'beep.wav')
    samplerate, data = wavfile.read(wav_fname)
    print(f"rate :{samplerate}")
    length = data.shape[0] / samplerate
    time = np.linspace(0., length, data.shape[0])
    wav_to_c(data, samplerate, len(data))
    print(data)
    plt.plot(time, data[:], label="Left channel")
    plt.legend()
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.show()
    pass

if __name__ == "__main__":
    main()
