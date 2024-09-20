import pandas as pd
import glob
import os
import logging
import unicodedata
import csv
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import sys
import queue
from tkinter import ttk


logging.basicConfig(
    filename="info.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def processar_diretorio(diretorio, status_var, progress_var, total_files):
    arquivos = glob.glob(os.path.join(diretorio, "**", "*.csv"), recursive=True)
    logging.info(f"Total de arquivos encontrados: {len(arquivos)}")
    status_var.set(f"Total de arquivos encontrados: {len(arquivos)}")
    progress_var["maximum"] = len(arquivos)

    lista_dfs = []

    colunas_padrao = [
        "prestador",
        "cep",
        "numero",
        "logradouro",
        "estado",
        "cidade",
        "bairro",
        "complemento",
    ]

    def padronizar_nome_coluna(col):
        col = "".join(
            c
            for c in unicodedata.normalize("NFD", col)
            if unicodedata.category(c) != "Mn"
        )
        col = col.strip().lower().replace(" ", "_")
        return col

    def detectar_delimitador(arquivo, enc="utf-8"):
        with open(arquivo, "r", encoding=enc, errors="ignore") as f:
            sample = f.read(1024)
            delimiters = [",", ";", "\t"]
            delimiter_counts = {d: sample.count(d) for d in delimiters}
            delimiter = max(delimiter_counts, key=delimiter_counts.get)
            return delimiter

    for idx, arquivo in enumerate(arquivos, start=1):
        nome_arquivo = os.path.basename(arquivo)
        status_var.set(f"Processando arquivo {idx} de {len(arquivos)}: {nome_arquivo}")
        logging.info(f"Iniciando processamento do arquivo: {nome_arquivo}")

        try:
            nome_upper = nome_arquivo.upper()
            if "_FIBRASIL" in nome_upper:
                tipo = "FIBRASIL"
                expected_cols = [
                    "comercializavel",
                    "uf",
                    "municipio",
                    "codigo_ibge",
                    "localidade",
                    "cnl",
                    "tipo",
                    "survey_endereco",
                    "bairro",
                    "logradouro_tipo",
                    "logradouro_titulo",
                    "logradouro_nome",
                    "logradouro_numero",
                    "cep",
                    "complemento_01",
                    "argumento_01",
                    "complemento_02",
                    "argumento_02",
                    "complemento_03",
                    "argumento_03",
                    "classificacao_residencial",
                    "classificacao_negocio",
                    "cto_atend_comercializaveis",
                    "armario",
                    "mapa_calor",
                    "fb",
                    "id_interno_fibrasil",
                ]
            elif "_ATC" in nome_upper:
                tipo = "ATC"
                expected_cols = [
                    "comercializavel",
                    "uf",
                    "municipio",
                    "codigo_ibge",
                    "localidade",
                    "cnl",
                    "tipo",
                    "survey_endereco",
                    "bairro",
                    "tipo_logradouro",
                    "titulo_logradouro",
                    "nome_do_logradouro",
                    "numero_fachada",
                    "cep",
                    "complemento_1",
                    "atr_complemento_1",
                    "complemento_2",
                    "atr_complemento_2",
                    "complemento_3",
                    "atr_complemento_3",
                    "tipo_mercado",
                    "tipo_de_local",
                    "cto_etiqueta",
                    "cto_pop",
                    "streetcode",
                ]
            elif "_VTAL" in nome_upper:
                tipo = "VTAL"
                expected_cols = [
                    "celula",
                    "estacao_abastecedora",
                    "uf",
                    "municipio",
                    "localidade",
                    "cod_localidade",
                    "localidade_abrev",
                    "logradouro",
                    "cod_logradouro",
                    "num_fachada",
                    "complemento",
                    "complemento2",
                    "complemento3",
                    "cep",
                    "bairro",
                    "cod_survey",
                    "quantidade_ums",
                    "cod_viabilidade",
                    "tipo_viabilidade",
                    "tipo_rede",
                    "ucs_residenciais",
                    "ucs_comerciais",
                    "nome_cdo",
                    "id_endereco",
                    "latitude",
                    "longitude",
                    "tipo_survey",
                    "rede_interna",
                    "ums_certificadas",
                    "rede_edif_cert",
                    "num_pisos",
                    "disp_comercial",
                    "estado_controle",
                    "data_estado_controle",
                    "id_celula",
                    "quantidade_hcs",
                    "projeto",
                ]
            elif "_IHS" in nome_upper:
                tipo = "IHS"
                expected_cols = [
                    "comercializavel",
                    "uf",
                    "municipio",
                    "codigo_ibge",
                    "localidade",
                    "cnl",
                    "tipo",
                    "survey_endereco",
                    "bairro",
                    "logradouro_tipo",
                    "logradouro_titulo",
                    "logradouro_nome",
                    "logradouro_numero",
                    "cep",
                    "complemento_01",
                    "argumento_01",
                    "complemento_02",
                    "argumento_02",
                    "complemento_03",
                    "argumento_03",
                    "classificacao_residencial",
                    "classificacao_negocio",
                    "cto_atend_comercializaveis",
                    "armario",
                    "mapa_calor",
                    "id_lote",
                ]
            else:
                logging.info(
                    f"Arquivo {nome_arquivo} não corresponde a nenhum tipo conhecido. Pulando."
                )
                continue

            delimiter = detectar_delimitador(arquivo)
            logging.info(
                f"Arquivo {nome_arquivo} - Delimitador detectado: '{delimiter}'"
            )

            codificacoes = ["utf-8", "latin1", "iso-8859-1"]
            df = None
            for encoding in codificacoes:
                try:
                    df = pd.read_csv(
                        arquivo,
                        delimiter=delimiter,
                        encoding=encoding,
                        engine="python",
                        on_bad_lines="skip",
                        quotechar='"',
                    )
                    logging.info(
                        f"Arquivo {nome_arquivo} lido com sucesso usando encoding '{encoding}'."
                    )
                    break
                except UnicodeDecodeError as e:
                    logging.warning(
                        f"Erro de codificação ao ler {nome_arquivo} com encoding '{encoding}': {e}"
                    )
                    df = None
            if df is None:
                logging.error(
                    f"Não foi possível ler o arquivo {nome_arquivo} com as codificações tentadas. Pulando."
                )
                continue

            df.columns = [padronizar_nome_coluna(col) for col in df.columns]
            expected_cols_padronizado = [
                padronizar_nome_coluna(col) for col in expected_cols
            ]

            logging.info(
                f"Arquivo {nome_arquivo} - Colunas presentes: {df.columns.tolist()}"
            )

            colunas_presentes = set(expected_cols_padronizado).intersection(
                set(df.columns)
            )
            colunas_faltando = set(expected_cols_padronizado) - set(df.columns)

            if len(colunas_presentes) == 0:
                logging.info(
                    f"Arquivo {nome_arquivo} não contém colunas esperadas. Pulando."
                )
                continue

            if colunas_faltando:
                logging.warning(
                    f"Arquivo {nome_arquivo} está faltando as colunas: {colunas_faltando}. Elas serão preenchidas com valores vazios."
                )
                for col in colunas_faltando:
                    df[col] = ""

            renomeacoes = {}
            if tipo == "FIBRASIL":
                renomeacoes = {
                    "cep": "CEP",
                    "logradouro_numero": "Número",
                    "logradouro_nome": "Logradouro",
                    "uf": "Estado",
                    "municipio": "Cidade",
                    "bairro": "Bairro",
                    "complemento_01": "Complemento1",
                    "complemento_02": "Complemento2",
                    "complemento_03": "Complemento3",
                }
            elif tipo == "ATC":
                renomeacoes = {
                    "cep": "CEP",
                    "numero_fachada": "Número",
                    "nome_do_logradouro": "Logradouro",
                    "uf": "Estado",
                    "municipio": "Cidade",
                    "bairro": "Bairro",
                    "complemento_1": "Complemento1",
                    "complemento_2": "Complemento2",
                    "complemento_3": "Complemento3",
                }
            elif tipo == "VTAL":
                renomeacoes = {
                    "cep": "CEP",
                    "num_fachada": "Número",
                    "logradouro": "Logradouro",
                    "uf": "Estado",
                    "municipio": "Cidade",
                    "bairro": "Bairro",
                    "complemento": "Complemento1",
                    "complemento2": "Complemento2",
                    "complemento3": "Complemento3",
                }
            elif tipo == "IHS":
                renomeacoes = {
                    "cep": "CEP",
                    "logradouro_numero": "Número",
                    "logradouro_nome": "Logradouro",
                    "uf": "Estado",
                    "municipio": "Cidade",
                    "bairro": "Bairro",
                    "complemento_01": "Complemento1",
                    "complemento_02": "Complemento2",
                    "complemento_03": "Complemento3",
                }

            df.rename(columns=renomeacoes, inplace=True)

            complemento_cols = [
                col for col in renomeacoes.values() if col.startswith("Complemento")
            ]
            if complemento_cols:
                df["Complemento"] = (
                    df[complemento_cols].fillna("").agg(" ".join, axis=1).str.strip()
                )
            else:
                df["Complemento"] = ""

            df["prestador"] = tipo

            df_padronizado = pd.DataFrame()
            df_padronizado["prestador"] = df["prestador"]
            df_padronizado["cep"] = df.get("CEP", "")
            df_padronizado["numero"] = df.get("Número", "")
            df_padronizado["logradouro"] = df.get("Logradouro", "")
            df_padronizado["estado"] = df.get("Estado", "")
            df_padronizado["cidade"] = df.get("Cidade", "")
            df_padronizado["bairro"] = df.get("Bairro", "")
            df_padronizado["complemento"] = df.get("Complemento", "")

            num_linhas = len(df_padronizado)
            logging.info(
                f"Arquivo {nome_arquivo} processado com sucesso. Linhas adicionadas: {num_linhas}"
            )

            lista_dfs.append(df_padronizado)

        except Exception as e:
            logging.error(f"Erro ao processar o arquivo {nome_arquivo}: {e}")
            continue

        progress_var.set(idx)

        status_var.set(f"Processando arquivo {idx} de {len(arquivos)}: {nome_arquivo}")

    if lista_dfs:
        df_final = pd.concat(lista_dfs, ignore_index=True)
        df_final.dropna(
            how="all",
            subset=[
                "cep",
                "numero",
                "logradouro",
                "estado",
                "cidade",
                "bairro",
                "complemento",
            ],
            inplace=True,
        )
        df_final.sort_values(by=["estado", "cidade"], inplace=True)
        df_final.to_csv("planilha_unificada.csv", index=False, encoding="utf-8-sig")
        logging.info(
            "Processamento concluído! O arquivo 'planilha_unificada.csv' foi criado."
        )
        status_var.set(
            "Processamento concluído! Arquivo 'planilha_unificada.csv' criado."
        )
        messagebox.showinfo(
            "Concluído", "Processamento concluído! Verifique os logs para detalhes."
        )
    else:
        logging.info(
            "Nenhum dado foi processado. Verifique os logs para mais informações."
        )
        status_var.set(
            "Nenhum dado foi processado. Verifique os logs para mais informações."
        )
        messagebox.showwarning(
            "Nenhum Dado",
            "Nenhum dado foi processado. Verifique os logs para mais informações.",
        )


def iniciar_processamento(diretorio, status_var, progress_var, total_files):
    thread = threading.Thread(
        target=processar_diretorio,
        args=(diretorio, status_var, progress_var, total_files),
    )
    thread.start()


def selecionar_diretorio(root, status_var, progress_var):
    diretorio = filedialog.askdirectory()
    if diretorio:
        status_var.set(f"Diretório selecionado: {diretorio}")
        iniciar_processamento(diretorio, status_var, progress_var, None)
    else:
        status_var.set("Nenhum diretório foi selecionado.")
        messagebox.showwarning(
            "Seleção de Diretório", "Nenhum diretório foi selecionado."
        )


def main():
    root = tk.Tk()
    root.title("Processador de CSV com GUI")
    root.geometry("600x200")

    status_var = tk.StringVar()
    status_var.set("Selecione um diretório para iniciar o processamento.")

    control_frame = tk.Frame(root)
    control_frame.pack(pady=10, padx=10, fill="x")

    selecionar_btn = tk.Button(
        control_frame,
        text="Selecionar Diretório e Processar",
        command=lambda: selecionar_diretorio(root, status_var, progress_var),
    )
    selecionar_btn.pack()

    progress_var = ttk.Progressbar(
        root, orient="horizontal", length=500, mode="determinate"
    )
    progress_var.pack(pady=20)

    status_label = tk.Label(
        root, textvariable=status_var, wraplength=500, justify="left"
    )
    status_label.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
