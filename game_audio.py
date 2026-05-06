import random
import pykraken as kn


day_background_sound = None
night_background_sound = None
current_background_sound = None

interact_sound = None
bone_sounds = None


def load_audio():
    global day_background_sound
    global night_background_sound
    global interact_sound
    global bone_sounds

    if day_background_sound is None:
        day_background_sound = kn.mixer.load_stream("audio/Background.wav")
        day_background_sound.looping = False
        day_background_sound.volume = 0.65

    if night_background_sound is None:
        night_background_sound = kn.mixer.load_stream("audio/BackgroundNight.wav")
        night_background_sound.looping = False
        night_background_sound.volume = 0.65

    if interact_sound is None:
        interact_sound = kn.mixer.load_sample("audio/interact.wav")
        interact_sound.volume = 0.8

    if bone_sounds is None:
        bone_sounds = [
            kn.mixer.load_sample("audio/bones1.wav"),
            kn.mixer.load_sample("audio/bones2.wav")
        ]

        for bone_sound in bone_sounds:
            bone_sound.volume = 0.55


def play_day_background():
    global current_background_sound

    load_audio()

    stop_background()

    current_background_sound = day_background_sound
    current_background_sound.seek(0)
    current_background_sound.play()


def play_night_background():
    global current_background_sound

    load_audio()

    stop_background()

    current_background_sound = night_background_sound
    current_background_sound.seek(0)
    current_background_sound.play()


def stop_background():
    global current_background_sound

    load_audio()

    if current_background_sound is not None:
        current_background_sound.stop()


def play_interact():
    load_audio()
    interact_sound.play()


def play_bone_step(volume=0.55):
    load_audio()

    # Clamp volume between 0 and 1.
    if volume < 0.0:
        volume = 0.0

    if volume > 1.0:
        volume = 1.0

    chosen_bone_sound = random.choice(bone_sounds)
    chosen_bone_sound.volume = volume
    chosen_bone_sound.play()