import quotes
from dataclasses import dataclass
from typing import List

def test_character_lookup():
    @dataclass
    class TestCase:
        name: str
        character_id: str
        character_dict: List[dict]
        expected: str

    testcases = [
            TestCase(
                name ="simple lookup",
                character_id = "1",
                character_dict = [{ "_id": "1", "name": "correct"}, {"_id": "2", "name": "incorrect"}],
                expected = "correct"),
            TestCase(
                name ="Lookup",
                character_id = "12345",
                character_dict = [{"_id": "1234", "name": "Paul"},
                    {"_id": "34", "name": "Barry"},
                    {"_id": "12345", "name": "Robert"},
                    {"_id": "1234", "name": "Harry"}],
                expected = "Robert"),
            TestCase(
                name ="missing name",
                character_id = "1",
                character_dict = [{"_id": "2", "name": "incorrect"}],
                expected = "unknown")
            ]

    for test in testcases:
        assert quotes.character_lookup(test.character_id ,test.character_dict) == test.expected 

