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


def execute_query(query, values=None, fetch_data=False):
    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()

        if fetch_data:
            return cursor.fetchall()
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error executing query: {err}")
    finally:
        close_connection(connection)


def delete_data():
    employee_id = enter_id.get()
    if not employee_id:
        messagebox.showwarning("Cannot Delete", "Please provide the Employee ID to delete the data")
    else:
        query = "DELETE FROM empDetails WHERE empId=%s"
        execute_query(query, (employee_id,))
        enter_id.delete(0, "end")
        enter_name.delete(0, "end")
        enter_dept.delete(0, "end")
        messagebox.showinfo("Delete Status", "Data Deleted Successfully")


def insert_data():
    id_value = enter_id.get()
    name = enter_name.get()
    dept = enter_dept.get()
    if not (id_value and name and dept):
        messagebox.showwarning("Cannot Insert", "All the fields are required!")
    else:
        query = "INSERT INTO empDetails VALUES (%s, %s, %s)"
        execute_query(query, (id_value, name, dept))
        enter_id.delete(0, "end")
        enter_name.delete(0, "end")
        enter_dept.delete(0, "end")
        messagebox.showinfo("Insert Status", "Data Inserted Successfully")


def update_data():
    id_value = enter_id.get()
    name = enter_name.get()
    dept = enter_dept.get()
    if id_value == "" or name == "" or dept == "":
        messagebox.showwarning("Cannot Update", "All the fields are required!")
    else:
        query = "UPDATE empDetails SET empName=%s, empDept=%s WHERE empId=%s"
        execute_query(query, (name, dept, id_value))
        enter_id.delete(0, "end")
        enter_name.delete(0, "end")
        enter_dept.delete(0, "end")
        messagebox.showinfo("Update Status", "Data Updated Successfully")


def get_data():
    id_value = enter_id.get()
    if id_value == "":
        messagebox.showwarning("Fetch Status", "Please provide the Emp ID to fetch the data")
    else:
        query = "SELECT * FROM empDetails WHERE empID=%s"
        rows = execute_query(query, (id_value,), fetch_data=True)
        for row in rows:
            enter_name.insert(0, row[1])
            enter_dept.insert(0, row[2])


def reset_fields():
    enter_id.delete(0, "end")
    enter_name.delete(0, "end")
    enter_dept.delete(0, "end")


# GUI Part
window = Tk()
window.geometry("600x270")
window.title("Employee CRUD App")

# All Labels
emp_id_label = Label(window, text="Employee ID", font=("Serif", 12))
emp_id_label.place(x=20, y=30)

# All Entry Boxes respective to Labels
enter_id = Entry(window)
enter_id.place(x=170, y=30)

# All Buttons
delete_btn = Button(window, text="Delete", font=("Sans", 12), bg="white", command=delete_data)
delete_btn.place(x=210, y=160)

insert_btn = Button(window, text="Insert", font=("Sans", 12), bg="white", command=insert_data)
insert_btn.place(x=20, y=160)

update_btn = Button(window, text="Update", font=("Sans", 12), bg="white", command=update_data)
update_btn.place(x=80, y=160)

get_btn = Button(window, text="Fetch", font=("Sans", 12), bg="white", command=get_data)
get_btn.place(x=150, y=160)

reset_btn = Button(window, text="Reset", font=("Sans", 12), bg="white", command=reset_fields)
reset_btn.place(x=20, y=210)

show_data = Listbox(window)
show_data.place(x=330, y=30)

window.mainloop()
