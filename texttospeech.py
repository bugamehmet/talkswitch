from gtts import gTTS
import os

text_file_path = "texts/translated_output_20240120233414.txt"

# Dosyadaki metni oku
with open(text_file_path, 'r', encoding='utf-8') as file:
    text_to_speak = file.read()

# gTTS ile metni ses dalgasına çevir
tts = gTTS(text=text_to_speak, lang='tr')

# Ses dosyasını kaydet
output_file_path = "output.mp3"
tts.save(output_file_path)

# Ses dosyasını oynat
os.system(f"start {output_file_path}")
