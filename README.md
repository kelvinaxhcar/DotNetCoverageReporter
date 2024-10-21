# Automação de Relatórios de Cobertura de Testes com `dotnet`

Este projeto automatiza a execução de comandos do .NET para gerar relatórios de cobertura de testes utilizando o `ReportGenerator`. Ele oferece uma interface gráfica simples construída com `Tkinter` para exibição de logs e seleção de diretórios de projeto, além de executar os seguintes passos:

## Funcionalidades

1. **Instalação do `ReportGenerator`:** O projeto instala a ferramenta globalmente usando o comando `dotnet tool install`.
2. **Construção e Teste:** Executa o comando `dotnet build` seguido de `dotnet test`, coletando a cobertura de código.
3. **Geração de Relatórios HTML:** Identifica o arquivo de cobertura de testes mais recente e gera um relatório em HTML.
4. **Movimentação de Pastas:** Move as pastas de resultados de teste e relatórios para o diretório raiz do projeto.
5. **Desinstalação do `ReportGenerator`:** A ferramenta é desinstalada após o uso para manter o ambiente limpo.
6. **Exibição de Relatórios:** Abre automaticamente o relatório HTML no navegador ao final da execução.

## Como Usar

1. Clone o repositório e execute o script Python.
2. Selecione a pasta do projeto .NET.
3. O script vai exibir uma janela de logs com a execução dos comandos.
4. Ao final, o relatório será aberto no navegador.

## Dependências

- Python 3.x
- `dotnet` CLI
- `ReportGenerator` (instalado e desinstalado automaticamente pelo script)
- Bibliotecas Python: `subprocess`, `os`, `glob`, `shutil`, `webbrowser`, `tkinter`, `threading`

## Exemplo de Uso

```bash
python automacao_cobertura_teste.py
