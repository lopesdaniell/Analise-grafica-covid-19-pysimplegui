# Link do banco de dados: https://data.brasil.io/dataset/covid19/caso.csv.gz
# Developer: Daniel Lopes

#  Importando as bibliotecas
import PySimpleGUI as sg
import pandas as pd
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Importando o dataset e fazendo ajustes
caso = pd.read_csv(r'caso.csv')
caso = caso.drop(['place_type', 'confirmed', 'order_for_place', 'is_last', 'estimated_population_2019',
                 'city_ibge_code', 'confirmed_per_100k_inhabitants', 'death_rate'], axis=1)
caso['city'] = caso['city'].str.title()

# Função que atualiza a gráfico
def update_figure():
    ax.clear()
    ax.tick_params(axis=u'both', which=u'both',length=0)
    ax.set_xticklabels([])
    ax.invert_xaxis()
    ax.set_ylabel('Mortes por COVID-19')

# Função que plota o gráfico
def plot_figure():
    ax.plot(x, y, 'b-')
    ax.set_xlabel(pri_dia + '                                                                               ' + ult_dia)
    fig.suptitle(cidade + ', ' + estado, fontsize=20)
    figure_canvas_agg.draw()

# Layout da interface gráfica
sg.theme('DarkBlue')

layout = [
    [sg.Text('Cidade:')],
    [sg.Input(key='cidade')],
    [sg.Text('UF:')],
    [sg.Combo(['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA',
              'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'], key='estado')],
    [sg.Button('Consultar')],
    [sg.Text('', key='mensagem')],
    [sg.Canvas(key='canvas')],
]

window = sg.Window('Análise Gráfica COVID-19', layout, finalize=True, font='Helvetica 14')

# Configurações do gráfico
fig = matplotlib.figure.Figure(figsize=(6, 5))
ax = fig.add_subplot(111)

figure_canvas_agg = FigureCanvasTkAgg(fig, window['canvas'].TKCanvas)
figure_canvas_agg.get_tk_widget().pack()

# Loop da interface gráfica
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    if event == 'Consultar':
        update_figure()
        cidade = values['cidade']
        cidade = cidade.title()  # Deixando a primeira letra da string maiúscula
        estado = values['estado']
        estado = estado.upper()  # Deixando toda a string maiúscula
        df = caso[(caso['city'] == cidade) & (caso['state'] == estado)] # Criando dataframe com amostras da cidade escolhida
        hab = df['estimated_population'].sum()
        if hab != 0:  # Verificando se a cidade existe
            x = df['date']
            y = df['deaths']
            ult_dia = df.iloc[0]['date']
            pri_dia = df.iloc[-1]['date']
            window['mensagem'].update('Cidade encontrada!')
            plot_figure()
        else:
            window['mensagem'].update('Cidade não encontrada!')
            
window.close()
