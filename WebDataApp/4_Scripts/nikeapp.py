from flask import Flask, jsonify, render_template

import pandas as pd

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')
    
@app.route('/Tabela/')
def tabela():
    dados = pd.read_csv('../1_Base_tratada/nikefinal.csv', sep= ";")
    tabela_html = dados.to_html(classes='table table-striped')
    return render_template('tabela.html', tabela=tabela_html)

@app.route('/Nome/')
#tipos dos produtos
def Nome():
    dados = pd.read_csv('../1_Base_tratada/nikefinal.csv', sep= ";")
    Nomes = dados['Nome'].unique()
    modaNomes = dados['Nome'].mode()[0]
    resposta = {'Nomes:':Nomes.tolist(),'Nome mais presente:':modaNomes}
    return jsonify(resposta)

@app.route('/Categoria/')
#tipos dos produtos
def Categoria():
    dados = pd.read_csv('../1_Base_tratada/nikefinal.csv', sep= ";")
    tipo = dados['Tipo'].unique()
    modaTipo = dados['Tipo'].mode()[0]
    contagem = dados['Tipo'].value_counts().to_dict()
    vlr_medio = dados[['Tipo','Valor c desc']]
    nota_media = dados[['Tipo','Avaliacao']]
    desc_medio = dados[['Tipo','Porcentagem desc']]
    resposta = {'Tipos:':tipo.tolist(),'Tipos mais presentes:':modaTipo,
                'Vezes que aparece':contagem,"valormedio":vlr_medio.to_dict(),
                "notamedia":nota_media.to_dict(),"descontomedio":desc_medio.to_dict()}
    return jsonify(resposta)

@app.route('/Modelo/')
#tipos dos produtos
def Modelo():
    dados = pd.read_csv('../1_Base_tratada/nikefinal.csv', sep= ";")
    tipo = dados['Modelo'].unique()
    modaTipo = dados['Modelo'].mode()[0]
    contagem = dados['Modelo'].value_counts().to_dict()
    vlr_medio = dados[['Modelo','Valor c desc']]
    nota_media = dados[['Modelo','Avaliacao']]
    desc_medio = dados[['Modelo','Porcentagem desc']]
    resposta = {'Modelos':tipo.tolist(),'Modelo mais presentes':modaTipo,
                'Modelos que aparecem':contagem,"valormedio":vlr_medio.to_dict(),
                "notamedia":nota_media.to_dict(),"descontomedio":desc_medio.to_dict()}
    return jsonify(resposta)

@app.route('/valoresComDesconto/') 
#Valor c desc
def valores_C_desconto():
    dados = pd.read_csv('../1_Base_tratada/nikefinal.csv', sep= ";")
    mediavalor = dados['Valor c desc'].mean()
    medianavalor = dados ['Valor c desc' ].median()
    maiorvalor = dados['Valor c desc'].max()
    menorvalor = dados['Valor c desc'].min()
    modavalor = dados['Valor c desc'].mode()[0]
    desvio = dados['Valor c desc'].std()
    valor_modelo = dados[['Valor c desc','Modelo']]
    valor_tipo = dados[['Valor c desc','Tipo']]
    q01 = dados['Valor c desc'].quantile(0.75)
    q02 = dados['Valor c desc'].quantile(0.25)
    Q1_tipo = dados.loc[dados['Valor c desc'] >= q01, 'Tipo'].value_counts().to_dict()
    Q2_tipo = dados.loc[dados['Valor c desc'] <= q02, 'Tipo'].value_counts().to_dict()
    Q1_modelo = dados.loc[dados['Valor c desc'] >= q01, 'Modelo'].value_counts().to_dict()
    Q2_modelo = dados.loc[dados['Valor c desc'] <= q02, 'Modelo'].value_counts().to_dict()
    resposta = {'Media valores':f"{mediavalor:.2f}",'Mediana valores':medianavalor,'Mais caro:':maiorvalor,'Mais barato':menorvalor,'Moda':modavalor, 'Desvio':f'{desvio:.2f}',
                'Q1tipo':Q1_tipo,'Q2tipo':Q2_tipo,'Q1modelo':Q1_modelo,
                'Q2modelo':Q2_modelo,'valormodelo':valor_modelo.to_dict(),'valortipo':valor_tipo.to_dict()}
    return jsonify(resposta)

@app.route('/ValoresSemDesconto/') 
#Valor c desc
def valores_S_desconto():
    dados = pd.read_csv('../1_Base_tratada/nikefinal.csv', sep= ";")
    mediavalor = dados['Valor s desc'].mean()
    medianavalor = dados ['Valor s desc' ].median()
    maiorvalor = dados['Valor s desc'].max()
    menorvalor = dados['Valor s desc'].min()
    modavalor = dados['Valor s desc'].mode()[0]
    desvio = dados['Valor s desc'].std()
    valor_modelo = dados[['Valor s desc','Modelo']]
    valor_tipo = dados[['Valor s desc','Tipo']]
    q01 = dados['Valor s desc'].quantile(0.75)
    q02 = dados['Valor s desc'].quantile(0.25)
    Q1_tipo = dados.loc[dados['Valor s desc'] >= q01, 'Tipo'].value_counts().to_dict()
    Q2_tipo = dados.loc[dados['Valor s desc'] <= q02, 'Tipo'].value_counts().to_dict()
    Q1_modelo = dados.loc[dados['Valor s desc'] >= q01, 'Modelo'].value_counts().to_dict()
    Q2_modelo = dados.loc[dados['Valor s desc'] <= q02, 'Modelo'].value_counts().to_dict()
    resposta = {'Media valores sem desconto:':f"{mediavalor:.2f}",'Mediana:':medianavalor,'Mais caro:':maiorvalor,'Mais barato':menorvalor,'Moda:':modavalor,'Desvio':f"{desvio:.2f}",
                'Q1tipo':Q1_tipo,'Q2tipo':Q2_tipo,'Q1modelo':Q1_modelo,
                'Q2modelo':Q2_modelo,'valormodelo':valor_modelo.to_dict(),'valortipo':valor_tipo.to_dict()
                }
    return jsonify(resposta)

@app.route('/Porcentagem desc/') 
#Valor c desc com desconto
def Porcentagem_desc():
    dados = pd.read_csv('../1_Base_tratada/nikefinal.csv', sep= ";")
    contagem_desconto = dados['Porcentagem desc'].value_counts().to_dict()
    mediadesconto = dados ['Porcentagem desc'].mean()
    medianadesconto = dados ['Porcentagem desc' ].median()
    maiordesconto = dados['Porcentagem desc'].max()
    menordesconto = dados['Porcentagem desc'].min()
    modadesconto = dados['Porcentagem desc'].mode()[0]
    desvio = dados['Porcentagem desc'].std()
    desconto = dados[['Porcentagem desc','Modelo']]
    desconto_tipo = dados[['Porcentagem desc','Tipo']]
    q01 = dados['Porcentagem desc'].quantile(0.75)
    q02 = dados['Porcentagem desc'].quantile(0.25)
    Q1_tipo = dados.loc[dados['Porcentagem desc'] >= q01, 'Tipo'].value_counts().to_dict()
    Q2_tipo = dados.loc[dados['Porcentagem desc'] <= q02, 'Tipo'].value_counts().to_dict()
    Q1_modelo = dados.loc[dados['Porcentagem desc'] >= q01, 'Modelo'].value_counts().to_dict()
    Q2_modelo = dados.loc[dados['Porcentagem desc'] <= q02, 'Modelo'].value_counts().to_dict()
    resposta = {'Media Desconto:':f"{mediadesconto:.2f}",'Mediana desconto:':f"{medianadesconto:.2f}",
                'Maior desconto:':maiordesconto,'Menor desconto':menordesconto,
                'Moda desconto:':modadesconto,'Desvio':f"{desvio:.2f}",
                'contagem':contagem_desconto, 'descontomodelo':desconto.to_dict(),
                'descontotipo':desconto_tipo.to_dict(),'Q1tipo':Q1_tipo,
                'Q2tipo':Q2_tipo,'Q1modelo':Q1_modelo,
                'Q2modelo':Q2_modelo
                }
    return jsonify(resposta)


@app.route('/Avaliação/')
#Descontos
def Avaliacao():
    dados = pd.read_csv('../1_Base_tratada/nikefinal.csv', sep= ";")
    nota_1 = dados.loc[(dados['Avaliacao'] >= 0) & (dados['Avaliacao'] <=1), 'Nome']
    nota_2 = dados.loc[(dados['Avaliacao'] > 1) & (dados['Avaliacao'] <=2), 'Nome']
    nota_3 = dados.loc[(dados['Avaliacao'] > 2) & (dados['Avaliacao'] <=3), 'Nome']
    nota_4 = dados.loc[(dados['Avaliacao'] > 3) & (dados['Avaliacao'] <=4), 'Nome']
    nota_5 = dados.loc[(dados['Avaliacao'] > 4) & (dados['Avaliacao'] <=5), 'Nome']
    contagem = dados['Avaliacao'].value_counts().to_dict()
    melhor_avalia = dados['Avaliacao'].max()
    melhores = dados.loc[dados['Avaliacao'] == melhor_avalia, 'Nome']
    pior_avalia = dados['Avaliacao'].min()
    piores = dados.loc[dados['Avaliacao'] == pior_avalia, 'Nome']
    mediaAvaliacao = dados['Avaliacao'].mean()
    modaAvaliacao = dados['Avaliacao'].mode()[0]
    medianaAvaliacao = dados['Avaliacao'].median()
    maiornota = dados['Avaliacao'].max()
    menornota = dados['Avaliacao'].min()
    desvio = dados['Avaliacao'].std()
    avaliacao_modelo = dados[['Avaliacao','Modelo']]
    avaliacao_tipo = dados[['Avaliacao','Tipo']]
    q01 = dados['Avaliacao'].quantile(0.75)
    q02 = dados['Avaliacao'].quantile(0.25)
    Q1_tipo = dados.loc[dados['Avaliacao'] >= q01, 'Tipo'].value_counts().to_dict()
    Q2_tipo = dados.loc[dados['Avaliacao'] <= q02, 'Tipo'].value_counts().to_dict()
    Q1_modelo = dados.loc[dados['Avaliacao'] >= q01, 'Modelo'].value_counts().to_dict()
    Q2_modelo = dados.loc[dados['Avaliacao'] <= q02, 'Modelo'].value_counts().to_dict()
    resposta = {'Media Avaliacao: ':f"{mediaAvaliacao:.2f}",
                'Moda Avaliacao: ':modaAvaliacao,
                'Mediana Avaliacao: ':medianaAvaliacao,
                'Maior avaliacao':maiornota,
                'Menor avaliacao':menornota,
                'Desvio: ':f"{desvio:.2f}",
                "Contagem":contagem,
                "melhores":melhores.to_dict(),
                "piores":piores.to_dict(),
                "nota1":nota_1.to_dict(),
                "nota2":nota_2.to_dict(),
                "nota3":nota_3.to_dict(),
                "nota4":nota_4.to_dict(),
                "nota5":nota_5.to_dict(),
                'avaliacaomodelo':avaliacao_modelo.to_dict(),
                'avaliacaotipo':avaliacao_tipo.to_dict(),'Q1tipo':Q1_tipo,
                'Q2tipo':Q2_tipo,'Q1modelo':Q1_modelo,
                'Q2modelo':Q2_modelo
                }
    return jsonify(resposta)

if __name__ == "__main__":
    app.run(debug=True)
