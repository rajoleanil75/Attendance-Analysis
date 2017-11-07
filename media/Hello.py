from xlrd import open_workbook
import MySQLdb

# Open the workbook and define the worksheet
book = open_workbook("pytest.xlsx")
#sheet = book.sheet_by_name("source")

# Establish a MySQL connection
database = MySQLdb.connect (host="localhost", user = "root", passwd = "", db = "anil")

# Get the cursor, which is used to traverse the database, line by line
cursor = database.cursor()

query = """INSERT INTO stud (roll,name) VALUES (%s, %s)"""

#for r in range(1, sheet.nrows):
#      product      = sheet.cell(r,).value
#      customer = sheet.cell(r,1).value
for sheet in book.sheets():
    n=sheet.nrows;
    for row in range(0,n):
        for col in range(0,1):
            roll=sheet.cell(row,0).value
            name=sheet.cell(row,1).value
            print(roll)
            print(name)
            values = (roll,name)
            cursor.execute(query, values)

cursor.close()

# Commit the transaction
database.commit()

# Close the database connection
database.close()
print("All Done! Bye, for now.")
