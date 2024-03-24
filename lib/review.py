from .. import CURSOR, CONN
from .Employee import Employee

class Review:
    """Class representing a review for an employee."""

    def __init__(self, year, summary, employee_id, id=None):
        """Initialize a review object with attributes."""
        self.id = id
        self.year = year
        self.summary = summary
        self.employee_id = employee_id

    def __repr__(self):
        """Return a formatted string representation of the review."""
        return f"<Review {self.id}: {self.year} - {self.summary}>"

    @classmethod
    def create_table(cls):
        """Create the 'reviews' database table."""
        CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY,
                year INTEGER,
                summary TEXT,
                employee_id INTEGER,
                FOREIGN KEY (employee_id) REFERENCES employees(id)
            )
        """)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """Drop the 'reviews' database table."""
        CURSOR.execute("DROP TABLE IF EXISTS reviews")
        CONN.commit()

    def save(self):
        """Persist the Review object to the 'reviews' table."""
        if self.id is None:
            CURSOR.execute("""
                INSERT INTO reviews (year, summary, employee_id)
                VALUES (?, ?, ?)
            """, (self.year, self.summary, self.employee_id))
            self.id = CURSOR.lastrowid
            CONN.commit()
        else:
            CURSOR.execute("""
                UPDATE reviews
                SET year=?, summary=?, employee_id=?
                WHERE id=?
            """, (self.year, self.summary, self.employee_id, self.id))
            CONN.commit()

    @classmethod
    def create(cls, year, summary, employee_id):
        """Create a new Review instance and save it to the database."""
        review = cls(year, summary, employee_id)
        review.save()
        return review

    @classmethod
    def instance_from_db(cls, row):
        """Create a Review instance from a database row."""
        review_id, year, summary, employee_id = row
        review = cls(year, summary, employee_id, review_id)
        return review

    @classmethod
    def find_by_id(cls, id):
        """Find a Review instance by its ID."""
        CURSOR.execute("SELECT * FROM reviews WHERE id=?", (id,))
        row = CURSOR.fetchone()
        if row:
            return cls.instance_from_db(row)
        else:
            return None

    def update(self, year, summary, employee_id):
        """Update the attributes of a Review instance."""
        self.year = year
        self.summary = summary
        self.employee_id = employee_id
        self.save()

    def delete(self):
        """Delete a Review instance from the database."""
        CURSOR.execute("DELETE FROM reviews WHERE id=?", (self.id,))
        CONN.commit()
        self.id = None

    @classmethod
    def get_all(cls):
        """Get all Review instances from the database."""
        CURSOR.execute("SELECT * FROM reviews")
        rows = CURSOR.fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @property
    def year(self):
        """Getter for the 'year' attribute."""
        return self._year

    @year.setter
    def year(self, value):
        """Setter for the 'year' attribute."""
        if isinstance(value, int) and value >= 2000:
            self._year = value
        else:
            raise ValueError("Year must be an integer greater than or equal to 2000")

    @property
    def summary(self):
        """Getter for the 'summary' attribute."""
        return self._summary

    @summary.setter
    def summary(self, value):
        """Setter for the 'summary' attribute."""
        if isinstance(value, str) and value.strip() != "":
            self._summary = value
        else:
            raise ValueError("Summary must be a non-empty string")

    @property
    def employee_id(self):
        """Getter for the 'employee_id' attribute."""
        return self._employee_id

    @employee_id.setter
    def employee_id(self, value):
        """Setter for the 'employee_id' attribute."""
        if isinstance(value, int):
            employee = Employee.find_by_id(value)
            if employee:
                self._employee_id = value
            else:
                raise ValueError("Employee with the provided ID does not exist")
        else:
            raise ValueError("Employee ID must be an integer")
