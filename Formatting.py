
from prettytable import PrettyTable
from Tools.ScreenColors import clr


def print_db_info(db, format=None):
    '''Print the DB information to the screen in a tabular format.'''
    
    if format == "table":
    
        info = PrettyTable(["{}: {}".format(clr.red("DB Name"),clr.white(db['info']['dbname'])),
                            "{}: {}".format(clr.red("DB User"),clr.white(db['info']['username'])),
                            "{}: {}".format(clr.red("DB Version"),clr.white(db['info']['version'])),
                            "{}: {}".format(clr.red("Tables"),clr.white(db['info']['table_count']))
                            ])
                            
        print(info)
        
    else:
        print(("\n{db}: {db_info}\t{user}: {user_info}\t{version}: {version_info}\t{tables}: {tables_info}\n") \
        .format(db=clr.red("DB Name"), db_info=clr.white(db['info']['dbname']),
        user=clr.red("DB User"), user_info=clr.white(db['info']['username']),
        version=clr.red("DB Version"), version_info=clr.white(db['info']['version']),
        tables=clr.red("Tables"), tables_info=clr.white(db['info']['table_count'])))

def render_cols(table):

    cols = PrettyTable(["No.","Columns"])
          
    cols.align = "l"
    
    i = 0
    
    for col,_ in table.items():
    
        i = i+1
        
        cols.add_row([clr.red(str(i)),clr.yellow(col)])
    
    return cols

def render_rows(col,col_name):

    rows = PrettyTable(["No.",col_name])
          
    rows.align = "l"
    
    i = 0
    
    for row in col:
    
        i = i+1
        
        rows.add_row([clr.red(str(i)),clr.yellow(row)])
    
    return rows
    
def render_tables(db):
    
    tables = PrettyTable(["No.","Tables"])
    
    tables.align = "l"
    
    i = 0
    
    for table,_ in db['tables'].items():
        
        i = i+1
        
        tables.add_row([clr.red(str(i)),clr.yellow(table)])
        
    return tables

def print_table_info(db, format=None):
    '''Print the table information to the screen in a tabular format.'''
    
    if format == "table":
        
        
        i = 0
        for table,content in db['tables'].items():
            
            i = i+1
                            
            head = PrettyTable(["{}".format(clr.white(str(i))),
                            "{}: {}".format(clr.red("Table Name"),clr.white(table)),
                            "{}: {}".format(clr.red("Columns"),clr.white(content['col_count'])),
                            "{}: {}".format(clr.red("Rows"),clr.white(content['row_count']))
                            ])
        
            body = render_cols(content['cols'])
            
            print(head)
            
            print(body)
    
    
    else:

        for table,content in db['tables'].items():
            
            print("\n{table}: {table_info}\t{column}: {column_info}\t{rows}: {rows_info}" \
            .format(table=clr.red("Table Name"),table_info=clr.white(table),
            column=clr.red("Columns"),column_info=clr.white(content['col_count']),
            rows=clr.red("Rows"),rows_info=clr.white(content['row_count'])))
            
            print(clr.yellow("COLUMNS:"))
            
            for col in content['cols']:
            
                print(clr.yellow("\t{}".format(col)))