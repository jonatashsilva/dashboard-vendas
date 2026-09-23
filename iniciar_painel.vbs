Set WshShell = CreateObject("WScript.Shell")

' Inicia o Flask ocultando a janela do CMD
WshShell.Run "cmd /c cd /d ""C:\PainelVendas"" && python app.py", 0, False

' Aguarda 10 segundos para o Flask iniciar
WScript.Sleep 10000