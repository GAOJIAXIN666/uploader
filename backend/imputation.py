import sqlite3
import sqlite3
from turtle import left
from matplotlib.pyplot import table
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn import neighbors
from sklearn.metrics import mean_squared_error 
from math import sqrt
from sklearn.ensemble import RandomForestClassifier
import numpy as np

def getTableSchema(conn, table_name):
    res = []
    for row in conn.execute(f"PRAGMA table_info('{table_name}')").fetchall():
        # print(table_name)
        # print(row)
        res.append(row[1])
    return res

def mergeTable(conn, table_to_impute, column_to_impute, foreign_keys): 

    # table_to_impute = "items"
    # column_to_impute = "owner_id"
    # input_query = ""
    # foreign_keys = "title:item_category,title; owner_id:users,id"   # this_table_column: (other_table, other_table_column)   
    # conn = sqlite3.connect('./testDB.db')

    data = conn.execute("SELECT * FROM %s" % (table_to_impute)).fetchall()
    data = pd.DataFrame(data, columns = getTableSchema(conn, "%s" % (table_to_impute)))


    # Scenario 1: 
    if foreign_keys == "": 
        return data, set()

    # process foreign key-primary key relationship 
    fks = foreign_keys.split("; ")
    key_ls = set()
    for fk in fks: 
        print(f"Foreign key: {fk}")
        left_key, other = fk.split(":")
        try:
            table_to_merge, right_key = other.split(",")
        except Exception as exp: 
            print(type(exp))
            print(exp)

        print(f"Left key: {left_key}")
        print(f"Right table: {table_to_merge}")
        print(f"Right key: {right_key}")
        key_ls.add(left_key)
        key_ls.add(right_key)
        print("--------------------------")
        print("Merging table %s" % (table_to_merge))

        # check if the left column has some missing values 
        if sum(data[left_key].isnull()) > 0: 
            if left_key == column_to_impute:
                # Scenario 2a
                print(f"Cannot merge: there are missing values on {left_key} and it is the column to impute")
                continue
            else: 
                # Scenario 2b, drop the rows with NA
                data.dropna(subset=[left_key])

        # now, left column has no missing values 
        # Scenario 3
        data_to_merge = conn.execute("SELECT * FROM %s" % (table_to_merge)).fetchall()
        data_to_merge = pd.DataFrame(data_to_merge, columns = getTableSchema(conn, "%s" % (table_to_merge)))
        merged_df = data.merge(data_to_merge, how = "left", 
                                left_on=left_key, 
                                right_on=right_key,
                                suffixes=("", "_y"))
        new_cols = list(merged_df.columns)
        print(f"New Columns of merged table:{new_cols}")
        dup_col = right_key+"_y" # left_on = owner_id, right_on = id, but id also exists in left table, then it will create a column "id_y" 
        if dup_col in new_cols:
            new_cols.remove(dup_col)                       
        data = merged_df[new_cols]
        

    # print(f"Columns: {list(data.columns)}")
    print(f"Keys : {key_ls}")

    return data, key_ls



def impute_missing_values(sql_path, table_to_impute, column_to_impute, input_query, foreign_keys): 
    # get all tables 
    def sql_fetch(conn):
        # return all table names
        cursorObj = conn.cursor()
        cursorObj.execute('SELECT name from sqlite_master where type= "table"')
        return cursorObj.fetchall() 

    conn = sqlite3.connect(sql_path)
    tables = sql_fetch(conn)
    print(f"Tables in current database: {tables}")

    # for testing 
    # table_to_impute = "items"
    # column_to_impute = "owner_id"
    # input_query = "SELECT * FROM items"
    # foreign_keys = "title:item_category,title; owner_id:users,id"               
    # conn = sqlite3.connect('./testDB.db')

    # cur_table = conn.execute(f"SELECT * FROM {table_to_impute}") 
    # data = cur_table.fetchall() 
    # print(type(data))

    # process foreign key-primary key relationship 
    df, key_ls = mergeTable(conn, table_to_impute, column_to_impute, foreign_keys)

    return imputation(df, column_to_impute, key_ls)


def imputation(whole_data, column_to_impute, key_ls):
    print(f"Input columns: {list(whole_data.columns)}")
    col = whole_data[column_to_impute]
    n = len(whole_data)
    print("Unique value percentage: %.4f: " % (len(col.unique()) / n))
    if col.dtype.kind not in 'iufc' and len(col.unique()) / n >= 0.2: 
        return -1, None  # cannot impute
    cols = []
    for i in whole_data.columns:
        if i in key_ls:
            if i == column_to_impute:
                cols.append(i)
            else:
                continue
        elif whole_data[i].dtype.kind in 'iufc' or whole_data[i].dtype.name == 'category':
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
    x_test = test.drop(column_to_impute, axis=1)
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
    final_error = error_rf
    if error_knn < error_rf:
        model = model_knn
        final_error = error_knn
    else:
        model = model_rf
        need_scale = True
    X = dat.drop(column_to_impute,axis=1)
    if need_scale:
        X = scaler.fit_transform(X)
    for i in range(len(dat)):
        if np.isnan(dat.loc[i,column_to_impute]):
            whole_data.loc[i,column_to_impute] = model.predict(X[i,:])
    
    return final_error, whole_data
    
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


