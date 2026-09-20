# Twitch Auto Reward Clicker

Ferramenta de automação para Windows que desenvolvi em Python. Seleciono uma área do ecrã, acompanho a proporção de píxeis verdes e, quando o limiar configurado é atingido, a aplicação pode executar um clique nessa área.

O funcionamento baseia-se na imagem do ecrã. Não precisa de acesso à conta Twitch, de uma extensão de navegador ou de uma chave de API.

## Funcionalidades

- Seleção visual de uma ou várias áreas.
- Deteção de píxeis verdes com sensibilidade ajustável.
- Interface de monitorização com informação visual.
- Integração com a área de notificação do Windows.
- Script para gerar um executável local.

## Requisitos

Windows com Python 3 e as dependências `pyautogui`, `pillow`, `numpy` e `pystray`. Para gerar o executável, instala também `pyinstaller`.

```powershell
python -m pip install pyautogui pillow numpy pystray
python AutoGreenClicker.py
```

## Compilar no Windows

```powershell
python -m pip install pyinstaller
.\BUILD.bat
```

O executável gerado pelo script é guardado na pasta `dist`, se a compilação terminar sem erros.

## Como utilizo

1. Abro a aplicação e adiciono uma área de monitorização.
2. Seleciono no ecrã a região que contém o botão pretendido.
3. Ajusto a percentagem mínima de píxeis verdes.
4. Inicio a monitorização e confirmo os resultados no painel.

## Limites

A deteção depende das cores apresentadas no ecrã, da escala e do tema da aplicação monitorizada. Não garante a identificação de todos os botões e pode reagir a outras zonas verdes. Testa primeiro numa área sem consequências importantes. Verifica também as regras do serviço onde pretendes utilizar automação.
