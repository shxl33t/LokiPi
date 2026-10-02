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

## 📝 Texto a ser digitado (`content.py`)

O `code.py` importa o texto de um arquivo chamado **`content.py`**:

```python
from content import CODE_CHUNKS
```

Crie esse arquivo na raiz do `CIRCUITPY`, com exatamente esse nome e uma lista chamada **`CODE_CHUNKS`**. **Insira o código da sua escolha dentro dos blocos** — é esse texto que o Pico vai digitar. Cada item da lista é um bloco. Entre um bloco e outro, o Pico faz uma pausa e às vezes mexe o mouse ou rola a tela.

O arquivo já vem com a lista vazia. **Cole o código da sua escolha entre os blocos `'''`**, assim:

```python
# content.py
CODE_CHUNKS = [
'''
# >>> Cole aqui o primeiro trecho que você quer que seja digitado <<<
''',

'''
# >>> Cole aqui o segundo trecho (adicione quantos blocos quiser) <<<
''',
]
```

Dicas:
- Use `'''` (três aspas simples) para escrever blocos com várias linhas.
- O texto não precisa ser um código que funcione. Ele só precisa parecer plausível na tela.
- Prefira caracteres ASCII simples. Acentos e `ç` não existem no layout US: o programa gera um erro e para.
- Desative o autocompletar e a indentação automática do editor de destino. Senão, a indentação vai se acumular.
- Se o arquivo não existir, o Pico mostra `ImportError: no module named 'content'` e não digita nada.

## ⚠️ Layout do teclado

O firmware usa o layout **US**. Se o Windows estiver em **ABNT2**, alguns símbolos (`"`, `;`, `/`, `[ ]`, `~`) sairão errados. Mude o layout do sistema para *Inglês (EUA)* durante o uso.

## 🛑 Como parar

- Aperte o botão no **GP15** para pausar ou retomar.
- Ou desconecte o Pico.

## 📜 Uso responsável

Este projeto serve para **testes autorizados** de ferramentas de monitoramento e para estudo de dispositivos HID. Não use para burlar políticas de monitoramento sem permissão de quem administra o ambiente.

## 🙏 Créditos

- [Adafruit CircuitPython HID](https://github.com/adafruit/Adafruit_CircuitPython_HID) (licença MIT)
