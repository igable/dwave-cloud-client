from __future__ import absolute_import, print_function

import os
import sys
import unittest
import textwrap

try:
    # python 3
    import unittest.mock as mock

    def iterable_mock_open(data):
        m = mock.mock_open(read_data=data)
        m.return_value.__iter__ = lambda self: self
        m.return_value.__next__ = lambda self: next(iter(self.readline, ''))
        return m

    configparser_open_namespace = "configparser.open"

except ImportError:
    # python 2
    import mock

    def iterable_mock_open(data):
        m = mock.mock_open(read_data=data)
        m.return_value.__iter__ = lambda self: iter(self.readline, '')
        return m

    configparser_open_namespace = "backports.configparser.open"


from dwave.cloud.config import detect_configfile_path, load_config_from_file, load_profile


class TestConfig(unittest.TestCase):

    config_body = """
        [defaults]
        url = https://cloud.dwavesys.com/sapi
        client = qpu

        [dw2000]
        solver = DW_2000Q_1
        token = ...

        [software]
        client = sw
        solver = c4-sw_sample
        token = ...

        [alpha]
        url = https://url.to.alpha/api
        proxy = http://user:pass@myproxy.com:8080/
        token = alpha-token
    """

    def test_config_load(self):
        with mock.patch(configparser_open_namespace, iterable_mock_open(self.config_body), create=True):
            config = load_config_from_file(filename="filename")
            self.assertEqual(config.sections(), ['dw2000', 'software', 'alpha'])
            self.assertEqual(config['dw2000']['client'], 'qpu')
            self.assertEqual(config['software']['client'], 'sw')

    def test_no_config_detected(self):
        with mock.patch("dwave.cloud.config.detect_configfile_path", lambda: None):
            self.assertRaises(ValueError, load_config_from_file)

    def test_invalid_filename_given(self):
        self.assertRaises(ValueError, load_config_from_file, filename='/path/to/non/existing/config')

    def test_config_load_profile(self):
        with mock.patch(configparser_open_namespace, iterable_mock_open(self.config_body), create=True):
            profile = load_profile(name="alpha", filename="filename")
            self.assertEqual(profile['token'], 'alpha-token')
            self.assertRaises(KeyError, load_profile, name="non-existing-section", filename="filename")

    def test_config_file_detection_cwd(self):
        configpath = "./dwave.conf"
        with mock.patch("os.path.exists", lambda path: path == configpath):
            self.assertEqual(detect_configfile_path(), configpath)

    def test_config_file_detection_user(self):
        if sys.platform == 'win32':
            # TODO
            pass
        elif sys.platform == 'darwin':
            configpath = os.path.expanduser("~/Library/Application Support/dwave/dwave.conf")
        else:
            configpath = os.path.expanduser("~/.config/dwave/dwave.conf")

        with mock.patch("os.path.exists", lambda path: path == configpath):
            self.assertEqual(detect_configfile_path(), configpath)

    def test_config_file_detection_system(self):
        if sys.platform == 'win32':
            # TODO
            pass
        elif sys.platform == 'darwin':
            configpath = os.path.expanduser("/Library/Application Support/dwave/dwave.conf")
        else:
            configpath = "/etc/xdg/dwave/dwave.conf"

        with mock.patch("os.path.exists", lambda path: path == configpath):
            self.assertEqual(detect_configfile_path(), configpath)

    def test_config_file_detection_nonexisting(self):
        with mock.patch("os.path.exists", lambda path: False):
            self.assertEqual(detect_configfile_path(), None)
