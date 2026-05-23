import threading
from AudioTranscriber import AudioTranscriber
from GPTResponder import GPTResponder  
import customtkinter as ctk
import AudioRecorder 
import queue
import time
import sys
import TranscriberModels
import subprocess

def write_in_textbox(textbox, text):
    textbox.delete("0.0", "end")
    textbox.insert("0.0", text)

def update_transcript_UI(transcriber, textbox):
    transcript_string = transcriber.get_transcript()
    write_in_textbox(textbox, transcript_string)
    # افزایش نرخ بازخوانی به 150 میلی‌ثانیه برای نرم‌تر و سریع‌تر شدن ظاهر زیرنویس
    textbox.after(150, update_transcript_UI, transcriber, textbox)

def update_response_UI(responder, textbox):
    response_string = responder.response
    write_in_textbox(textbox, response_string)
    textbox.after(150, update_response_UI, responder, textbox)

def clear_context(transcriber, speaker_queue, mic_queue):
    transcriber.clear_transcript_data()
    with speaker_queue.mutex:
        speaker_queue.queue.clear()
    with mic_queue.mutex:
        mic_queue.queue.clear()

def create_ui_components(root, transcriber, speaker_queue, mic_queue):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    root.title("Ecoute")
    root.geometry("1000x800") 

    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    
    main_frame = ctk.CTkFrame(root)
    main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
    
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_rowconfigure(0, weight=1) 
    main_frame.grid_rowconfigure(1, weight=1) 
    main_frame.grid_rowconfigure(2, weight=0) 

    transcript_textbox = ctk.CTkTextbox(
        main_frame, 
        font=("Arial", 20), 
        text_color='#FFFCF2', 
        wrap="word"
    )
    transcript_textbox.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))

    response_textbox = ctk.CTkTextbox(
        main_frame, 
        font=("Arial", 20), 
        text_color='#00FF00', 
        wrap="word"
    )
    response_textbox.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))

    clear_button = ctk.CTkButton(
        main_frame, 
        text="Clear Transcript", 
        command=lambda: clear_context(transcriber, speaker_queue, mic_queue)
    )
    clear_button.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))

    return transcript_textbox, response_textbox

def main():
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        print("ERROR: The ffmpeg library is not installed. Please install ffmpeg and try again.")
        return

    root = ctk.CTk()
    speaker_queue = queue.Queue()
    mic_queue = queue.Queue()

    # تنظیمات سرعت فشرده برای کاهش حجم بافرهای صوتی (کاهش تأخیر)
    user_audio_recorder = AudioRecorder.DefaultMicRecorder()
    speaker_audio_recorder = AudioRecorder.DefaultSpeakerRecorder()
    
    # تلاش برای اعمال ضریب زمانی سریع‌تر روی نمونه‌بردار در صورت پشتیبانی ماژول
    for recorder in [user_audio_recorder, speaker_audio_recorder]:
        if hasattr(recorder, 'record_timeout'):
            recorder.record_timeout = 1.5
        if hasattr(recorder, 'phrase_timeout'):
            recorder.phrase_timeout = 2.0

    user_audio_recorder.record_into_queue(mic_queue)
    time.sleep(1) # کاهش زمان معطلی اولیه برای لود سریع‌تر
    speaker_audio_recorder.record_into_queue(speaker_queue)

    model = TranscriberModels.get_model('--api' in sys.argv)

    transcriber = AudioTranscriber(user_audio_recorder.source, speaker_audio_recorder.source, model)
    
    # تلاش برای تنظیم پارامتر سکوت مستقیماً روی ترنسکرایبر
    if hasattr(transcriber, 'phrase_timeout'):
        transcriber.phrase_timeout = 2.0

    transcribe = threading.Thread(target=transcriber.transcribe_audio_queue, args=(speaker_queue, mic_queue))
    transcribe.daemon = True
    transcribe.start()

    responder = GPTResponder()
    respond = threading.Thread(target=responder.respond_to_transcriber, args=(transcriber,))
    respond.daemon = True
    respond.start()

    transcript_textbox, response_textbox = create_ui_components(root, transcriber, speaker_queue, mic_queue)

    print("READY")

    update_transcript_UI(transcriber, transcript_textbox)
    update_response_UI(responder, response_textbox) 

    root.mainloop()

if __name__ == "__main__":
    main()
