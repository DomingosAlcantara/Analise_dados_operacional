# Guia de Desenvolvimento - Dashboard

Este documento detalha o fluxo de trabalho, a arquitetura e as regras de negócio padronizadas para a implementação de novas telas e funcionalidades neste projeto Dash.

## 🔄 Fluxo de Implementação de Novas Telas

A criação de uma nova funcionalidade deve seguir a ordem abaixo para garantir que o front-end e o back-end estejam sempre em sincronia:

### Passo 1: Construção da Tela (View e CSS)
- **1. Componentes:** Crie a estrutura visual no arquivo Python correspondente (ex: `NomeDaTelaView.py`), definindo os IDs dos gráficos e tabelas (`html.Div`, `dash_table.DataTable`, `dcc.Graph`).
- **2. CSS:** Adicione as regras de estilização. 
  - *Atenção:* Evite usar `overflow-y: hidden` junto com `max-height` em tabelas e containers que recebem dados dinâmicos, para não ocultar informações. Prefira `overflow-y: auto`.

### Passo 2: Regras de Negócio e Dados (Model e Controller)
- **1. Consulta:** Crie os métodos na classe de motor/banco de dados para extrair as informações.
- **2. Processamento (Sempre no Python/Pandas):**
  - **Limpeza de Strings:** Remova tags HTML ou sujeiras direto no DataFrame (ex: `df['Coluna'].str.split("<br>").str[-1]`).
  - **Ordenação:** Ordene os dados com `.sort_values()` antes de enviar para o front-end. Deixe o JavaScript livre desse peso.
  - **Cores:** Atribua a paleta de cores no Python usando a função padrão do projeto (ex: `get_color_palette()`), criando uma coluna `"cor"` no DataFrame.
- **3. Payload:** Empacote os DataFrames em um dicionário JSON usando `.to_dict("records")` no Controller.

### Passo 3: Lógica de Front-end (JavaScript)
- **1. Classes Auxiliares:** Se houver lógicas repetitivas (formatações, builders), ajuste os arquivos base (ex: `ChartBuilder.js`, `TableFormatter.js`).
- **2. Presenter:** Crie a classe Presenter (ex: `03_NovaTelaPresenter.js`) para receber o JSON do Python, instanciar o ChartBuilder e retornar as figuras prontas.
- **3. Init:** Crie o arquivo de inicialização (ex: `04_nova_tela_init.js`) responsável por registrar a função no `window.dash_clientside` e fazer a ponte final.

---

## 🛑 Regras de Ouro e Boas Práticas

### 1. Tratamento de Dados (Backend > Frontend)
O Front-end (JavaScript) deve ser "burro" e rápido. Qualquer transformação de dados deve acontecer no Python (Pandas):
- Ordenação de listas e categorias.
- Definição de Cores.
- Limpeza, corte ou formatação pesada de strings.

### 2. Ordem de Carregamento do JavaScript
O Dash carrega os arquivos da pasta `assets/` em **ordem alfabética**. Respeite sempre a numeração no início do arquivo para evitar o erro `is not a constructor` ou `undefined`:
- `01_...` -> Classes e Formatadores globais (Auxiliares).
- `02_...` -> Construtores Visuais (ex: `ChartBuilder.js`).
- `03_...` -> Presenters (Classes que montam a tela específica).
- `04_...` -> Init (Ponto de entrada do `dash_clientside`).

### 3. Configurações de Gráficos (Plotly / ChartBuilder)
- **Gráficos Horizontais:** Use `textposition: 'inside'` para que os rótulos fiquem dentro das barras.
- **Textos Longos nos Eixos:** Ative a propriedade `automargin: true` nos eixos X e Y e garanta um respiro inicial adequado (ex: `margin: { l: 150 }`).

### 4. Ciclo de Atualização do Servidor (Troubleshooting)
Sempre pare (`Ctrl + C`) e reinicie o servidor Python quando:
- Criar ou renomear um arquivo físico na pasta `assets` (JS, CSS, Imagens).
- Alterar a estrutura visual (HTML/Componentes) das Views.
*Dica:* Após reiniciar o servidor, utilize sempre `Ctrl + F5` no navegador para limpar o cache do CSS e JavaScript.