import configparser


def resetConfig():
    cfg = configparser.ConfigParser()
    cfg['SFX'] = {
        'focusendsound': 'sounds/focusend.wav',
        'breakendsound': 'sounds/breakend.wav',
        'pomodoroendsound': 'sounds/pomodoroend.wav',
    }

    cfg['SETTINGS'] = {
        'focustime': 50,
        'breaktime': 10,
        'loops': 2,
        'volume': 0.5,
        'waitforinteraction': 'no',
    }

    cfg['KEYBINDS'] = {
        'quit': 'q',
        'skip': 's',
    }

    cfg['MISC'] = {
        'barlength': 30,
    }

    with open('config.ini', 'w') as cfgfile:
        cfg.write(cfgfile)


if __name__ == "__main__":
    resetConfig()
