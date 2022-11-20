from re import T
import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn import neighbors
from sklearn.metrics import mean_squared_error 
from math import sqrt
from sklearn.ensemble import RandomForestClassifier

# Input arguments
table_to_impute = "items"
column_to_impute = "owner_id"
input_query = "SELECT * FROM items"
foreign_keys = {"title" : "item_category", "owner_id": "users"}  # which 


conn = sqlite3.connect('./testDB.db')
cur = conn.cursor()

# get all tables 
def sql_fetch(conn):
    cursorObj = conn.cursor()
    cursorObj.execute('SELECT name from sqlite_master where type= "table"')
    #print(cursorObj.fetchall())
    return cursorObj.fetchall()

tables = sql_fetch(conn)
print(tables)

# get the schema of all tables
for table in tables: 
    table_name = table[0] 
    if table_name != "sqlite_sequence":
        for row in cur.execute(f"PRAGMA table_info('{table_name}')").fetchall():
            pass
            # print(table_name)
            # print(row)


# which table to impute missing values 

cur_table = conn.execute(input_query) 
#subset_data = cur_table.fetchall() # subset of data 
whole_data = conn.execute(f"SELECT * FROM {table_to_impute}").fetchall()


# Merge table
# How to merge???? 

# for col, table in foreign_keys: 


#print(subset_data)
print(whole_data)


# Imputation Part

def imputation(whole_data,column_to_impute):
    col = whole_data[column_to_impute]
    n = len(whole_data)
    if col.dtype.kind not in 'iufc' and len(col.unique()) >= 10:
        return None
    cols = []
    for i in whole_data.columns:
        if whole_data[i].dtype.kind in 'iufc' or whole_data[i].dtype.name == 'category':
            cols.append(i)
        elif (n - len(whole_data[i].unique())) / n >= 0.9:
            whole_data[i] = pd.Categorical(whole_data[i])
            cols.append(i)
    dat = whole_data[cols]
    df = dat.dropna()
    if len(df) > 10000:
        df = df.sample(n=10000)
    df = pd.get_dummies(df)
    
    train , test = train_test_split(df, test_size = 0.3)
    x_train = train.drop(column_to_impute, axis=1)
    y_train = train[column_to_impute]
    x_test = test.drop(column_to_impute, axis = 1)
    y_test = test[column_to_impute]
    scaler = MinMaxScaler(feature_range=(0, 1))
    x_train_scaled = scaler.fit_transform(x_train)
    x_train = pd.DataFrame(x_train_scaled)
    x_test_scaled = scaler.fit_transform(x_test)
    x_test = pd.DataFrame(x_test_scaled)
    model_knn, error_knn = KNN(x_train,y_train,x_test,y_test)
    model_rf, error_rf = RandomForest(x_train, y_train, x_test, y_test)
    model= None
    need_scale = False
    if error_knn < error_rf:
        model = model_knn
    else:
        model = model_rf
        need_scale = True
    X = dat.drop(column_to_impute,axis=1)
    if need_scale:
        X = scaler.fit_transform(X)
    for i in range(len(dat)):
        if np.isnan(dat.loc[i,column_to_impute]):
            whole_data.loc[i,column_to_impute] = model.predict(X[i,:])
    
    return whole_data
    
def KNN(x_train,y_train,x_test,y_test):      
    model = neighbors.KNeighborsRegressor(k=sqrt(len(x_train)))
    model.fit(x_train,y_train)
    pred = model.predict(x_test)
    error = sqrt(mean_squared_error(y_test,pred))
    return model, error
    
def RandomForest(x_train,y_train,x_test,y_test):
    model = RandomForestClassifier()
    model.fit(x_train,y_train)
    pred = model.predict(x_test)
    error = sqrt(mean_squared_error(y_test,pred))
    return model, error

        

                

            

#cur.execute("PRAGMA table_info('Users')").fetchall()
#[(0, 'id', 'INTEGER', 0, None, 1), (1, 'name', 'TEXT', 0, None, 0), (2, 'email', 'TEXT', 0, None, 0)]


# for row in cur.execute("PRAGMA table_info('users')").fetchall():
#     print(row)

# (0, 'id', 'INTEGER', 0, None, 1)
# (1, 'name', 'TEXT', 0, None, 0)
# (2, 'email', 'TEXT', 0, None, 0)


