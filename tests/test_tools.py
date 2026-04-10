"""Tests for hotkey and related tool functions in mcp_pyautogui_server."""

from unittest.mock import patch

from easy_automation_mcp.tools.keyboard import press_hotkey


class TestHotkey:
    """Tests for the hotkey() function."""

    def test_single_key_detected(self):
        """単一キー（ctrl）が keyboard.send に渡されること。"""
        with patch("keyboard.send") as mock_send:
            result = press_hotkey(keys=["ctrl"])
        mock_send.assert_called_once_with("ctrl")
        assert result["status"] == "success"

    def test_combination_keys_detected(self):
        """2キー組み合わせ（Ctrl+A）が keyboard.send に渡されること。"""
        with patch("keyboard.send") as mock_send:
            result = press_hotkey(keys=["ctrl", "a"])
        mock_send.assert_called_once_with("ctrl+a")
        assert result["status"] == "success"

    def test_three_key_combination_detected(self):
        """3キー組み合わせ（Ctrl+Shift+A）が keyboard.send に渡されること。"""
        with patch("keyboard.send") as mock_send:
            result = press_hotkey(keys=["ctrl", "shift", "a"])
        mock_send.assert_called_once_with("ctrl+shift+a")
        assert result["status"] == "success"

    def test_backspace_detected(self):
        """Backspace 単体が keyboard.send に渡されること。"""
        with patch("keyboard.send") as mock_send:
            result = press_hotkey(keys=["backspace"])
        mock_send.assert_called_once_with("backspace")
        assert result["status"] == "success"

    def test_ctrl_backspace_detected(self):
        """Ctrl+Backspace の組み合わせが keyboard.send に渡されること。"""
        with patch("keyboard.send") as mock_send:
            result = press_hotkey(keys=["ctrl", "backspace"])
        mock_send.assert_called_once_with("ctrl+backspace")
        assert result["status"] == "success"

    def test_invalid_key_name(self):
        """無効なキー名を渡した場合にエラーが返ること。"""
        with patch("keyboard.send", side_effect=ValueError("Key named 'invalidkey_xyz' not found")):
            result = press_hotkey(keys=["invalidkey_xyz"])
        assert result["status"] == "error"
        assert "invalidkey_xyz" in result["message"]

    def test_mixed_valid_and_invalid_keys(self):
        """有効なキーと無効なキーが混在する場合にエラーが返ること。"""
        with patch("keyboard.send", side_effect=ValueError("Key named 'invalidkey_xyz' not found")):
            result = press_hotkey(keys=["ctrl", "invalidkey_xyz"])
        assert result["status"] == "error"
        assert "invalidkey_xyz" in result["message"]

    def test_failsafe_exception(self):
        """予期しない例外が発生した場合にエラーが返ること。"""
        with patch("keyboard.send", side_effect=Exception("failsafe triggered")):
            result = press_hotkey(keys=["ctrl", "a"])
        assert result["status"] == "error"
        assert "failsafe" in result["message"].lower()

    def test_unexpected_exception(self):
        """予期しない例外が発生した場合にエラーが返ること。"""
        with patch("keyboard.send", side_effect=Exception("unexpected error")):
            result = press_hotkey(keys=["ctrl", "a"])
        assert result["status"] == "error"
        assert "unexpected error" in result["message"]
