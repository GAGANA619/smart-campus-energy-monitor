from pathlib import Path
import unittest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
HTML_FILE = PROJECT_ROOT / "index.html"


class EnergyDashboardTests(unittest.TestCase):
    def test_dashboard_file_exists(self):
        self.assertTrue(HTML_FILE.exists())

    def test_buildings_exist(self):
        html = HTML_FILE.read_text(encoding="utf-8")
        self.assertIn("Academic Block A", html)
        self.assertIn("Library", html)
        self.assertIn("Laboratory Block", html)

    def test_consumption_values_exist(self):
        html = HTML_FILE.read_text(encoding="utf-8")
        self.assertIn("consumption: 120", html)
        self.assertIn("consumption: 85", html)
        self.assertIn("consumption: 150", html)

    def test_energy_targets_exist(self):
        html = HTML_FILE.read_text(encoding="utf-8")
        self.assertIn("target: 110", html)
        self.assertIn("target: 90", html)
        self.assertIn("target: 130", html)

    def test_warning_logic_exists(self):
        html = HTML_FILE.read_text(encoding="utf-8")
        self.assertIn("building.consumption > 100", html)
        self.assertIn("building.consumption - 100", html)

    def test_enhanced_summary_exists(self):
        html = HTML_FILE.read_text(encoding="utf-8")
        self.assertIn("totalConsumption", html)
        self.assertIn("highestBuilding", html)


if __name__ == "__main__":
    unittest.main(verbosity=2)