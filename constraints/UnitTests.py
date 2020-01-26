# TODO
import unittest

# from constraints.ConstraintContainsString import ConstraintContainsString
from . import ConstraintContainsString


class TestConstraintContainsString(unittest.TestCase):
    def test_string_contains_letter(self):
        constraint = ConstraintContainsString("a", True)
        output = constraint.is_satisfied_by_state("apple")
        self.assertEqual(output, True, "'a' should be in apple")

    # def test_sum_tuple(self):
    #     self.assertEqual(sum((1, 2, 2)), 6, "Should be 6")


if __name__ == "__main__":
    unittest.main()
