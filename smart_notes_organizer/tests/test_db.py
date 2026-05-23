"""
Automated Unit Tests for Smart Notes Organizer.
Tests database CRUD operations, business logic, validation, and search capabilities.
Runs in isolation using SQLite in-memory databases (:memory:).
"""
import unittest
import os
import sys
import time

# Ensure main directory is in path to import config and database modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import DatabaseManager, DatabaseError

class TestDatabaseOperations(unittest.TestCase):
    """Unit test cases for validating core SQLite Database and CRUD functionality."""

    def setUp(self):
        """Run setup before each individual test case. Spins up an isolated in-memory DB."""
        self.db = DatabaseManager(":memory:")

    def tearDown(self):
        """Cleanup after each individual test case."""
        pass

    def test_db_initialization(self):
        """Ensure schema creation executes without issues on initialization."""
        # DatabaseManager constructor executes initialize_db
        # We verify that table 'notes' exists in sqlite_master
        conn = self.db._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='notes'")
        row = cursor.fetchone()
        conn.close()
        
        self.assertIsNotNone(row, "The 'notes' table should be created during initialization.")
        self.assertEqual(row['name'], 'notes')

    def test_add_note_success(self):
        """Verify adding a note correctly returns a valid ID and populates fields."""
        note_id = self.db.add_note(
            title="Meeting Notes",
            content="Discuss project deliverables and timeline.",
            category="Work"
        )
        self.assertIsInstance(note_id, int)
        self.assertTrue(note_id > 0)

        # Retrieve and verify fields
        note = self.db.get_note_by_id(note_id)
        self.assertIsNotNone(note)
        self.assertEqual(note['title'], "Meeting Notes")
        self.assertEqual(note['content'], "Discuss project deliverables and timeline.")
        self.assertEqual(note['category'], "Work")
        self.assertIsNotNone(note['created_at'])
        self.assertIsNotNone(note['updated_at'])

    def test_add_note_empty_title_fails(self):
        """Verify attempting to add notes with empty or blank titles raises DatabaseError."""
        with self.assertRaises(DatabaseError) as context:
            self.db.add_note(title="   ", content="Valid content but empty title", category="Personal")
        
        self.assertIn("title cannot be blank", str(context.exception))

        with self.assertRaises(DatabaseError):
            self.db.add_note(title="", content="No title at all", category="Personal")

    def test_get_all_notes_ordering(self):
        """Verify get_all_notes returns note records in descending order of updated_at."""
        # Create three notes with small delays to ensure distinct update times
        id1 = self.db.add_note("First Note", "Content A", "Ideas")
        time.sleep(1.0)  # Wait so updated_at differs
        id2 = self.db.add_note("Second Note", "Content B", "Work")
        time.sleep(1.0)
        id3 = self.db.add_note("Third Note", "Content C", "Personal")

        notes = self.db.get_all_notes()
        self.assertEqual(len(notes), 3)
        
        # Newest should be first
        self.assertEqual(notes[0]['id'], id3)
        self.assertEqual(notes[1]['id'], id2)
        self.assertEqual(notes[2]['id'], id1)

    def test_get_note_by_invalid_id(self):
        """Verify fetching non-existent note IDs safely returns None."""
        note = self.db.get_note_by_id(9999)
        self.assertIsNone(note)

    def test_update_note_success(self):
        """Verify modifying an existing note updates its schema columns and updated_at."""
        note_id = self.db.add_note("Original Title", "Original Content", "Ideas")
        original_note = self.db.get_note_by_id(note_id)
        
        time.sleep(1.0) # Ensure updated timestamp will change

        # Update note
        success = self.db.update_note(
            note_id=note_id,
            title="Modified Title",
            content="Modified Content",
            category="Important"
        )
        self.assertTrue(success)

        # Retrieve and verify edits
        updated_note = self.db.get_note_by_id(note_id)
        self.assertEqual(updated_note['title'], "Modified Title")
        self.assertEqual(updated_note['content'], "Modified Content")
        self.assertEqual(updated_note['category'], "Important")
        self.assertEqual(updated_note['created_at'], original_note['created_at'])
        self.assertNotEqual(updated_note['updated_at'], original_note['updated_at'])

    def test_update_note_empty_title_fails(self):
        """Verify modifying notes with blank titles is blocked and raises DatabaseError."""
        note_id = self.db.add_note("Valid Title", "Content", "Ideas")
        
        with self.assertRaises(DatabaseError) as context:
            self.db.update_note(note_id, title="  ", content="New Content", category="Work")
            
        self.assertIn("title cannot be blank", str(context.exception))

    def test_update_non_existent_note(self):
        """Verify updating non-existent IDs returns False without crashing."""
        success = self.db.update_note(9999, "Title", "Content", "Work")
        self.assertFalse(success)

    def test_delete_note_success(self):
        """Verify removing notes deletes them from the DB and they cannot be queried."""
        note_id = self.db.add_note("To Be Deleted", "Content", "Personal")
        
        # Delete note
        success = self.db.delete_note(note_id)
        self.assertTrue(success)

        # Try to retrieve it
        note = self.db.get_note_by_id(note_id)
        self.assertIsNone(note)

        # Verify count is 0
        all_notes = self.db.get_all_notes()
        self.assertEqual(len(all_notes), 0)

    def test_delete_non_existent_note(self):
        """Verify deleting non-existent IDs returns False without raising exceptions."""
        success = self.db.delete_note(9999)
        self.assertFalse(success)

    def test_search_notes(self):
        """Verify keyword searches match partially in title, content, or category."""
        self.db.add_note("Buy Groceries", "Need milk, eggs, and bread.", "Todo")
        self.db.add_note("Project Kickoff Meeting", "Schedule a sync for next Monday.", "Work")
        self.db.add_note("Creative Writing Ideas", "Sci-fi plot outline and characters.", "Ideas")

        # 1. Search by title match (partial)
        results = self.db.search_notes("Groceries")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], "Buy Groceries")

        # 2. Search by content match (case-insensitive & partial)
        results = self.db.search_notes("monday")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], "Project Kickoff Meeting")

        # 3. Search by category match
        results = self.db.search_notes("ideas")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], "Creative Writing Ideas")

        # 4. Search yielding no matches
        results = self.db.search_notes("Python Code")
        self.assertEqual(len(results), 0)

if __name__ == '__main__':
    unittest.main()
