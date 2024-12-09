from dash import Dash, dcc, html, Input, Output, callback,ctx,State
import os
import sqlite3
import pandas as pd
from utilidades import handler_slider,querier
import plotly.graph_objects as go
import dash_auth 

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)
app.server.secret_key=os.urandom(24)
seg_df=pd.read_csv('user_psw.csv')
user=seg_df.loc[0,'user']
pswd=seg_df.loc[0,'password']

# auth = dash_auth.BasicAuth(
#     app,
#     {user:pswd}
# )

connection=sqlite3.connect('main_database_semantic_2.db', check_same_thread=False)
cursor=connection.cursor()
total=pd.read_sql('SELECT COUNT(*) as total FROM documents',connection).loc[0,'total']
#print(total)
#df=df[df['feeling'].isnull()]
with open('count.txt') as gfile:
    content=gfile.read()

poscontroller=handler_slider(int(content))

server = app.server
#labels=sorted(['encabezado', 'antecedentes', 'consideraciones de la corte',
#             'decisión', 'firmas', 'salvamento de voto', 'intervenciones',
#             'competencia', 'sin sección', 'norma(s) demandada(s)',
#             'pretensiones', 'intervención del procurador', 'pruebas',
#             'actuaciones en sede revisión', 'audiencia(s) pública(s)',
#             'síntesis de la decisión'])
#labels=sorted(['quote', 'plain', 'emphasis', 'footnote', 'footnote_number',
#            'footnote_emphasis', 'title', 'title_emphasis', 'page_number', 'footnote_quote',
#            'quote_emphasis', 'page_number_quote', 'page_number_emphasis', 'footnote_quote_emphasis',
#            'emphasis_quote', 'title_quote', 'footnote_title_quote', 'footnote_emphasis_quote',
#            'footnote_title', 'title_quote_emphasis'])
labels=['normal',  'número de pie de página', 'cita', 'énfasis', 'pie de página',
 'énfasis_cita', 'pie de página_cita', 'título', 'título_cita', 'pie de página_énfasis', 'pie de página_énfasis_cita',
 'título_énfasis']

buttons_list=[]
inputs_list=[]
for label in labels:
    buttons_list.append(html.Button(label,id=f'class-{label}',n_clicks=0))
    inputs_list.append(Input(f'class-{label}','n_clicks'))
#print(len(inputs_list))
app.layout = html.Div([
    
    
    html.H2('Text labeler'),
    html.Div(id='sentencia-div',style={'top':'10%','position':'absolute'}),
    html.Div(id='class-output',style={'top':'15%','position':'absolute'}),
    html.Br(),
    html.Br(),
    html.Div(id='confirmation-div'),
    html.Div(id='paragraph-id-div',style={'top':'21%','position':'absolute'}),
    html.Div(id='paragraph-pos-div',style={'top':'24%','position':'absolute'}),
    
    html.Div(id='text-output',style={'top':'30%','position':'absolute','overflow':'scroll','height':'200px'}),
    
    
    html.Div([
        #html.P('Escoge la etiqueta adecuada, si el texto no tiene etiqueta o no es coherente escoger la etiqueta SIN SECCIÓN'),
        html.P('Escoge la etiqueta adecuada'),
        html.Div(
            children=buttons_list

        ),
        html.Br(),
        html.Div(children=[
            
            html.Button('⬅️ Previous',id='backward',n_clicks=0),
            html.Button('Next ➡️',id='forward',n_clicks=0)
        ],style={'margin-left':'40%'}),
        html.Div(id='position-div'),
        html.Div(id='summary-div')
        
        
        
    #],style={'margin-left':'auto','margin-right':'auto','position':'absolute','top':'50%','left':'50%','transform':'translate(-50%,50%)'}),
    ],style={'top':'70%','position':'absolute'}),
    
    
    
])
@app.callback(Output('position-div','children'),
              Output('text-output','children'),
              Output('class-output','children'),
              Output('confirmation-div','children'),
              Output('sentencia-div','children'),
              Output('paragraph-id-div','children'),
              Output('paragraph-pos-div','children'),
              [Input('forward','n_clicks'),
               Input('backward','n_clicks')])
def moving_forward(forward,backward):
    if ctx.triggered_id=='forward':
        poscontroller.forward()
        if poscontroller.actual_num>total-1:
            poscontroller.actual_num=total-1
        with open('count.txt','w') as gfile:
            content=gfile.write(str(poscontroller.actual_num))
    if ctx.triggered_id=='backward':
        poscontroller.backward()
        if poscontroller.actual_num<0:

            poscontroller.actual_num=0
        with open('count.txt','w') as gfile:
            content=gfile.write(str(poscontroller.actual_num))
    df=pd.read_sql(f'SELECT * FROM documents WHERE id={poscontroller.actual_num}',connection)
    text=df.loc[0,'text']
    label=df.loc[0,'text_type']
    real_label=df.loc[0,'real_label']
    sentencia=df.loc[0,'name']
    paragraph_id=df.loc[0,'paragraph_id']
    paragraph_pos=df.loc[0,'paragraph_pos']
    #print(type(label))
    msg=html.P(children=[html.P([f'La etiqueta sintética del documento {poscontroller.actual_num} es...'],style={'display':'inline-block'}),html.P([f'{label}'],style={'color':'green','display':'inline-block','font-size':'20px'})])
    msg2=html.P(children=[html.P([f'La etiqueta real del documento {poscontroller.actual_num} es...'],style={'display':'inline-block'}),html.P([f'{real_label}'],style={'color':'blue','display':'inline-block','font-size':'20px'})])
    msg3=html.P(children=[html.P([f'La sentencia correspondiente al documento {poscontroller.actual_num} es...'],style={'display':'inline-block'}),html.P([f'{sentencia}'],style={'color':'#00008B','display':'inline-block','font-size':'20px'})])
    msg4=html.P(children=[html.P([f'El paragraph_id correspondiente al documento {poscontroller.actual_num} es...'],style={'display':'inline-block'}),html.P([f'{paragraph_id}'],style={'color':'#00008B','display':'inline-block','font-size':'20px'})])
    msg5=html.P(children=[html.P([f'El paragraph_pos correspondiente al documento {poscontroller.actual_num} es...'],style={'display':'inline-block'}),html.P([f'{paragraph_pos}'],style={'color':'#00008B','display':'inline-block','font-size':'20px'})])
    
   
    
    with open('count.txt') as gfile:
        content=gfile.read()
    return f'{content}/{total-1}',text,msg,msg2,msg3,msg4,msg5

@app.callback(Output('confirmation-div','children', allow_duplicate=True),
              Output('summary-div','children', allow_duplicate=True),
             inputs_list,
              prevent_initial_call=True )
def update_step(a,b,c,d,e,f,g,h,i,j,k,l):
    true_label=ctx.triggered_id
    
    
    if true_label is None:
        true_label='paila-class'
    true_label=true_label.split('-')[1]
    if  true_label in labels:
        query=f"""UPDATE documents SET real_label="{true_label}" WHERE ID={poscontroller.actual_num}"""
        cursor.execute(query)
        connection.commit()
        msg=html.P(children=[html.P([f'La etiqueta Real del comentario {poscontroller.actual_num} se ha cambiado por..'],style={'display':'inline-block'}),html.P([f'{true_label}'],style={'color':'red','display':'inline-block','font-size':'20px'})])
        summary=pd.read_sql("""SELECT real_label,count(*) as  etiquetas_experta FROM documents group by real_label""",connection)
        fig=go.Figure()
        fig.add_trace(go.Table(header=dict(values=list(summary.columns)),cells=dict(values=[list(summary[c]) for c in summary.columns ])))
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
        figure=dcc.Graph(figure=fig)

        return msg,figure
    else:
        return '',''




if __name__ == '__main__':
    #app.run(host='207.246.120.159',debug=True)
    app.run(debug=True)
