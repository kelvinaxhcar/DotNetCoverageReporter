import subprocess
import os
import glob
import shutil
import webbrowser
from tkinter import Tk, filedialog, Text, Scrollbar, Toplevel, END
import threading


def selecionar_pasta():
    root = Tk()
    root.withdraw()
    pasta_projeto = filedialog.askdirectory()
    root.destroy()
    return pasta_projeto


def exibir_logs():
    global text_widget
    log_window = Toplevel()
    log_window.title("Logs de Execução")

    scrollbar = Scrollbar(log_window)
    scrollbar.pack(side='right', fill='y')

    text_widget = Text(log_window, wrap='word', yscrollcommand=scrollbar.set)
    text_widget.pack(expand=True, fill='both')

    scrollbar.config(command=text_widget.yview)


def adicionar_log(mensagem):
    text_widget.insert(END, mensagem)
    text_widget.see(END)
    text_widget.update_idletasks()


def run_command(command, cwd=None):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=cwd)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            adicionar_log(output)
    rc = process.poll()
    return rc


def executar_processo():
    adicionar_log("Instalando o ReportGenerator...\n")
    run_command("dotnet tool install -g dotnet-reportgenerator-globaltool")

    adicionar_log("Executando dotnet build...\n")
    run_command("dotnet build", cwd=projeto_dir)

    adicionar_log("Executando dotnet test...\n")
    run_command('dotnet test --collect:"XPlat Code Coverage"', cwd=projeto_dir)

    adicionar_log("Procurando arquivo de cobertura mais recente...\n")
    test_results_dir = os.path.join(projeto_dir, 'TestResults')
    coverage_files = glob.glob(os.path.join(test_results_dir, '*/coverage.cobertura.xml'))
    if not coverage_files:
        raise FileNotFoundError("Arquivo de cobertura não encontrado.")
    report_input = max(coverage_files, key=os.path.getmtime)

    report_output = os.path.join(projeto_dir, 'Reports')

    adicionar_log("Gerando relatório HTML...\n")
    report_command = f'reportgenerator "-reports:{report_input}" "-targetdir:{report_output}" "-reporttypes:HTML"'
    run_command(report_command, cwd=projeto_dir)

    adicionar_log("Movendo pastas TestResults e Reports...\n")
    mover_diretorio(test_results_dir, raiz_dir)
    mover_diretorio(report_output, raiz_dir)

    adicionar_log("Desinstalando o ReportGenerator...\n")
    run_command("dotnet tool uninstall -g dotnet-reportgenerator-globaltool")

    index_file = os.path.join(raiz_dir, 'Reports', 'index.html')
    if os.path.exists(index_file):
        adicionar_log("Abrindo relatório no navegador...\n")
        webbrowser.open(f'file://{index_file}')
    else:
        adicionar_log(f'Arquivo {index_file} não encontrado.\n')


def mover_diretorio(origem, destino):
    if os.path.exists(origem):
        destino_final = os.path.join(destino, os.path.basename(origem))
        if os.path.exists(destino_final):
            shutil.rmtree(destino_final)
        shutil.move(origem, destino)
        adicionar_log(f'\nDiretório {origem} movido para {destino}\n')
    else:
        adicionar_log(f'\nDiretório {origem} não encontrado.\n')

projeto_dir = selecionar_pasta()

if not projeto_dir:
    print("Nenhuma pasta selecionada. Encerrando o programa.")
    exit()

raiz_dir = os.path.dirname(os.path.abspath(__file__))

root = Tk()
root.withdraw()
exibir_logs()

thread = threading.Thread(target=executar_processo)
thread.start()

root.mainloop()
