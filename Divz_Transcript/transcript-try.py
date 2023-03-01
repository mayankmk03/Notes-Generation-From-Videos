# Step 1 : Importing libararies
import speech_recognition as sr 
import moviepy.editor as mp

# Step 2: Video to Audio conversion

VidClip = mp.VideoFileClip("D:\Transcript\what-is-the-pythagoras-theorem-dont-memorise.mp4") 
VidClip.audio.write_audiofile("D:\Transcript\converted.wav")

# Step 3: Speech recognition

reco = sr.Recognizer()
audio = sr.AudioFile("D:\Transcript\converted.wav")
#Now, let's use the recognize_google() method to read our file. 
# This method requires us to use a parameter of the speech_recognition() module, the AudioData object.
#The Recognizer class has a record() method that can be used to convert our audio file to an AudioData object. 
# Then, pass the AudioFile object to the record() method
with audio as source:
  reco.adjust_for_ambient_noise(source)
  audio_file = reco.record(source)
result = reco.recognize_google(audio_file)

# Step 4: Finally exporting the result 

with open('D:\Transcript\SpeechText.txt',mode ='w') as file: 
   file.write("Recognized Speech Text:") 
   file.write("\n") 
   file.write(result) 
print("Text file ready!")