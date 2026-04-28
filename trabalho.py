import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency

# Configurar página com tema e cores
st.set_page_config(
    page_title="Análise de Dados",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para melhorar aparência
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #f8f9fa 0%, #e8f0f7 100%);
    }
    .stTabs [data-baseweb="tab-list"] button {
        background-color: #e8f0f7;
        color: #1f366d;
        font-weight: bold;
        border-radius: 10px;
        margin: 2px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0066cc !important;
        color: white !important;
        border-radius: 10px;
    }
    h1 {
        color: #0066cc;
        font-size: 2em;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    h2 {
        color: #004b94;
        font-size: 1.8em;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .stDataFrame {
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .stSidebar {
        background-color: #f0f4f8;
        border-radius: 10px;
    }
    .stSelectbox {
        background-color: white;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1,3])


#st.image("imagem.png", width=150)
#st.title("Fatec Sebrae - Ciências de Dados para negócios")
#st.write("🔍 Relação da avaliação subjetiva de saúde, capacidade funcional e cognição em idosos longevos")

# Configurar matplotlib com estilo melhorado
plt.style.use('default')
sns.set_palette("husl")
df = pd.read_excel('Banco de dados.xlsx')
df.columns = df.columns.str.strip()
# Menu
menu = st.sidebar.selectbox("Escolha a análise:", ["⭐Apresentação","📘 Metodologia","📈 Tabela de Frequência", "🔗 Correlação", "📊 Teste Qui-Quadrado", "📊 Gráfico de Barras", "🥧 Gráfico de Pizza"])

if menu == "⭐Apresentação":
    col1, col2 = st.columns([1,5])
    with col1:
        st.image("imagem.png", width=200)
    #col1, col2, col3 = st.columns([1,2,1])
    #with col2:
        #st.image("imagem.png", width=180)
    st.title("📊 Análise de Dados com Streamlit")
    st.header("Relação da autoavaliação de saúde, capacidade funcional e cognição em idosos longevos")
    st.write("Curso: Ciências de Dados para negócios - Fatec Sebrae - 2° semestre")
    st.write("Docente: Rômulo Francisco de Souza Maia")
    st.write("Discente: Amanda de Jesus dos Santos")


if menu == "📘 Metodologia":
    #col1, col2 = st.columns([1,5])
    #with col1:
        #st.image("imagem.png", width=150)
    #st.title("📊 Análise de Dados com Streamlit")
    #st.write("🔍 Relação da avaliação subjetiva de saúde, capacidade funcional e cognição em idosos longevos")
    st.header("Metodologia do Estudo")
    st.subheader("Objetivo")
    st.write("O objetivo deste estudo foi relacionar a capacidade funcional e cognição do indivíduo octogenário com a autoavaliação de saúde")
    st.subheader("Tipo de estudo")
    st.write("Estudo do tipo transversal composto por uma amostra de conveniência")
    st.subheader("População")
    st.write("103 idosos com 80 anos ou mais de ambos os sexos")
    st.subheader("Variáveis analisadas")
    st.write("Sexo; Autoavaliação da saúde; Classificação SPPB; Sarcopenia; ABVD e AIVD; GDS (depressão); MAN (estado nutricional); Escolaridade; MEEM (cognição)")
    st.subheader("Análises estatísticas")
    st.markdown("""
    - Estatística descritiva - frequência absoluta e acumulada  
    - Teste Qui-Quadrado - associação entre variáveis categóricas  
    - Correlação entre variáveis  
    - Visualizações gráficas (barras e pizza)
    - Foi adotado α = 0,05 para testes de significância estatística          
    """) 
    ### 🧪 Nível de significância
    #"Foi adotado α = 0,05."

if menu == "📈 Tabela de Frequência":
    st.header("📈 Tabela de Frequência")
    # Variáveis específicas solicitadas (ajustadas aos nomes no dataset)
    desired_vars = ['Sexo', 'Autoavaliação da saúde', 'Classificação SPPB', 'Sarcopenia', 'Classificação ABVD', 'Classificação GDS', 'Classificação MAN', 'Escolaridade', 'Classificação AIVD', 'MEEM', 'Classificação CP']
    available_vars = [col for col in desired_vars if col in df.columns]
    
    if len(available_vars) > 0:
        st.subheader("Variáveis e suas Categorias")
        summary = []
        for col in available_vars:
            categories = df[col].dropna().unique()
            summary.append({'Variável': col, 'Categorias': ', '.join(map(str, categories))})
        summary_df = pd.DataFrame(summary)
        st.dataframe(summary_df)
        
        tab1, tab2 = st.tabs(["Frequência Geral", "Frequência por Sexo"])
        
        with tab1:
            selected_cols = st.multiselect("Escolha as variáveis para tabela de frequência geral:", available_vars, default=available_vars, key="geral")
            if selected_cols:
                all_freq = []
                stats_summary = []
                for col in selected_cols:
                    freq_table = df[col].value_counts().reset_index()
                    freq_table.columns = ['Categoria', 'Frequência Absoluta']
                    freq_table['Frequência Relativa (%)'] = (freq_table['Frequência Absoluta'] / freq_table['Frequência Absoluta'].sum() * 100).round(2)
                    freq_table['Frequência Acumulada'] = freq_table['Frequência Absoluta'].cumsum()
                    freq_table['Frequência Acumulada (%)'] = (freq_table['Frequência Acumulada'] / freq_table['Frequência Absoluta'].sum() * 100).round(2)
                    freq_table['Variável'] = col
                    all_freq.append(freq_table)
                    # Estatísticas
                    try:
                        col_data = pd.to_numeric(df[col], errors='coerce').dropna()
                        if len(col_data) > 0:
                            media = col_data.mean()
                            desvio = col_data.std()
                            stats_summary.append({'Variável': col, 'Média': round(media, 2), 'Desvio Padrão': round(desvio, 2)})
                    except:
                        pass
                combined_freq = pd.concat(all_freq, ignore_index=True)
                combined_freq = combined_freq[['Variável', 'Categoria', 'Frequência Absoluta', 'Frequência Relativa (%)', 'Frequência Acumulada', 'Frequência Acumulada (%)']]
                combined_freq = combined_freq.sort_values(['Variável', 'Frequência Absoluta'], ascending=[True, False])
                st.dataframe(combined_freq)
                # Exibir estatísticas
                if stats_summary:
                    st.subheader("Média e Desvio Padrão das Variáveis Numéricas")
                    st.dataframe(pd.DataFrame(stats_summary))
            else:
                st.write("Selecione pelo menos uma variável.")
        
        with tab2:
            if 'Sexo' in df.columns:
                selected_cols_sexo = st.multiselect("Escolha as variáveis para tabela de frequência por sexo:", [col for col in available_vars if col != 'Sexo'], default=[col for col in available_vars if col != 'Sexo'], key="sexo")
                if selected_cols_sexo:
                    all_freq_sexo = []
                    stats_sexo = []
                    for col in selected_cols_sexo:
                        freq_by_sexo = df.groupby('Sexo')[col].value_counts().unstack().fillna(0).stack().reset_index(name='Frequência Absoluta')
                        freq_by_sexo.columns = ['Sexo', 'Categoria', 'Frequência Absoluta']
                        total_by_sexo = df['Sexo'].value_counts()
                        freq_by_sexo['Frequência Relativa (%)'] = freq_by_sexo.apply(lambda row: (row['Frequência Absoluta'] / total_by_sexo[row['Sexo']] * 100).round(2), axis=1)
                        freq_by_sexo['Variável'] = col
                        all_freq_sexo.append(freq_by_sexo)
                        # Estatísticas por sexo
                        try:
                            for sexo in df['Sexo'].dropna().unique():
                                col_data = pd.to_numeric(df[df['Sexo'] == sexo][col], errors='coerce').dropna()
                                if len(col_data) > 0:
                                    media = col_data.mean()
                                    desvio = col_data.std()
                                    stats_sexo.append({'Variável': col, 'Sexo': sexo, 'Média': round(media, 2), 'Desvio Padrão': round(desvio, 2)})
                        except:
                            pass
                    combined_freq_sexo = pd.concat(all_freq_sexo, ignore_index=True)
                    combined_freq_sexo = combined_freq_sexo[['Variável', 'Sexo', 'Categoria', 'Frequência Absoluta', 'Frequência Relativa (%)']]
                    combined_freq_sexo = combined_freq_sexo.sort_values(['Variável', 'Sexo', 'Frequência Absoluta'], ascending=[True, True, False])
                    st.dataframe(combined_freq_sexo)
                    # Exibir estatísticas por sexo
                    if stats_sexo:
                        st.subheader("Média e Desvio Padrão por Sexo (variáveis numéricas)")
                        st.dataframe(pd.DataFrame(stats_sexo))
                else:
                    st.write("Selecione pelo menos uma variável.")
            else:
                st.write("Coluna 'SEXO' não encontrada para estratificação.")
    else:
        st.write("Nenhuma das variáveis desejadas foi encontrada no dataset.")


elif menu == "🔗 Correlação":

    st.header("🔗 Análise de Correlação")
    desired_vars = ['Sexo', 'Autoavaliação da saúde', 'Classificação SPPB', 'Sarcopenia', 'Classificação ABVD', 'Classificação GDS', 'Classificação MAN', 'Escolaridade', 'Classificação AIVD', 'MEEM', 'Classificação CP']
    available_vars = [col for col in desired_vars if col in df.columns]
    
    if len(available_vars) >= 2:
        selected_vars = st.multiselect("Escolha as variáveis para análise de correlação:", available_vars, default=available_vars)
        if len(selected_vars) >= 2:
            try:
                # Preparar dados para correlação
                df_corr = df[selected_vars].copy()
                
                # Codificar variáveis categóricas e numéricas
                for col in df_corr.columns:
                    if df_corr[col].dtype in ['object', 'string']:
                        # Converter para string e depois para numérico
                        df_corr[col] = pd.factorize(df_corr[col].astype(str))[0]
                    else:
                        # Se for numérico, tentar converter
                        try:
                            df_corr[col] = pd.to_numeric(df_corr[col], errors='coerce')
                        except:
                            df_corr[col] = pd.factorize(df_corr[col].astype(str))[0]
                
                # Remover linhas com valores faltantes
                df_corr = df_corr.dropna()
                
                if len(df_corr) > 1:
                    # Calcular correlação
                    corr = df_corr.corr()
                    
                    st.subheader("Matriz de Correlação")
                    st.dataframe(corr.round(3))
                    
                    st.subheader("Heatmap de Correlação")
                    fig, ax = plt.subplots(figsize=(12, 10))
                    sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1, ax=ax, fmt='.2f')
                    ax.set_title('Heatmap de Correlação - Todas as Variáveis')
                    st.pyplot(fig)
                else:
                    st.write("Dados insuficientes após remover valores faltantes.")
            except Exception as e:
                st.error(f"Erro na análise de correlação: {str(e)}")
        else:
            st.write("Selecione pelo menos 2 variáveis.")
    else:
        st.write("Não há variáveis suficientes para análise de correlação.")

elif menu == "📊 Teste Qui-Quadrado":
    st.header("🔬 Teste Qui-Quadrado (Chi-Square)")
    categorical_cols = df.select_dtypes(include=['object', 'category', 'string']).columns
    if len(categorical_cols) >= 2:
        col1, col2 = st.columns(2)
        with col1:
            var1 = st.selectbox("Escolha a primeira variável categórica:", categorical_cols)
        with col2:
            var2 = st.selectbox("Escolha a segunda variável categórica:", [col for col in categorical_cols if col != var1])
        
        if st.button("🔍 Executar Teste Qui-Quadrado"):
            try:
                # Criar tabela de contingência
                contingency_table = pd.crosstab(df[var1], df[var2])
                
                st.subheader("📊 Tabela de Contingência")
                st.dataframe(contingency_table)
                
                # Executar teste
                chi2, p_value, dof, expected = chi2_contingency(contingency_table)
                
                # Exibir resultados
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("χ² (Chi-Square)", f"{chi2:.4f}")
                with col2:
                    st.metric("P-value", f"{p_value:.6f}")
                with col3:
                    st.metric("Graus de Liberdade", dof)
                
                # Interpretação
                st.subheader("📋 Interpretação")
                alpha = 0.05
                if p_value < alpha:
                    st.success(f"✅ **P-value ({p_value:.6f}) < {alpha}**: Há associação significativa entre as variáveis (rejeitamos H0)")
                else:
                    st.info(f"❌ **P-value ({p_value:.6f}) ≥ {alpha}**: Não há associação significativa entre as variáveis (não rejeitamos H0)")
                
                # Frequências esperadas
                st.subheader("📈 Frequências Esperadas")
                expected_df = pd.DataFrame(expected, index=contingency_table.index, columns=contingency_table.columns)
                st.dataframe(expected_df.round(2))
                
                # Visualização das frequências
                st.subheader("📊 Visualização da Tabela de Contingência")
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.heatmap(contingency_table, annot=True, fmt='d', cmap='Blues', ax=ax, cbar_kws={'label': 'Frequência'})
                ax.set_title(f'Tabela de Contingência: {var1} vs {var2}', fontsize=14, fontweight='bold')
                st.pyplot(fig)
                
            except Exception as e:
                st.error(f"Erro na análise: {str(e)}")
    else:
        st.write("São necessárias pelo menos 2 variáveis categóricas para o teste qui-quadrado.")

elif menu == "📊 Gráfico de Barras":

    st.header("📊 Gráfico de Barras")
    categorical_cols = df.select_dtypes(include=['object', 'category', 'string']).columns
    if len(categorical_cols) > 0:
        selected_col = st.selectbox("Escolha uma coluna categórica para o gráfico de barras:", categorical_cols)
        counts = df[selected_col].value_counts()
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = plt.cm.Set3(range(len(counts)))
        counts.plot(kind='bar', ax=ax, color=colors, edgecolor='black', linewidth=1.2)
        ax.set_title(f'Gráfico de Barras de {selected_col}', fontsize=14, fontweight='bold')
        ax.set_xlabel(selected_col, fontsize=12)
        ax.set_ylabel('Frequência', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        ax.grid(axis='y', alpha=0.3)
        st.pyplot(fig)
    else:
        st.write("Não há colunas categóricas no dataset.")

elif menu == "🥧 Gráfico de Pizza":
    st.header("🥧 Gráfico de Pizza")
    categorical_cols = df.select_dtypes(include=['object', 'category', 'string']).columns
    if len(categorical_cols) > 0:
        selected_col = st.selectbox("Escolha uma coluna categórica para o gráfico:", categorical_cols)
        counts = df[selected_col].value_counts()
        fig, ax = plt.subplots(figsize=(10, 8))
        colors = plt.cm.Set3(range(len(counts)))
        ax.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=90, colors=colors, textprops={'fontsize': 10, 'weight': 'bold'})
        ax.set_title(f'Gráfico de Pizza de {selected_col}', fontsize=14, fontweight='bold')
        ax.axis('equal')
        st.pyplot(fig)
    else:
        st.write("Não há colunas categóricas no dataset.")
        