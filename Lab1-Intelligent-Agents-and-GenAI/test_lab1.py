import csv
import math
import unittest
from pathlib import Path

HERE = Path(__file__).parent

def lighting_agent(occupied, light_lux):
    if occupied and light_lux < 300:
        return "LIGHT_ON"
    return "LIGHT_OFF"

def safer_lighting_agent(occupied, light_lux):
    if not isinstance(occupied, bool):
        return "MANUAL_REVIEW"
    if not isinstance(light_lux, (int, float)) or math.isnan(light_lux) or math.isinf(light_lux) or light_lux < 0:
        return "MANUAL_REVIEW"
    if occupied and light_lux < 300:
        return "LIGHT_ON"
    return "LIGHT_OFF"

def calculate_spam_metrics(tp, fp, fn, tn, c_fp=50, c_fn=10):
    n = tp + fp + fn + tn
    acc = (tp + tn) / n
    rec = tp / (tp + fn)
    cost = c_fp * fp + c_fn * fn
    return acc, rec, cost

class TestLab1(unittest.TestCase):
    def test_basic_lighting_agent(self):
        cases = [
            (True, 180, "LIGHT_ON"),
            (True, 420, "LIGHT_OFF"),
            (False, 70, "LIGHT_OFF"),
            (True, 300, "LIGHT_OFF"),
            (False, 300, "LIGHT_OFF"),
        ]
        for occ, lux, expected in cases:
            self.assertEqual(lighting_agent(occ, lux), expected)

    def test_safer_lighting_agent_abnormal(self):
        abnormal = [
            (None, 180),
            (True, -2),
            (True, None),
            (True, float("nan")),
            ("yes", 200),
            (False, -100)
        ]
        for occ, lux in abnormal:
            self.assertEqual(safer_lighting_agent(occ, lux), "MANUAL_REVIEW")

    def test_spam_cost_comparison(self):
        acc_a, rec_a, cost_a = calculate_spam_metrics(799, 11, 1, 189)
        acc_b, rec_b, cost_b = calculate_spam_metrics(762, 0, 38, 200)
        self.assertAlmostEqual(acc_a, 0.988)
        self.assertAlmostEqual(acc_b, 0.962)
        self.assertEqual(cost_a, 560)
        self.assertEqual(cost_b, 380)
        self.assertLess(cost_b, cost_a)  # Agent B is cheaper

    def test_claims_csv_classification(self):
        csv_file = HERE / "DCIT313_L1_Student_Claims.csv"
        self.assertTrue(csv_file.exists())
        with open(csv_file, newline="", encoding="utf-8-sig") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(len(rows), 12)
        for row in rows:
            self.assertIn(row["student_label"], ["SUPPORTED", "CONTRADICTED", "NOT_SPECIFIED"])
            self.assertTrue(len(row["supporting_quote"].strip()) > 0)

if __name__ == "__main__":
    unittest.main()
