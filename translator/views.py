from django.shortcuts import render
from django.http import HttpResponseServerError
from django.utils.translation import gettext as _
from django.http import FileResponse

from .forms import TranslationForm
from .models import Translation
from googletrans import Translator
from gtts import gTTS
import os
import pygame
from django.core.files.storage import FileSystemStorage
from PyPDF2 import PdfReader
import tempfile


def translate(request):
    if request.method == 'POST':
        form = TranslationForm(request.POST, request.FILES)
        if form.is_valid():
            text = form.cleaned_data['text']
            target_language = form.cleaned_data['target_language']

            # Handle PDF file upload
            pdf_file = request.FILES.get('pdf_file')
            if pdf_file:
                # Process the PDF file
                pdf_text = extract_text_from_pdf(pdf_file)
                text += "\n\n" + pdf_text

            # Translate text
            translator = Translator()
            translation_result = translator.translate(text, dest=target_language)
            translated_text = translation_result.text

            try:
                # Save translation to the database
                translation = Translation.objects.create(
                    text=text,
                    source_language='en',
                    target_language=target_language,
                    translated_text=translated_text,
                    pdf_file=pdf_file
                )

                # Generate audio file
                audio_directory = os.path.join('media', 'audio')
                os.makedirs(audio_directory, exist_ok=True)  # Create directory if it doesn't exist
                audio_path = os.path.join(audio_directory, f'{translation.id}.mp3')
                tts = gTTS(translated_text, lang=target_language)
                tts.save(audio_path)
                translation.audio_file = audio_path
                translation.save()

                # Play audio using Pygame mixer
                pygame.init()
                pygame.mixer.init()
                pygame.mixer.music.load(audio_path)
                pygame.mixer.music.play()

                return render(request, 'translator/translation_result.html', {'translation': translation})

            except Exception as e:
                # Handle any exception that might occur during database or file operations
                return HttpResponseServerError(_(f"An error occurred: {str(e)}"))
    else:
        form = TranslationForm()

    return render(request, 'translator/translate.html', {'form': form})


def extract_text_from_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
    return text

