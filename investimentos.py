import requests
import streamlit as st
import pandas as pd
import plotly_express as px

# ================== API =====================
url = 'https://api.hgbrasil.com/finance/taxes'

params = {
    'key': '08a2a276'
}
response = requests.get(url, params=params)
data = response.json()
taxa_selic = data['results'][0]['selic_daily']
# ================================ Interface ==============================
st.title('Calculadora de Juros Compostos')

st.header('SIMULADOR DE JUROS COMPOSTOS (Selic)')   

st.write('**Taxa Selic Hoje:** ', taxa_selic, '%') # Taxa selic anual

vi = st.number_input('Valor Inicial (R$)')         # Valor Inicial do Aporte
t = st.number_input('Périodo em meses', value=0)   # meses
im = st.number_input('Investimento Mensal (R$)')   # Aporte mensal

i = taxa_selic / 100 / 12             # Taxa selic mensal em %

# ==================================== Calculando ================================
if st.button('Calcular'):
    if vi == 0 or im == 0 or t == 0:
        st.write('*Preencha os todos os campos')
    else:
        m = vi * (1 + i) ** t +im * ((1 + i) ** t - 1) / i  # Montante final
        vti = im*t + vi                                     # Total Investido
        tj = m - vti                                        # Total Juros
        nm = [f'{m:.2f}', f'{vti:.2f}', f'{tj:.2f}']        # Os valores formatados
        st.header('RESULTADO: ')
        st.write('**Valor Total Final:** R$', nm[0])
        st.write('**Valor Total Investido:** R$', nm[1])
        st.write('**Total juros:** R$', nm[2])

        table = {
            'Meses':[],
            'Juros':[0],
            'Total Investido':[],
            'Total Juros':[],
            'Acumulado':[]
        }
        CTJ = 0 # Contador do Total de Juros
        meses = 0  
        for c in range(0, t): 
            table['Total Investido'].append(im*c + vi)
            if c == 0:
                juros = 0
            else:
                table['Juros'].append(table['Acumulado'][c - 1] * i)
            CTJ += table['Juros'][c]
            table['Total Juros'].append(CTJ)
            table['Acumulado'].append(im*c + vi + table['Total Juros'][c])
            table['Meses'].append(meses)
            meses += 1
        df = pd.DataFrame(table)
        
        df_invest = df.style.format({'Juros': 'R${:,.2f}', 'Total Juros': 'R${:,.2f}', 'Total Investido': 'R${:,.2f}', 'Acumulado': 'R${:,.2f}', })
        
        st.header('Gráfico')
        fig = px.line(df, x='Meses', y=['Acumulado', 'Total Investido'])
        st.plotly_chart(fig)

        st.header('Tabela')
        df_invest
