"""
Database manager for Smart Notes Organizer.
Handles SQLite CRUD operations with comprehensive exception handling.
"""
import sqlite3
import datetime
import logging
from typing import List, Dict, Any, Optional

# Setup basic logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class DatabaseError(Exception):
    """Custom exception class for database operations errors."""
    pass

class DatabaseManager:
    """Manages SQLite database connections, initialization, and queries for Notes."""

    def __init__(self, db_path: str):
        """Initialize database manager and run table setup."""
        self.db_path = db_path
        try:
            self.initialize_db()
        except sqlite3.Error as e:
            logging.error(f"Failed to initialize SQLite Database at {db_path}: {e}")
            raise DatabaseError(f"Database setup failed: {e}") from e

    def _get_connection(self) -> sqlite3.Connection:
        """Helper to create and return a database connection with dictionary-like rows."""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Access columns by name like dict keys
            return conn
        except sqlite3.Error as e:
            logging.error(f"Failed to establish database connection: {e}")
            raise DatabaseError(f"Could not connect to database: {e}") from e

    def initialize_db(self) -> None:
        """Create the notes schema table if it does not already exist."""
        query = """
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT,
            category TEXT NOT NULL DEFAULT 'Uncategorized',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            logging.info("Database and tables checked/initialized successfully.")
        except sqlite3.Error as e:
            logging.error(f"SQL Error during initialization: {e}")
            raise DatabaseError(f"Initialization query failed: {e}") from e
        finally:
            if conn:
                conn.close()

    def add_note(self, title: str, content: str, category: str) -> int:
        """
        Insert a new note into the database.
        
        Args:
            title: The title of the note. Must not be empty.
            content: The text content of the note.
            category: The tag/category of the note.
            
        Returns:
            The integer ID of the newly inserted note.
        """
        if not title.strip():
            raise DatabaseError("Note title cannot be blank or empty.")

        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = """
        INSERT INTO notes (title, content, category, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?)
        """
        conn = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(query, (title.strip(), content, category, now_str, now_str))
            conn.commit()
            new_id = cursor.lastrowid
            logging.info(f"Note added successfully with ID: {new_id}")
            return new_id
        except sqlite3.Error as e:
            logging.error(f"SQL Error while adding note: {e}")
            if conn:
                conn.rollback()
            raise DatabaseError(f"Failed to create new note: {e}") from e
        finally:
            if conn:
                conn.close()

    def get_all_notes(self) -> List[Dict[str, Any]]:
        """
        Fetch all notes ordered by updated_at descending.
        
        Returns:
            A list of dictionary-like rows containing all notes.
        """
        query = "SELECT * FROM notes ORDER BY updated_at DESC"
        conn = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            logging.error(f"SQL Error fetching all notes: {e}")
            raise DatabaseError(f"Failed to retrieve notes: {e}") from e
        finally:
            if conn:
                conn.close()

    def get_note_by_id(self, note_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve details of a single note by ID.
        
        Args:
            note_id: The ID of the note.
            
        Returns:
            A dictionary containing note info or None if not found.
        """
        query = "SELECT * FROM notes WHERE id = ?"
        conn = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(query, (note_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            logging.error(f"SQL Error retrieving note with ID {note_id}: {e}")
            raise DatabaseError(f"Failed to retrieve note details: {e}") from e
        finally:
            if conn:
                conn.close()

    def update_note(self, note_id: int, title: str, content: str, category: str) -> bool:
        """
        Update an existing note's values.
        
        Args:
            note_id: The ID of the note to update.
            title: The new title (cannot be empty).
            content: The new text content.
            category: The new category.
            
        Returns:
            True if the update was successful, False if no note had that ID.
        """
        if not title.strip():
            raise DatabaseError("Note title cannot be blank or empty.")

        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = """
        UPDATE notes
        SET title = ?, content = ?, category = ?, updated_at = ?
        WHERE id = ?
        """
        conn = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(query, (title.strip(), content, category, now_str, note_id))
            conn.commit()
            rows_affected = cursor.rowcount
            success = rows_affected > 0
            if success:
                logging.info(f"Note {note_id} updated successfully.")
            else:
                logging.warning(f"No note found with ID {note_id} to update.")
            return success
        except sqlite3.Error as e:
            logging.error(f"SQL Error updating note {note_id}: {e}")
            if conn:
                conn.rollback()
            raise DatabaseError(f"Failed to save changes to note: {e}") from e
        finally:
            if conn:
                conn.close()

    def delete_note(self, note_id: int) -> bool:
        """
        Delete a note from the database by ID.
        
        Args:
            note_id: The ID of the note to delete.
            
        Returns:
            True if deleted, False if no note had that ID.
        """
        query = "DELETE FROM notes WHERE id = ?"
        conn = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(query, (note_id,))
            conn.commit()
            rows_affected = cursor.rowcount
            success = rows_affected > 0
            if success:
                logging.info(f"Note {note_id} deleted successfully.")
            else:
                logging.warning(f"No note found with ID {note_id} to delete.")
            return success
        except sqlite3.Error as e:
            logging.error(f"SQL Error deleting note {note_id}: {e}")
            if conn:
                conn.rollback()
            raise DatabaseError(f"Failed to delete note: {e}") from e
        finally:
            if conn:
                conn.close()

    def search_notes(self, query_string: str) -> List[Dict[str, Any]]:
        """
        Search for notes matching query string in title or content (case-insensitive).
        
        Args:
            query_string: The term to search for.
            
        Returns:
            A list of dictionary notes matching the search criteria.
        """
        query = """
        SELECT * FROM notes 
        WHERE title LIKE ? OR content LIKE ? OR category LIKE ?
        ORDER BY updated_at DESC
        """
        conn = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            search_param = f"%{query_string}%"
            cursor.execute(query, (search_param, search_param, search_param))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            logging.error(f"SQL Error searching notes for term '{query_string}': {e}")
            raise DatabaseError(f"Failed to execute search: {e}") from e
        finally:
            if conn:
                conn.close()
