# 🟢 Twitch Auto Reward Clicker

Ferramenta de automação de ecrã que deteta quando um botão fica verde e clica automaticamente — feita especificamente para resgatar Channel Points e recompensas na Twitch sem teres de estar presente.

---

## 💡 Como funciona

A maioria dos rewards na Twitch (e noutras plataformas) seguem o mesmo padrão visual: o botão está **cinzento** enquanto não está disponível, e fica **verde** quando podes clicar.

Este programa monitoriza em tempo real as áreas do ecrã que tu selecionas. Assim que deteta a transição de cinzento para verde, espera 1 segundo (para parecer humano) e clica automaticamente.

Podes ir dormir — ele não perde nenhum reward.

---

## ✨ Funcionalidades

- 🖱️ Seleção visual de áreas no ecrã com overlay interativo
- 🎨 Deteção de cor em tempo real via análise de píxeis (RGB)
- ⏱️ Delay de 1s após deteção + movimento suave do rato (mais natural)
- 📋 Múltiplas áreas em simultâneo, cada uma com o seu nome
- 🔁 Apenas clica na transição cinzento → verde (não repete)
- 🎚️ Slider de sensibilidade ajustável (% de píxeis verdes para disparar)
- 📊 Debug em tempo real com valores RGB e percentagem detetada
- 🔔 Ícone na system tray — X minimiza, não fecha (como o Discord)
- ✅ Compilável como `.exe` — sem consola, sem Python visível

---

## 🚀 Instalar e usar

### Opção A — Correr direto com Python

```bash
pip install pyautogui pillow numpy pystray
python AutoGreenClicker.py
```

### Opção B — Compilar como .exe (recomendado)

1. Coloca `AutoGreenClicker.py`, `BUILD.bat` e `icon.ico` na mesma pasta
2. Corre o `BUILD.bat`
3. O `.exe` aparece em `dist\AutoGreenClicker.exe`
4. Clica com botão direito → **Afixar na barra de tarefas**

---

## 🎮 Caso de uso principal — Twitch Channel Points

1. Abre a Twitch no browser
2. Abre a app e clica em **+ Adicionar área**
3. Seleciona a zona do botão de reward
4. Dá-lhe um nome (ex: `"Pontos Twitch"`)
5. Clica em **Iniciar monitorização**
6. Fecha a janela (fica na tray) e vai fazer a tua vida

Quando o reward ficar disponível, a app deteta o verde, aguarda 1 segundo e clica sozinha.

---

## ⚙️ Sensibilidade

O slider controla a percentagem mínima de píxeis verdes dentro da área para disparar o clique.

| Situação | Valor recomendado |
|---|---|
| Botão inteiro fica verde | 30 – 50% |
| Só parte do botão fica verde | 10 – 20% |
| Pequeno indicador / ícone | 3 – 8% |

O debug mostra o valor real em tempo real — coloca o slider uns 10 pontos abaixo do que aparece quando o botão está verde.

---

## 🛡️ Aviso

Esta ferramenta interage com o ecrã localmente, sem aceder a qualquer API, token ou conta. Não injeta nada, não faz bypass de nada. É equivalente a um utilizador a clicar manualmente com o rato.

Usa com responsabilidade.

---

## 🧰 Tecnologias

- Python 3
- Tkinter (interface gráfica)
- Pillow + NumPy (captura e análise de cor)
- PyAutoGUI (controlo do rato)
- Pystray (system tray)
- PyInstaller (compilação para .exe)
