import yt_dlp as youtube_dl
import nltk
import whisper
import pytextrank
import spacy
from simplet5 import SimpleT5
import moviepy.editor as me
import threading
from pathlib import Path


class NotesMaker():

    def __init__(self) -> None:
        self.t5_model = self.__load_simplet5()
        self.wh_model = self.__load_whisper()
        self.nlp = self.__load_spacy()
        self.uploaded = False
        self.transcript_generated = False
        self.notes_generated = False
        # a = threading.Thread(target=self.__load_simplet5)
        # b = threading.Thread(target=self.__load_whisper)
        # c = threading.Thread(target=self.__load_spacy)
        # self.model = a.start()
        # self.model_wh = b.start()
        # self.nlp = c.start()
        # c.join()
        # b.join()
        # a.join()

    def __load_simplet5(self):
        model = SimpleT5()
        model.load_model(
            "t5", r"C:\Users\adiph\OneDrive\Documents\KJ_Somaiya\Codes\Python_and_SVU\mini-project-sem-vi\compiling_all\testing_t5_trained\model_hai\content\outputs\simplet5-epoch-4-train-loss-1.7187-val-loss-2.036", use_gpu=False)

        return model

    def __load_whisper(self):
        return whisper.load_model("tiny")

    def __load_spacy(self):
        nlp = spacy.load("en_core_web_lg")
        nlp.add_pipe("textrank")
        return nlp

    def __gen_para_summary(self, tile) -> tuple:
            
        doc = self.nlp(tile)
        result = []
        subheading = self.t5_model.predict(tile)

        for sent in doc._.textrank.summary(limit_phrases=2, limit_sentences=5):
            result.append(sent)
        # tile = list(processed_str._.textrank.summary(limit_phrases=2, limit_sentences=10))[0]

        return (subheading,"".join(list(map(str, result))))

    def __get_text(self) -> str:
        text = ""
        with open('transcript.txt', 'r', encoding='utf-8') as f:
            text = f.read()
        return text

    def __set_text(self, text) -> str:
        with open('transcript.txt', 'w', encoding='utf-8') as f:
            f.write(text)

        return text

    def get_aud_from_link(self, link: str) -> int:
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'wav',
                    'preferredquality': '192',
                }],
                'outtmpl': 'audio_file'
            }

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                duration = ydl.extract_info(link)["duration"]

                if duration > 600 or duration < 300:
                    print("Time Limit Exceeded!")
                    return 0
                else:
                    # ydl.download(link)
                    print("audio_file downloaded!")
                    self.uploaded = True

        except:
            print("Connection Error")
            return None

        return duration

    def get_aud_from_vid(self, path: str) -> None:
        try:
            video = me.VideoFileClip(path)
            print(video.duration)
            if video.duration > 600 or video.duration < 300:
                print("Not in the given video length range.")
                return 0
            else:

                audio = video.audio
                audio.write_audiofile("audio_file.wav")
                duration = video.duration

                print("audio_file downloaded!")
                self.uploaded = True
        except:
            print("Connection error!")
            return None

        return duration

    def gen_transcript(self) -> str:
        if not self.uploaded:
            print("No link or video uploaded.")
            return False

        audio = "audio_file.wav"
        result = self.wh_model.transcribe(audio, fp16=False)

        self.__set_text(result["text"])
        self.transcript_generated = True
        return result["text"]

    def gen_notes(self) -> bool:
        if not self.uploaded:
            print("No link or video uploaded.")
            return False
        
        if not self.transcript_generated:
            print("Transcript not generated!")
            return False
        
        text_corpus = self.__get_text()
        data_to_segment = ".\n\n".join(text_corpus.split("."))
        fileheading = self.t5_model.predict(text_corpus)

        ttt = nltk.tokenize.TextTilingTokenizer(w=25)
        tiles = ttt.tokenize(data_to_segment)
        print(len(tiles))

        for i in range(len(tiles)):
            tiles[i] = tiles[i].replace('\n\n', '')

        with open("paras.txt", "w", encoding="utf-8") as f:
            f.write(f"Main Topic: {fileheading[0]}\n\n")

            for idx, tile in enumerate(tiles):
                subheading, para = self.__gen_para_summary(tile)

                f.write(f"Topic {idx + 1}: {subheading[0]}\n\n")
                f.write(para)
                f.write("\n\n")

            print("Notes are Ready!")

        self.notes_generated = True
        return True


if __name__ == "__main__":
    nm = NotesMaker()
    duration = nm.get_aud_from_link("https://www.youtube.com/watch?v=2W85Dwxx218")
    # nm.gen_notes()
    transcript = nm.gen_transcript()
    nm.gen_notes()