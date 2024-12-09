import pandas as pd
class handler_slider:
    def __init__(self,actual_num):
        self.actual_num=actual_num
    def forward(self):
        self.actual_num+=1
    def backward(self):
        self.actual_num-=1

class querier:
    def __init__(self,connection,df):
        self.df=df
        self.connection=connection
        self.cursor=self.connection.cursor()
    def update(self,feeling,indice):
        query=f"""UPDATE to_db SET feeling={feeling} WHERE ID={indice}"""
        self.cursor.execute(query)
        self.connection.commit()

