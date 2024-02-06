from tkinter import *
from tkinter import messagebox
import mysql.connector.pooling


# Initialize connection pool
connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="my_pool",
    pool_size=5,
    pool_reset_session=True,
    host="localhost",
    user="root",
    password="YOUR_PASSWORD",
    database="employee"
)


def close_connection(connection):
    connection.close()


def deleteData():
    employee_id = enterId.get()
    if not employee_id:
        messagebox.showwarning("Cannot Delete", "Please provide the Employee ID to delete the data")
    else:
        try:
            connection = connection_pool.get_connection()
            cursor = connection.cursor()
            query = "DELETE FROM empDetails WHERE empId=%s"
            cursor.execute(query, (employee_id,))
            connection.commit()
            enterId.delete(0, "end")
            enterName.delete(0, "end")
            enterDept.delete(0, "end")
            messagebox.showinfo("Delete Status", "Data Deleted Successfully")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error deleting data: {err}")
        finally:
            close_connection(connection)


# Insert Data Function
def insertData():
    # Read the data provided by the user
    id = enterId.get()
    name = enterName.get()
    dept = enterDept.get()
    if not (id and name and dept):  # Correcting condition for empty data
        messagebox.showwarning("Cannot Insert", "All the fields are required!")
    else:  # Insert data in the empDetails table
        try:
            myDB = mysql.connector.connect(host="localhost", user="root", passwd="YOUR_PASSWORD", database="employee")
            myCur = myDB.cursor()
            query = "INSERT INTO empDetails VALUES (%s, %s, %s)"
            myCur.execute(query, (id, name, dept))
            myDB.commit()
            enterId.delete(0, "end")
            enterName.delete(0, "end")
            enterDept.delete(0, "end")
            messagebox.showinfo("Insert Status", "Data Inserted Successfully")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error inserting data: {err}")
        finally:
            myDB.close()


# Update Data Function
def updateData():
    id = enterId.get()
    name = enterName.get()
    dept = enterDept.get()
    if id == "" or name == "" or dept == "":
        messagebox.showwarning("Cannot Update", "All the fields are required!")
    else:
        try:
            myDB = mysql.connector.connect(host="localhost", user="root", passwd="YOUR_PASSWORD", database="employee")
            myCur = myDB.cursor()
            query = "UPDATE empDetails SET empName=%s, empDept=%s WHERE empId=%s"
            myCur.execute(query, (name, dept, id))
            myDB.commit()
            enterId.delete(0, "end")
            enterName.delete(0, "end")
            enterDept.delete(0, "end")
            messagebox.showinfo("Update Status", "Data Updated Successfully")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error updating data: {err}")
        finally:
            myDB.close()


# Get Data Function
def getData():
    id = enterId.get()
    if id == "":
        messagebox.showwarning("Fetch Status", "Please provide the Emp ID to fetch the data")
    else:
        try:
            myDB = mysql.connector.connect(host="localhost", user="root", passwd="YOUR_PASSWORD", database="employee")
            myCur = myDB.cursor()
            query = "SELECT * FROM empDetails WHERE empID=%s"
            myCur.execute(query, (id,))
            rows = myCur.fetchall()
            for row in rows:
                enterName.insert(0, row[1])
                enterDept.insert(0, row[2])
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error fetching data: {err}")
        finally:
            myDB.close()


# Global variables for Entry widgets
enterId = None
enterName = None
enterDept = None


# Reset Fields Method
def resetFields():
    global enterId, enterName, enterDept
    if enterId and enterName and enterDept:
        enterId.delete(0, "end")
        enterName.delete(0, "end")
        enterDept.delete(0, "end")
    else:
        messagebox.showwarning("Entry Not Defined", "Entry fields are not defined")



# GUI Part

# Creating Parent Window
window = Tk()
window.geometry("600x270")
window.title("Employee CRUD App")


# All Labels
empId = Label(window, text="Employee ID", font=("Serif", 12))
empId.place(x=20, y=30)

# All Entry Boxes respective to Labels
enterId = Entry(window)
enterId.place(x=170, y=30)


# All Buttons

deleteBtn = Button(window, text="Delete", font=("Sans", 12), bg="white", command=deleteData)
deleteBtn.place(x=210, y=160)

insertBtn = Button(window, text="Insert", font=("Sans", 12), bg="white", command=insertData)
insertBtn.place(x=20, y=160)

updateBtn = Button(window, text="Update", font=("Sans", 12), bg="white", command=updateData)
updateBtn.place(x=80, y=160)

getBtn = Button(window, text="Fetch", font=("Sans", 12), bg="white", command=getData)
getBtn.place(x=150, y=160)

resetBtn = Button(window, text="Reset", font=("Sans", 12), bg="white", command=resetFields)  # Corrected function name
resetBtn.place(x=20, y=210)

showData = Listbox(window)
showData.place(x=330, y=30)

window.mainloop()