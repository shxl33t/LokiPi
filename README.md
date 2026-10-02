# ᚠ Loki

> *Na mitologia nórdica, **Loki** é o deus trapaceiro que muda de forma.*

**LokiPi** é um firmware em CircuitPython para o **Raspberry Pi Pico** que se apresenta ao computador como teclado e mouse USB e imita uma pessoa trabalhando: digita código com ritmo irregular, erra e corrige, faz pausas para "pensar", rola a tela e mexe o mouse.

O objetivo é **testar se ferramentas de monitoramento de atividade conseguem distinguir comportamento humano real de atividade sintética.**

---

## ✨ Funcionalidades

- ⌨️ **Digitação humanizada**: intervalo aleatório entre teclas e pausas ocasionais
- 🔙 **Erros de digitação**: digita uma letra errada e corrige com Backspace
- 🖱️ **Mouse natural**: movimentos em vários micro-passos, nunca em saltos
- 📜 **Scroll**: rola a tela de vez em quando
- 💭 **Pausas de "pensamento"**: para de digitar e mexe levemente o mouse
- ⏯️ **Botão de pausa** no GP15
- 💡 **LED de status**: aceso = rodando · piscando = pausado

## 🧰 Hardware

| Item | Observação |
|---|---|
| Raspberry Pi Pico (RP2040) | Testado com CircuitPython 10.0.0 |
| Cabo micro-USB com dados | Cabos só de carga não funcionam |
| Botão (opcional) | Entre o **GP15** e o **GND** |

## 🚀 Instalação

1. Instale o [CircuitPython](https://circuitpython.org/board/raspberry_pi_pico/) no Pico.
2. Baixe o [Adafruit CircuitPython Bundle](https://circuitpython.org/libraries) e copie a pasta `adafruit_hid` para `CIRCUITPY/lib/`.
3. Copie `code.py` e `content.py` para a raiz do drive `CIRCUITPY`.
4. O Pico reinicia sozinho. Você tem **6 segundos** para clicar na janela do editor onde o texto será digitado.

```
CIRCUITPY/
├── code.py          # programa principal
├── content.py       # texto que será digitado
└── lib/
    └── adafruit_hid/
```

## ⚙️ Configuração

Os parâmetros ficam no topo do `code.py`:

| Parâmetro | Padrão | Efeito |
|---|---|---|
| `TYPO_PROB` | `0.03` | Chance de errar uma tecla e corrigir |
| `THINK_PAUSE_PROB` | `0.05` | Chance de micro-pausa entre teclas |
| `LINE_PAUSE_PROB` | `0.25` | Chance de pausa longa ao fim da linha |
| `SCROLL_SESSION_PROB` | `0.15` | Chance de rolar a tela antes de um bloco |
| `MOUSE_AFTER_CHUNK_PROB` | `0.4` | Chance de mexer o mouse após um bloco |

Para mudar o que é digitado, edite a lista `CODE_CHUNKS` em `content.py`.

## ⚠️ Layout do teclado

O firmware usa o layout **US**. Se o Windows estiver em **ABNT2**, alguns símbolos (`"`, `;`, `/`, `[ ]`, `~`) sairão errados. Mude o layout do sistema para *Inglês (EUA)* durante o uso.

## 🛑 Como parar

- Aperte o botão no **GP15** para pausar ou retomar.
- Ou desconecte o Pico.

## 📜 Uso responsável

Este projeto serve para **testes autorizados** de ferramentas de monitoramento e para estudo de dispositivos HID. Não use para burlar políticas de monitoramento sem permissão de quem administra o ambiente.

## 🙏 Créditos

- [Adafruit CircuitPython HID](https://github.com/adafruit/Adafruit_CircuitPython_HID) (licença MIT)
