from . import CURSOR, CONN

class Employee:
    """Class representing an employee."""

    def __init__(self, name, department_id, id=None):
        """Initialize an employee object with attributes."""
        self.id = id
        self.name = name
        self.department_id = department_id

    def __repr__(self):
        """Return a formatted string representation of the employee."""
        return f"<Employee {self.id}: {self.name}>"

    @classmethod
    def create_table(cls):
        """Create the 'employees' database table."""
        CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY,
                name TEXT,
                department_id INTEGER,
                FOREIGN KEY (department_id) REFERENCES departments(id)
            )
        """)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """Drop the 'employees' database table."""
        CURSOR.execute("DROP TABLE IF EXISTS employees")
        CONN.commit()

    def save(self):
        """Persist the Employee object to the 'employees' table."""
        if self.id is None:
            CURSOR.execute("""
                INSERT INTO employees (name, department_id)
                VALUES (?, ?)
            """, (self.name, self.department_id))
            self.id = CURSOR.lastrowid
            CONN.commit()
        else:
            CURSOR.execute("""
                UPDATE employees
                SET name=?, department_id=?
                WHERE id=?
            """, (self.name, self.department_id, self.id))
            CONN.commit()

    @classmethod
    def create(cls, name, department_id):
        """Create a new Employee instance and save it to the database."""
        employee = cls(name, department_id)
        employee.save()
        return employee

    @classmethod
    def instance_from_db(cls, row):
        """Create an Employee instance from a database row."""
        employee_id, name, department_id = row
        employee = cls(name, department_id, employee_id)
        return employee

    @classmethod
    def find_by_id(cls, id):
        """Find an Employee instance by its ID."""
        CURSOR.execute("SELECT * FROM employees WHERE id=?", (id,))
        row = CURSOR.fetchone()
        if row:
            return cls.instance_from_db(row)
        else:
            return None

    def update(self, name, department_id):
        """Update the attributes of an Employee instance."""
        self.name = name
        self.department_id = department_id
        self.save()

    def delete(self):
        """Delete an Employee instance from the database."""
        CURSOR.execute("DELETE FROM employees WHERE id=?", (self.id,))
        CONN.commit()
        self.id = None

    @classmethod
    def get_all(cls):
        """Get all Employee instances from the database."""
        CURSOR.execute("SELECT * FROM employees")
        rows = CURSOR.fetchall()
        return [cls.instance_from_db(row) for row in rows]
