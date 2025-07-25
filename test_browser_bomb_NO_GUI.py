import unittest
from unittest.mock import patch
from browser_bomb_NO_GUI import SmartBrowserBomb, log

class TestSmartBrowserBomb(unittest.TestCase):

    def setUp(self):
        self.bomb = SmartBrowserBomb()
        self.bomb.running = False
        self.bomb.triggered = False

    def test_detect_system_specs(self):
        self.bomb.detect_system_specs()
        self.assertIn(self.bomb.os_name, ["Windows", "Linux", "Darwin"])
        self.assertGreater(self.bomb.ram_mb, 0)
        self.assertGreater(self.bomb.cpu_cores, 0)

    def test_calculate_tab_count_low(self):
        self.bomb.ram_mb = 2000
        self.assertEqual(self.bomb.calculate_tab_count(), 500)

    def test_calculate_tab_count_medium(self):
        self.bomb.ram_mb = 4000
        self.assertEqual(self.bomb.calculate_tab_count(), 666)

    def test_calculate_tab_count_high(self):
        self.bomb.ram_mb = 16000
        self.assertEqual(self.bomb.calculate_tab_count(), 2000)

    def test_get_current_processes_returns_set(self):
        processes = self.bomb.get_current_processes()
        self.assertIsInstance(processes, set)
        for proc in processes:
            self.assertIsInstance(proc, str)

    @patch("builtins.print")
    def test_log_function(self, mock_print):
        log("Test log message")
        mock_print.assert_called_with("Test log message")

    @patch("cv2.VideoCapture")
    def test_capture_webcam_snapshot(self, mock_video):
        mock_video.return_value.read.return_value = (False, None)
        self.bomb.capture_webcam_snapshot()
        mock_video.return_value.release.assert_called()

    @patch("webbrowser.open")
    def test_launch_tabs_mocked(self, mock_open):
        self.bomb.tab_count = 3
        self.bomb.running = True
        self.bomb.launch_tabs()
        self.assertEqual(mock_open.call_count, 3)

if __name__ == '__main__':
    unittest.main()

