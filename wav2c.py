
import matplotlib.pyplot as plt
import os
import codecs
import binascii
from bitstring import BitArray
import numpy as np

# get hex data
def wav2hex(filename:str, bit_range:int):
	'''
	Get hex data from file
	Select sound data convert that to selected bit length
	'''
	temp,data = "",[]
	filename = filename.split(".")[0] if "." in filename else filename
	#Get hex data from file and split into 16 bit chunks
	with open(f"{filename}.wav", 'rb') as f:
	    for chunk in iter(lambda: f.read(32), b''):
	    	hex_chunk = str(binascii.hexlify(chunk))[2:-1]
	    	for i, word in enumerate(hex_chunk):
	    		if (i+1)%2 == 0:
	    			temp += word
	    			data.append(temp)
	    			temp = ""
	    		else:
	    			temp += word
	    	temp = ""

	## Remove header from data and convert it into something readable
	## Sample rate is found in the header
	header = data[:44]
	data = data[44:]
	sample_rate, BitsPerSample = metadata(header)
	BitsPerSample = BitsPerSample[1]/BitsPerSample[0] 

	data_temp = []
	for i, byte in enumerate(data):
		if i > len(data) - len(data)*0.005: #Last couple of samples seems to be noise or potentially a footer
			break
		if (i+1) % 2 == 0:
			data_temp.append(BitArray(hex = byte[::1]).int/((2**(BitsPerSample-1))-1))
	data = data_temp

	if "sample_data.txt" in os.listdir():
		mode = input("sample_data.txt exists, append or overwrite file? [a/o]")
		mode = "a" if "a" in mode else "w+"
	f = open("sample_data.txt",mode)

	## Output sound sequence in the form of a c struct
	data_string = f"\nSound {filename} = {{{len(data_temp)}, {sample_rate[0]},{{"
	for sample in data_temp:
		data_string += str(int(sample*(2**(bit_range-1)-1)+(2**(bit_range-1)))) + ","

	data_string = data_string[:-1] + "}};"
	f.write(data_string)
	f.close()
	return data_string

def metadata(header):
	'''
	Converts the 44 byte header to something readable using the table below: (src = http://soundfile.sapp.org/doc/WaveFormat/)
	Positions	Sample Value	Description
	1 - 4	"RIFF"	Marks the file as a riff file. Characters are each 1 byte long.
	5 - 8	File size (integer)	Size of the overall file - 8 bytes, in bytes (32-bit integer). Typically, you'd fill this in after creation.
	9 -12	"WAVE"	File Type Header. For our purposes, it always equals "WAVE".
	13-16	"fmt "	Format chunk marker. Includes trailing null
	17-20	16	Length of format data as listed above
	21-22	1	Type of format (1 is PCM) - 2 byte integer
	23-24	2	Number of Channels - 2 byte integer
	25-28	44100	Sample Rate - 32 byte integer. Common values are 44100 (CD), 48000 (DAT). Sample Rate = Number of Samples per second, or Hertz.
	29-32	176400	(Sample Rate * BitsPerSample * Channels) / 8.
	33-34	4	(BitsPerSample * Channels) / 8.1 - 8 bit mono2 - 8 bit stereo/16 bit mono4 - 16 bit stereo
	35-36	16	Bits per sample
	37-40	"data"	"data" chunk header. Marks the beginning of the data section.
	41-44	File size (data)	Size of the data section.
	'''
	stack = ["RIFF","size","WAVE","fmt","data_length","pcm_and_ch","sample_rate","nr","BitsPerSample","data","file_size"]

	head_temp = {}
	temp = ""

	while len(stack) != 0:
		curr_ins = stack.pop(0)
		head_temp[curr_ins] = []

		byte_len = 4
		curr_data = header[:byte_len]
		header = header[byte_len:]
		if(curr_ins == "RIFF") or (curr_ins == "WAVE")  or (curr_ins == "fmt") or (curr_ins == "data"):
			head_temp[curr_ins] = "".join([chr(int(i,16)) for i in curr_data])
		elif(curr_ins == "size"):
			head_temp[curr_ins] = int("".join(curr_data[::-1]),16)
		elif(curr_ins == "data_length"):
			head_temp[curr_ins] = "".join(curr_data[::-1])
		elif(curr_ins == "pcm_and_ch"):
			head_temp[curr_ins] = ["PCM" if int("".join(curr_data[0:2][::-1]),16) == 1 else "Compression, check this","Mono" if int("".join(curr_data[2:4][::-1]),16) == 1 else "Stereo"]
		elif(curr_ins == "sample_rate") or (curr_ins == "nr") or (curr_ins == "file_size"):
			head_temp[curr_ins] = [int("".join(curr_data[::-1]),16)]
		elif (curr_ins == "BitsPerSample"):
			head_temp[curr_ins] = [int("".join(curr_data[0:2][::-1]),16),int("".join(curr_data[2:4][::-1]),16)]
	print(head_temp)
	return head_temp["sample_rate"], head_temp["BitsPerSample"]



if __name__  == "__main__":
	file = input("Give me a .wav file \n")
	bit_range = int(input("Bit range of output? [8,16,...] ex: 8 bit(0 - 255) \n"))
	data_string = wav2hex(file, bit_range) # header is a hex string array
	print("Converted and written to data_sample.txt")






















# print(re.sub([^\x],'',a))
