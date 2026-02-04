"""
Basic tests for RWSDBv2.1
Tests the core functionality of the Railway Station Database System v2.1
"""


def test_basic_imports():
    """Test that basic modules can be imported"""
    try:
        import sys
        from PyQt6.QtWidgets import QApplication
        print("Basic imports successful")
        return True
    except ImportError as e:
        print(f"Import error: {e}")
        return False


def test_database_manager():
    """Test the database manager functionality"""
    try:
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '..'))  # Add parent directory to path
        from database.manager import DatabaseManager
        db_manager = DatabaseManager()
        assert db_manager is not None
        print("Database manager created successfully")
        return True
    except Exception as e:
        print(f"Database manager test failed: {e}")
        return False


def run_tests():
    """Run all basic tests"""
    print("Running basic tests for RWSDBv2.1...")
    
    results = []
    results.append(test_basic_imports())
    results.append(test_database_manager())
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("All tests passed!")
        return True
    else:
        print("Some tests failed!")
        return False


if __name__ == "__main__":
    run_tests()