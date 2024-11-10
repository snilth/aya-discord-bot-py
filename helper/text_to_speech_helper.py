import discord
from gtts import gTTS
import asyncio
import os


FFMPEG_OPTIONS = {
    'options': '-vn',
    'executable': r'C:\ffmpeg\ffmpeg.exe'
}

async def text_to_speech(voice_client, message):
        try:
            speech = gTTS(text=message, lang="th", slow=False)
            speech.save("tts-audio.mp3")
            
            if voice_client.is_playing():
                voice_client.stop()
            
            source = discord.FFmpegPCMAudio("tts-audio.mp3", 
                                            **FFMPEG_OPTIONS)
            voice_client.play(source)

            while voice_client.is_playing():
                await asyncio.sleep(1)
            os.remove("tts-audio.mp3")
            
        except Exception as error:
            print(f"Error playing audio: {error}")