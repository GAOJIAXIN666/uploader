from fileinput import filename
from operator import index
from time import process_time
from tracemalloc import start
from urllib import response
from fastapi import FastAPI, UploadFile, File, Form, status, HTTPException
from fastapi.responses import FileResponse
import time

from tempfile import TemporaryDirectory
import os

from pandas import DataFrame
from py import process
from backend import imputation
from numpy import outer
import aiofiles
from typing import List
from pydantic import BaseModel
import pandas as pd
import traceback


app = FastAPI()
app.table_to_impute = "rail_ridership"
app.column_to_impute = "time_period_id"
app.input_query = "SELECT * FROM rail_ridership"
app.foreign_keys = "line_id:lines,line_id; station_id:stations,station_id; time_period_id:time_periods,time_period_id"


# class ImputationRes(BaseModel):
#     final_error: str
#     processed_table: DataFrame



@app.get("/")
async def root():
    return {"message": "Hello World"}


# @app.get("/impute_test")
# async def impute_test():
#     imputations = "abc"
#     best_model = "Random Forest"
#     training_acc = 0.7,
#     validation_acc = 0.6
#     return {
#         "values": imputations, # a list of values 
#         "best model": best_model,
#         "training accuracy": training_acc, 
#         "validation accuracy": validation_acc
#     }

@app.post("/sendqueries")
async def getQueryStr(table:str = Form(), column:str = Form(), foreignKey = Form(), query = Form()):
    print(f"Input table to impute: {table}")
    print(f"Input column to impute: {column}")
    print(f"Input foreign keys: {foreignKey}")
    print(f"Input query: {query}")

    app.table_to_impute = table
    app.column_to_impute = column
    app.foreign_keys = foreignKey
    app.input_query = query
 

@app.post("/upload")
async def impute(newFile: UploadFile = File()):
                # table:str = Form(), 
                # column:str = Form(), 
                # foreignKey:str = Form(), 
                # query:str = Form()):
    print(f"User uploaded database: {newFile.filename}")
    print(f"table to impute: {app.table_to_impute}")
    print(f"column to impute: {app.column_to_impute}")
    print(f"foreign keys: {app.foreign_keys}")
    print(f"query: {app.input_query}")

    with TemporaryDirectory() as sql_dir:
        sql_path = os.path.join(sql_dir, newFile.filename)
        async with aiofiles.open(sql_path, 'wb') as out_file:
            content = await newFile.read()  # async read
            await out_file.write(content)  # async write

            # Exception 1: -1, None  # cannot impute, unique value percentage > 0.2
            # Exception 2: Wrong format for foreign keys 

            try:
                start_time = time.time()
                processed_data, eval_metric = imputation.impute_missing_values(sql_path, app.table_to_impute, app.column_to_impute, app.input_query, app.foreign_keys)  
                end_time = time.time()    
                print("Time for imputation: %.4f s" % (end_time - start_time))
                #final_error = 0.1
                #processed_data = pd.DataFrame(data = {'col1': [1, 2], 'col2': [3, 4]})
                fname = "%s.csv" % (eval_metric)

                file_path = os.path.join("persistant_folder", fname)
                processed_data.to_csv(file_path, index=False)
              
                return FileResponse(file_path, media_type="text/csv")        
            except:
                traceback.print_exc()
                raise HTTPException(
                    status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                )   
                        

