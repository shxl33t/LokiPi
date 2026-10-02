# code.py
# Firmware CircuitPython para o Raspberry Pi Pico.
# Simula comportamento humano (digitacao, mouse, scroll, pausas de
# "pensar") para testar se a ferramenta de monitoramento (Blue TCM)
# consegue distinguir atividade real de atividade sintetica.
#
# Uso: copie este arquivo + content.py para a raiz do drive CIRCUITPY.

import time
import random

import board
import digitalio
import usb_hid

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse

from content import CODE_CHUNKS

kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)
mouse = Mouse(usb_hid.devices)

# Botao opcional em GP15 -> GND para pausar/retomar sem desconectar o Pico.
button = digitalio.DigitalInOut(board.GP15)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

# LED onboard para indicar estado (ligado = rodando, piscando = pausado).
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# ---------------------------------------------------------------------
# Parametros de "humanizacao" -- ajuste aqui para calibrar o teste
# ---------------------------------------------------------------------
TYPO_PROB = 0.03            # chance de digitar errado e corrigir com backspace
THINK_PAUSE_PROB = 0.05     # chance de uma micro-pausa "pensando" entre teclas
LINE_PAUSE_PROB = 0.25      # chance de pausa maior ao terminar uma linha
SCROLL_SESSION_PROB = 0.15  # chance de rolar a tela em vez de digitar um bloco
MOUSE_AFTER_CHUNK_PROB = 0.4

paused = False


def toggle_pause_if_pressed():
    global paused
    if not button.value:  # ativo em nivel baixo
        paused = not paused
        time.sleep(0.3)  # debounce
        while not button.value:
            time.sleep(0.05)


def wait_while_paused():
    while paused:
        led.value = not led.value
        toggle_pause_if_pressed()
        time.sleep(0.25)
    led.value = True


def jitter(base, spread):
    # CircuitPython nao tem random.gauss(); aproxima com ruido uniforme.
    delta = (random.random() * 2.0 - 1.0) * spread
    return max(0.0, base + delta)


def human_key_delay():
    if random.random() < THINK_PAUSE_PROB:
        time.sleep(jitter(1.1, 0.5))
    else:
        time.sleep(jitter(0.09, 0.045))


def move_mouse_naturally(steps=None):
    """Move o mouse em varios micro-passos, como uma mao real faria,
    em vez de um unico salto (o que fica obviamente robotico)."""
    steps = steps or random.randint(4, 12)
    for _ in range(steps):
        dx = random.randint(-6, 6)
        dy = random.randint(-4, 4)
        mouse.move(x=dx, y=dy)
        time.sleep(jitter(0.02, 0.01))


def scroll_naturally():
    # CircuitPython nao tem random.choice(); sorteia via randint.
    direction = 1 if random.randint(0, 1) else -1
    for _ in range(random.randint(2, 6)):
        mouse.move(wheel=direction)
        time.sleep(jitter(0.08, 0.03))


def idle_pause():
    """Simula 'pensando': para de digitar, mas de vez em quando
    mexe um pouco o mouse (como alguem descansando a mao)."""
    duration = jitter(2.2, 1.3)
    end = time.monotonic() + duration
    while time.monotonic() < end:
        toggle_pause_if_pressed()
        wait_while_paused()
        if random.random() < 0.3:
            move_mouse_naturally(steps=random.randint(1, 3))
        time.sleep(0.3)


_ALNUM_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def type_char_with_possible_typo(ch):
    # CircuitPython nao tem str.isalnum(); checa contra um set explicito.
    if ch in _ALNUM_CHARS and random.random() < TYPO_PROB:
        wrong = "abcdefghijklmnopqrstuvwxyz"[random.randint(0, 25)]
        layout.write(wrong)
        time.sleep(jitter(0.15, 0.05))
        kbd.send(Keycode.BACKSPACE)
        time.sleep(jitter(0.12, 0.05))
    layout.write(ch)


def type_text_humanized(text):
    for ch in text:
        wait_while_paused()
        toggle_pause_if_pressed()
        type_char_with_possible_typo(ch)
        human_key_delay()
        if ch == "\n" and random.random() < LINE_PAUSE_PROB:
            idle_pause()


def run():
    led.value = True
    # tempo para voce clicar na janela/editor de destino antes de comecar
    time.sleep(6)

    while True:
        for chunk in CODE_CHUNKS:
            wait_while_paused()
            toggle_pause_if_pressed()

            if random.random() < SCROLL_SESSION_PROB:
                scroll_naturally()
                idle_pause()

            type_text_humanized(chunk)
            idle_pause()

            if random.random() < MOUSE_AFTER_CHUNK_PROB:
                move_mouse_naturally()

        # ao "terminar o arquivo", pausa maior como se trocasse de tarefa
        time.sleep(jitter(20, 8))


run()
