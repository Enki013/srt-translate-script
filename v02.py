import os
import shutil
import srt
from translate import Translator

def translate_srt_files(root_folder, target_lang):
    for dirpath, dirnames, filenames in os.walk(root_folder):
        # Sadece içinde SRT dosyaları bulunan klasörlere odaklan
        if any(file.lower().endswith('.srt') for file in filenames):
            # "en" klasörünü oluştur
            en_folder = os.path.join(dirpath, 'en')
            if not os.path.exists(en_folder):
                os.makedirs(en_folder)

            # "tr" klasörünü oluştur
            tr_folder = os.path.join(dirpath, 'tr')
            if not os.path.exists(tr_folder):
                os.makedirs(tr_folder)

            print(f"Klasör: {dirpath}")

            for filename in filenames:
                if os.path.splitext(filename)[1].lower() == '.srt':
                    # SRT dosyasının tam yolu
                    srt_path = os.path.join(dirpath, filename)

                    # SRT dosyasını "en" klasörüne kopyala
                    en_srt_path = os.path.join(en_folder, filename)
                    shutil.copy2(srt_path, en_srt_path)
                    print(f"Yedeklenen dosya: {en_srt_path}")

                    # Çeviri işlemini gerçekleştir
                    translated_srt_path = os.path.join(tr_folder, filename)
                    translate_srt_file(en_srt_path, translated_srt_path, target_lang)
                    print(f"Çevrilen dosya: {translated_srt_path}")

                    print()  # Bir sonraki dosya için boşluk bırak

def translate_srt_file(input_file, output_file, target_lang):
    # SRT dosyasını yükle
    with open(input_file, 'r', encoding='utf-8-sig') as f:
        srt_content = f.read()

    # SRT içeriğini ayrıştır
    subs = list(srt.parse(srt_content))

    # Her altyazıyı çevir
    translator = Translator(to_lang=target_lang)
    for sub in subs:
        sub.content = translator.translate(sub.content)

    # Çevrilen SRT içeriğini oluştur
    translated_srt_content = srt.compose(subs)

    # Çevrilen SRT dosyasını kaydet
    with open(output_file, 'w', encoding='utf-8-sig') as f:
        f.write(translated_srt_content)

# Kullanım örneği
root_folder = 'Flutter & Dart - The Complete Guide'  # Çalışma konumundaki ana klasör
target_lang = 'tr'  # Hedef dil kodu (Örneğin, 'de' Almanca için)

translate_srt_files(root_folder, target_lang)
