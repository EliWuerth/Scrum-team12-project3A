import unittest
from app import validate_chart_type, validate_date, validate_symbol, validate_time_series

# Unit Tests
class TestInputValidation(unittest.TestCase):
    
    def test_validate_symbol(self):
        # Valid symbols
        self.assertTrue(validate_symbol("A"))         # Single character, valid
        self.assertTrue(validate_symbol("AAPL"))
        self.assertTrue(validate_symbol("GOOG"))
        self.assertTrue(validate_symbol("TSLA"))
        
        # Invalid symbols
        self.assertFalse(validate_symbol("AAPL123"))  # Contains numbers
        self.assertFalse(validate_symbol("ABCDEFGH"))  # Too long
        self.assertFalse(validate_symbol("aapl"))      # Not capitalized
        self.assertFalse(validate_symbol("A@PL"))      # Special characters

    def test_validate_chart_type(self):
        # Valid chart types
        self.assertTrue(validate_chart_type("1"))
        self.assertTrue(validate_chart_type("2"))
        
        # Invalid chart types
        self.assertFalse(validate_chart_type("3"))  # Not in range
        self.assertFalse(validate_chart_type("a"))  # Not numeric
        self.assertFalse(validate_chart_type(""))    # Empty input

    def test_validate_time_series(self):
        # Valid time series
        self.assertTrue(validate_time_series("1"))
        self.assertTrue(validate_time_series("2"))
        self.assertTrue(validate_time_series("3"))
        self.assertTrue(validate_time_series("4"))
        
        # Invalid time series
        self.assertFalse(validate_time_series("5"))  # Not in range
        self.assertFalse(validate_time_series("a"))  # Not numeric
        self.assertFalse(validate_time_series(""))    # Empty input

    def test_validate_date(self):
        # Valid dates
        self.assertTrue(validate_date("2023-01-01"))
        self.assertTrue(validate_date("2020-12-31"))
        
        # Invalid dates
        self.assertFalse(validate_date("2023-02-30"))  # Invalid date
        self.assertFalse(validate_date("2023-13-01"))  # Invalid month
        self.assertFalse(validate_date("2023-01-32"))  # Invalid day
        self.assertFalse(validate_date("01-01-2023"))  # Wrong format
        self.assertFalse(validate_date("2023/01/01"))  # Wrong separator

if __name__ == '__main__':
    unittest.main()