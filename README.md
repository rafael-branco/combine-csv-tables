# Guia de Uso do Script `processador_csv`

Este guia irá lhe ajudar a utilizar o script `processador_csv.exe`, disponível na seção de releases do GitHub.

## Requisitos

- Sistema Operacional: Windows
- Python 3.x instalado (opcional, caso utilize o `.exe` diretamente não será necessário)
- Pacotes necessários (caso execute o script `.py` diretamente):
  - pandas
  - glob
  - os
  - logging
  - unicodedata
  - tkinter

## Como Usar

1. **Baixar o `processador_csv.exe`**:Você pode baixar o arquivo executável (`processador_csv.exe`) diretamente na seção de releases do [GitHub](https://github.com/rafael-branco/combine-csv-tables/release). Isso elimina a necessidade de instalar dependências Python.
2. **Executar o Programa**:

   - Dê um duplo clique no arquivo `processador_csv.exe`.
   - Caso o Windows exiba a mensagem "O Windows protegeu seu PC" (SmartScreen), clique em **Mais informações** e depois em **Executar assim mesmo**.
3. **Seleção do Diretório**:

   - Uma janela irá abrir. Clique no botão **Selecionar Diretório e Processar**.
   - Selecione o diretório que contém os arquivos `.csv` que deseja processar.
4. **Acompanhamento**:

   - O programa exibirá a quantidade de arquivos encontrados e processará cada um deles.
   - Você verá uma barra de progresso que indica o andamento do processamento.
   - Ao final, um arquivo chamado `planilha_unificada.csv` será gerado no mesmo diretório de execução do programa.
5. **Logs de Execução**:

   - Durante a execução, um arquivo `info.log` será gerado, contendo detalhes sobre os arquivos processados e possíveis erros.

## Possíveis Problemas

- **Aviso de Proteção do Windows**:
  - Como mencionado anteriormente, o Windows pode exibir um aviso ao tentar executar o `.exe` baixado. Basta clicar em **Mais informações** e depois em **Executar assim mesmo**.
- **Erro de Codificação em Arquivos CSV**:
  - O script tenta lidar com diferentes encodings automaticamente. Caso algum arquivo CSV não seja lido corretamente, verifique os logs para mais informações.

## Contribuição

Se você encontrar algum problema ou tiver sugestões, sinta-se à vontade para abrir uma issue no [repositório GitHub](https://github.com/rafael-branco/combine-csv-tables/issues).
