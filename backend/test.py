import sqlite3
from matplotlib.pyplot import table
import pandas as pd


def mergeTable(conn, table_name): 

    def getTableSchema(conn, table_name):
        res = []
        for row in conn.execute(f"PRAGMA table_info('{table_name}')").fetchall():
            # print(table_name)
            # print(row)
            res.append(row[1])
        return res
            

    table_to_impute = "items"
    column_to_impute = "owner_id"
    input_query = ""
    foreign_keys = "title:item_category,title; owner_id:users,id"   # this_table_column: (other_table, other_table_column)
        
    conn = sqlite3.connect('./testDB.db')
    data = conn.execute("SELECT * FROM %s" % (table_to_impute)).fetchall()
    data = pd.DataFrame(data, columns = getTableSchema(conn, "%s" % (table_to_impute)))
    print(data)

    # print(type(data.at[1, "description"])) check if data type is correct

    # process foreign key-primary key relationship 
    fks = foreign_keys.split("; ")
    key_ls = set()
    for fk in fks: 
        left_key, other = fk.split(":")
        table_to_merge, right_key = other.split(",")
        key_ls.add(left_key)
        key_ls.add(right_key)
        print("Merging table %s" % (table_to_merge))

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
        #print(data)
        

    print("Final table: ")
    print(data)
    print(f"Keys : {key_ls}")

    return data, key_ls

