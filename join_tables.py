import pandas as pd
class JoinTables():
    def __init__(self):
        self.file1=None
        self.file2=None
        self.connected_file=None

    def readCSV(self,how):
        self.file1=input("Enter  first CSV file path: ")
        df1=pd.read_csv(self.file1)
        self.file2=input("Enter second file path: ")
        df2=pd.read_csv(self.file2)
        if how=="merge":
            merge_type=input("Enter the merge type (inner, outer, left, right): ").strip().lower()
            self.connected_file=pd.merge(df1,df2,how=merge_type,on="urun_id")

        elif how=="concat":
            self.connected_file=pd.concat([df1,df2],ignore_index=True)
        print(self.connected_file)

    def readExcel(self,how):
        self.file1=input("Enter  first Excel file path: ")
        df1=pd.read_excel(self.file1)
        self.file2=input("Enter second file path: ")
        df2=pd.read_excel(self.file2)
        if how=="merge":
            merge_type=input("Enter the merge type (inner, outer, left, right): ").strip().lower()
            self.connected_file=pd.merge(df1,df2,how=merge_type,on="urun id")
        elif how=="concat":
            self.connected_file=pd.concat([df1,df2],ignore_index=True)
        print(self.connected_file)

    def readJSON(self,how):
        self.file1=input("Enter  first Excel file path: ")
        df1=pd.read_json(self.file1)
        self.file2=input("Enter second file path: ")
        df2=pd.read_json(self.file2)
        if how=="merge":
            merge_type=input("Enter the merge type (inner, outer, left, right): ").strip().lower()
            self.connected_file=pd.merge(df1,df2,how=merge_type,on="urun_id")
        elif how=="concat":
            self.connected_file=pd.concat([df1,df2],ignore_index=True)
        print(self.connected_file)


    def addNewColumn(self,name,how):
        column1=how.split(" ")[0]
        column2=how.split(" ")[2]
        operateor=how.split(" ")[1]
        if operateor=="+":
            self.connected_file[name]=self.connected_file[column1]+self.connected_file[column2]
        elif operateor=="-":
            self.connected_file[name]=self.connected_file[column1]-self.connected_file[column2]
        elif operateor=="/":
            self.connected_file[name]=self.connected_file[column1]/self.connected_file[column2]
        elif operateor=="*":
            self.connected_file[name]=self.connected_file[column1]*self.connected_file[column2]
        
        print(self.connected_file)

    def parseValue(self,val,col_name=None):
        v=val.strip()
        if v=="":
            return pd.NA
        if col_name and "tarih" in col_name.lower():
            try:
                return pd.to_datetime(v,errors="coerce").date()
            except:
                return pd.NA
            
        try:
            return int(v)
        except:
            try:
                return float(v)
            except:
                return v

    def addNewRow(self):
        new_row_data=input("Enter the new row data separated by commas: ").strip().split(" ")
        print(new_row_data)
        if "tarih" in self.connected_file.columns:
            s=self.connected_file["tarih"].astype(str).str.strip().replace({"":pd.NA})
            dt=pd.to_datetime(s,errors="coerce",infer_datetime_format=True)
            self.connected_file["tarih"]=dt.dt.date

            bad=self.connected_file[self.connected_file["tarih"].isna()]
            if not bad.empty:
                print("These rows have invalid date format and will be set to NaT:")
                print(bad)

        cols=self.connected_file.columns
        parsed=[self.parseValue(val,col_name) for val,col_name in zip(new_row_data,cols)]
        self.connected_file.loc[len(self.connected_file)]=parsed


        print(self.connected_file)
 
    def sort(self,column_name,ascending=True):
        self.connected_file=self.connected_file.sort_values(by=column_name,ascending=ascending)
        print(self.connected_file)

    def saveToFile(self,name):
        self.connected_file.to_excel((f"{name}.xlsx"),index=False)

    def homeScreen(self):
        while True:
            process=input("What do you want to do? (add new column \nadd new row \nsort \nsave to excel file \nto exit: q): ").strip().lower()
            if process=="add new column":
                how_many=int(input("How many new columns do you want to add? "))
                for _ in range(how_many):
                    name=input("Enter the new column name: ")
                    how=input("Enter how to create the new column (column_name + caolumn_name): ")
                    table.addNewColumn(name=name,how=how)
            elif process=="add new row":
                how_many=int(input("How many new rows do you want to add? "))
                for _ in range(how_many):
                    table.addNewRow()
            elif process=="sort":
                column_name=input("Enter the column name to sort by: ")
                ascending=input("Sort ascending? (yes/no): ").strip().lower()=="yes"
                table.sort(column_name=column_name,ascending=ascending)
            elif process=="q":
                break

table=JoinTables()
file_type=input("Enter the file type (csv / excel / json / to exit: q): ").strip().lower()
while True:
    if file_type=="csv":
        how=input("Enter how to join the tables (merge, concat): ").strip().lower()
        table.readCSV(how=how)
        table.homeScreen()

    elif file_type=="excel":
        how=input("Enter how to join tables (merge/concat): ").strip().lower()
        table.readExcel(how=how)
        table.homeScreen()

    elif file_type=="json":
        how=input("Enter how to join tables (merge/concat)")
        table.readJSON(how=how)
        table.homeScreen()

    elif file_type=="q":
        break