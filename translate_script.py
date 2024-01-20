from translate import Translator
from datetime import datetime

# 500 karakter sınırını aşmamak için metni kelimelere ayırdık
def translate_large_text(text, target_language='en', word_limit=100):
    translator = Translator(to_lang=target_language)

    words = text.split()

    translated_words = [translator.translate(' '.join(words[i:i + word_limit])) for i in
                        range(0, len(words), word_limit)]

    translated_text = ' '.join(translated_words)
    return translated_text


def translate_file(input_file_path, output_file_path, target_language='en', word_limit=25):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        original_text = file.read()

    translated_text = translate_large_text(original_text, target_language=target_language, word_limit=word_limit)

    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(translated_text)


input_file_path = 'texts/transcription_20240120175720.txt'
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
output_file_path = f'texts/translated_output_{timestamp}.txt'
translate_file(input_file_path, output_file_path, target_language='tr', word_limit=25)
