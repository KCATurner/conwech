"""
Unit tests for the conwech.__main__.
"""

import re
import pytest
import subprocess
import conwech.__main__


class TestRead:

    @pytest.mark.parametrize(
        argnames='numeral',
        argvalues=['negative twelve thousand and three tenths', ])
    def test_nominal(self, numeral):
        output = subprocess.run(
            ['python', str(conwech.__main__.__file__), 'read', numeral],
            capture_output=True, text=True, check=True).stdout
        for color in conwech.__main__.Colors:
            output = output.replace(color.value, '')
        assert output.strip() == conwech.functions.text2number(numeral)


class TestSpell:

    @pytest.mark.parametrize(
        argnames='number',
        argvalues=['-12000.3'])
    def test_nominal(self, number):
        output = subprocess.run(
            ['python', str(conwech.__main__.__file__), 'spell', str(number)],
            capture_output=True, text=True, check=True).stdout
        for color in conwech.__main__.Colors:
            output = output.replace(color.value, '')
        assert output.strip() == conwech.functions.number2text(number)

    def test_recursive_flag(self):
        output = subprocess.run(
            ['python', str(conwech.__main__.__file__), 'spell', '-r', '323'],
            capture_output=True, text=True, check=True).stdout
        for color in conwech.__main__.Colors:
            output = output.replace(color.value, '')
        numbers = [int(n) for n in re.findall(r'\b(\d+)\b', output)]
        assert numbers == [23, 11, 6, 3, 5, 4, 4]
