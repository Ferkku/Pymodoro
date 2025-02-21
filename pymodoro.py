import keyboard
import configparser
import argparse
import time
import datetime
import pyglet

# For testing
SLEEP_TIME = 0.1

DEFAULT_PHASE_ENDED_SOUND = pyglet.media.StaticSource(
    pyglet.media.load("sounds/default.wav"))

# Config
config = configparser.ConfigParser()
config.read('config.ini')

# [SETTINGS]
FOCUS_TIME = config.getint('SETTINGS', 'focustime')
BREAK_TIME = config.getint('SETTINGS', 'breaktime')
LOOPS = config.getint('SETTINGS', 'loops')
VOLUME = config.getfloat('SETTINGS', 'volume')
REQUIRE_INTERACTION = config.getboolean('SETTINGS', 'waitforinteraction')

# [MISC]
TIMER_BAR_LENGTH = config.getint('MISC', 'barlength')

# [KEYBINDS]
QUIT_KEY = config.get('KEYBINDS', 'quit')
SKIP_KEY = config.get('KEYBINDS', 'skip')

# Load sounds, use default if not found
try:
    FOCUS_ENDED_SOUND = pyglet.media.StaticSource(
        pyglet.media.load(config.get('SFX', 'focusendsound')))
except FileNotFoundError:
    print("File: " + config.get('SFX', 'focusendsound') + " could not be found!")
    input("Press Enter to continue with default...")
    FOCUS_ENDED_SOUND = DEFAULT_PHASE_ENDED_SOUND

try:
    BREAK_ENDED_SOUND = pyglet.media.StaticSource(
        pyglet.media.load(config.get('SFX', 'breakendsound')))
except FileNotFoundError:
    print("File: " + config.get('SFX', 'breakendsound') + " could not be found!")
    input("Press Enter to continue with default...")
    BREAK_ENDED_SOUND = DEFAULT_PHASE_ENDED_SOUND

try:
    POMODORO_ENDED_SOUND = pyglet.media.StaticSource(
        pyglet.media.load(config.get('SFX', 'pomodoroendsound')))
except FileNotFoundError:
    print("File: " + config.get('SFX', 'pomodoroendsound') + " could not be found!")
    input("Press Enter to continue with default...")
    POMODORO_ENDED_SOUND = DEFAULT_PHASE_ENDED_SOUND

activeAudioPlayers = []
skipFlag = False
stopFlag = False


def on_key_event(event):
    global skipFlag
    global stopFlag
    if event.name == QUIT_KEY:
        print("Quitting...")
        stopFlag = True
    elif event.name == SKIP_KEY:
        print("Skipping...")
        skipFlag = True


keyboard.on_press(on_key_event)


def createTimerBar(emptyBars=0):
    timerBar = ""
    for i in range(TIMER_BAR_LENGTH - emptyBars):
        timerBar += "█"
    for i in range(emptyBars):
        timerBar += "░"
    return timerBar


def playSound(sound, volume):
    global activeAudioPlayers
    player = pyglet.media.Player()
    player.volume = volume
    player.queue(sound)
    player.play()

    activeAudioPlayers.append(player)

    def on_eos():
        if player in activeAudioPlayers:
            activeAudioPlayers.remove(player)

    player.push_handlers(on_eos=on_eos)


def createTimer(seconds, loop, maxLoops, reqAction, volume, timerText="Timer"):
    global skipFlag
    global stopFlag
    timerBar = createTimerBar()
    segmentLength = seconds / TIMER_BAR_LENGTH
    totalTimer = datetime.timedelta(seconds=seconds)

    segmentCounter = 0
    emptyBars = 0
    while seconds >= 0:
        if skipFlag or stopFlag:
            skipFlag = False
            break
        timer = datetime.timedelta(seconds=seconds)
        text = f"Loop: {loop} / {maxLoops}\n{timerBar}\n\n{timerText}: {timer}  /  {totalTimer}"

        if timerText == "Break" and loop == maxLoops and seconds <= 0:
            print(text)
        else:
            print(text, end="\033[H\033[J")

        time.sleep(SLEEP_TIME)
        seconds -= 1

        segmentCounter += 1
        if segmentCounter >= segmentLength:
            emptyBars += 1
            timerBar = createTimerBar(emptyBars)
            segmentCounter = 0

    if not stopFlag:
        if timerText == "Focus":
            playSound(FOCUS_ENDED_SOUND, volume)
        elif timerText == "Break":
            # Don't play the sound if last segment
            if loop != maxLoops:
                playSound(BREAK_ENDED_SOUND, volume)
        else:
            playSound(DEFAULT_PHASE_ENDED_SOUND, volume)

        if reqAction:
            input("Press Enter to continue...")


def pomodoro(ft, bt, requireInteraction, volume, loops=1):
    global stopFlag
    focusSecs = ft * 60
    breakSecs = bt * 60

    for loop in range(1, loops+1):
        createTimer(focusSecs, loop, loops,
                    requireInteraction, volume, "Focus")
        createTimer(breakSecs, loop, loops,
                    requireInteraction, volume, "Break")
        if stopFlag:
            break

    if not stopFlag:
        playSound(POMODORO_ENDED_SOUND, volume)
        print("END!!!")
        # Sleep until the sound is played
        time.sleep(POMODORO_ENDED_SOUND.duration)


def Main(args):
    focusTime = max(1, args.focustime)
    breakTime = max(1, args.breaktime)
    loops = args.loops
    reqInteraction = args.require_interaction
    volume = min(1, max(0, args.volume))

    pomodoro(focusTime, breakTime, reqInteraction, volume, loops)


if __name__ == "__main__":
    # Cli args
    parser = argparse.ArgumentParser()

    parser.add_argument('--focustime', '-ft', type=int, default=FOCUS_TIME,
                        help="Sets the time for focus segments (in minutes)")
    parser.add_argument('--breaktime', '-bt', type=int, default=BREAK_TIME,
                        help="Sets the time for break segments (in minutes)")
    parser.add_argument('--loops', '-l', type=int, default=LOOPS,
                        help="Sets the number of loops (loop = focus segment + break segment)")
    parser.add_argument('--require_interaction', '-ri',
                        type=bool, default=REQUIRE_INTERACTION, help="Sets whether or not the user is required to give input to continue to the next segment")
    parser.add_argument('--volume', '-v',
                        type=float, default=VOLUME, help="Sets the volume (From 0 to 1)")

    args = parser.parse_args()

    Main(args)
