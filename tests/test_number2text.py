"""
Unit tests for number2text function.
"""

from unittest import TestCase
from spellnum import number2text, exceptions


# TODO: refactor, reevaluate, and expand on test cases where necessary


class InputValidity(TestCase):
    """
    Tests valid and invalid input types for number2text.
    """
    
    def test_invalid_input_type(self):
        for invalid_type in (None, {123, }, [123, ], (123, )):
            with self.subTest(invalid_type=invalid_type):
                self.assertRaises(exceptions.InvalidNumberLikeString, number2text, invalid_type)
                
    def test_invalid_input_formats(self):
        self.assertRaises(ValueError, number2text, '')
        self.assertRaises(ValueError, number2text, '.')
        self.assertRaises(ValueError, number2text, 'e')
        self.assertRaises(ValueError, number2text, '-')
        self.assertRaises(ValueError, number2text, '+')
        self.assertRaises(ValueError, number2text, '.e')
        self.assertRaises(ValueError, number2text, '.0e')
        self.assertRaises(ValueError, number2text, '.0e-')
        self.assertRaises(ValueError, number2text, '0.0e')
        self.assertRaises(ValueError, number2text, '0.0e-')
        self.assertRaises(ValueError, number2text, '0.e-0')
        self.assertRaises(ValueError, number2text, '--123')
        self.assertRaises(ValueError, number2text, '++123')
        self.assertRaises(ValueError, number2text, '-+123')
        self.assertRaises(ValueError, number2text, '+-123')
        self.assertRaises(ValueError, number2text, '1.2.3')
        
    def test_string_dXXX(self):
        expected = 'one hundred twenty-three one thousandths'
        self.assertMultiLineEqual(expected, number2text('.123'))
        self.assertMultiLineEqual('negative ' + expected, number2text('-.123'))
    
    def test_string_ndXXX(self):
        expected = 'one hundred twenty-three one thousandths'
        self.assertMultiLineEqual(expected, number2text('.123'))
        self.assertMultiLineEqual('negative ' + expected, number2text('-.123'))
    
    def test_ValidFormat_dXeX(self):
        expected = 'one hundred million'
        self.assertMultiLineEqual(expected, number2text(.1e9))
        self.assertMultiLineEqual(expected, number2text('.1e9'))
        self.assertMultiLineEqual('negative ' + expected, number2text(-.1e9))
        self.assertMultiLineEqual('negative ' + expected, number2text('-.1e9'))
    
    def test_ValidFormat_XdXEX(self):
        expected = 'one billion two hundred million'
        self.assertMultiLineEqual(expected, number2text(1.2E9))
        self.assertMultiLineEqual(expected, number2text('1.2E9'))
        self.assertMultiLineEqual('negative ' + expected, number2text(-1.2E9))
        self.assertMultiLineEqual('negative ' + expected, number2text('-1.2E9'))
    
    def test_ValidFormat_XdXeX(self):
        expected = 'one billion two hundred million'
        self.assertMultiLineEqual(expected, number2text(1.2e9))
        self.assertMultiLineEqual(expected, number2text('1.2e9'))
        self.assertMultiLineEqual('negative ' + expected, number2text(-1.2e9))
        self.assertMultiLineEqual('negative ' + expected, number2text('-1.2e9'))
    
    def test_ValidFormat_XdXenX(self):
        expected = 'twelve ten billionths'
        self.assertMultiLineEqual(expected, number2text(1.2e-9))
        self.assertMultiLineEqual(expected, number2text('1.2e-9'))
        self.assertMultiLineEqual('negative ' + expected, number2text(-1.2e-9))
        self.assertMultiLineEqual('negative ' + expected, number2text('-1.2e-9'))
    
    def test_ValidFormat_0dXeX(self):
        expected = 'one hundred million'
        self.assertMultiLineEqual(expected, number2text(0.1e9))
        self.assertMultiLineEqual(expected, number2text('0.1e9'))
        self.assertMultiLineEqual('negative ' + expected, number2text(-0.1e9))
        self.assertMultiLineEqual('negative ' + expected, number2text('-0.1e9'))
    
    def test_ValidFormat_Xd0eX(self):
        expected = 'one billion'
        self.assertMultiLineEqual(expected, number2text(1.0e9))
        self.assertMultiLineEqual(expected, number2text('1.0e9'))
        self.assertMultiLineEqual('negative ' + expected, number2text(-1.0e9))
        self.assertMultiLineEqual('negative ' + expected, number2text('-1.0e9'))
    
    def test_ValidFormat_XXXdXXXeXXX(self):
        expected = 'one hundred twenty-three quadragintillion four hundred fifty-six noventrigintillion'
        self.assertMultiLineEqual(expected, number2text(123.456e123))
        self.assertMultiLineEqual(expected, number2text('123.456e123'))
        self.assertMultiLineEqual('negative ' + expected, number2text(-123.456e123))
        self.assertMultiLineEqual('negative ' + expected, number2text('-123.456e123'))
    
    def test_ValidFormat_0XXdXX0e0XX(self):
        expected = 'twelve trillion three hundred forty billion'
        self.assertMultiLineEqual(expected, number2text(012.340e012))
        self.assertMultiLineEqual(expected, number2text('012.340e012'))
        self.assertMultiLineEqual('negative ' + expected, number2text(-012.340e012))
        self.assertMultiLineEqual('negative ' + expected, number2text('-012.340e012'))
    
    def test_PrecisionRetention(self):
        expected = ('one quadragintillion two hundred thirty-four noventrigintillion five hundred sixty-seven '
                    'octotrigintillion eight hundred ninety-eight septentrigintillion seven hundred sixty-five '
                    'sestrigintillion four hundred thirty-two quinquatrigintillion one hundred quattuortrigintillion')
        self.assertMultiLineEqual(expected, number2text('1.2345678987654321e123'))
        self.assertMultiLineEqual('negative ' + expected, number2text('-1.2345678987654321e123'))
        
        
class SpellingExceptions(TestCase):
    """
    Tests 'zero' spelling use cases for spell.
    NOTE: Due to the number of valid input formats, these tests are not exhaustive.
    """
    
    def test_singular_fraction(self):
        expected = 'one tenth'
        actual = number2text(0.1)
        self.assertMultiLineEqual(expected, actual)
    
    def test_float_0(self):
        expected = 'zero'
        actual = number2text(0)
        self.assertMultiLineEqual(expected, actual)
    
    def test_float_0d0(self):
        expected = 'zero'
        actual = number2text(0.0)
        self.assertMultiLineEqual(expected, actual)
    
    def test_float_0e0(self):
        expected = 'zero'
        actual = number2text(0e0)
        self.assertMultiLineEqual(expected, actual)
    
    def test_float_d0e0(self):
        expected = 'zero'
        actual = number2text(.0e0)
        self.assertMultiLineEqual(expected, actual)
    
    def test_float_0d0e0(self):
        expected = 'zero'
        actual = number2text(0.0e0)
        self.assertMultiLineEqual(expected, actual)
    
    def test_float_n0(self):
        expected = 'zero'
        actual = number2text(-0)
        self.assertMultiLineEqual(expected, actual)
    
    def test_float_n0d0(self):
        expected = 'zero'
        actual = number2text(-0.0)
        self.assertMultiLineEqual(expected, actual)
    
    def test_float_n0en0(self):
        expected = 'zero'
        actual = number2text(-0e-0)
        self.assertMultiLineEqual(expected, actual)
    
    def test_float_n0d0en0(self):
        expected = 'zero'
        actual = number2text(-0.0e-0)
        self.assertMultiLineEqual(expected, actual)
    
    def test_string_0(self):
        expected = 'zero'
        actual = number2text('0')
        self.assertMultiLineEqual(expected, actual)
    
    def test_string_0d0(self):
        expected = 'zero'
        actual = number2text('0.0')
        self.assertMultiLineEqual(expected, actual)
    
    def test_string_d0e0(self):
        expected = 'zero'
        actual = number2text('.0e0')
        self.assertMultiLineEqual(expected, actual)
    
    def test_string_0e0(self):
        expected = 'zero'
        actual = number2text('0e0')
        self.assertMultiLineEqual(expected, actual)
    
    def test_string_0d0e0(self):
        expected = 'zero'
        actual = number2text('0.0e0')
        self.assertMultiLineEqual(expected, actual)
    
    def test_string_n0(self):
        expected = 'zero'
        actual = number2text('-0')
        self.assertMultiLineEqual(expected, actual)
    
    def test_string_n0d0(self):
        expected = 'zero'
        actual = number2text('-0.0')
        self.assertMultiLineEqual(expected, actual)
    
    def test_string_n0en0(self):
        expected = 'zero'
        actual = number2text('-0e-0')
        self.assertMultiLineEqual(expected, actual)
    
    def test_string_n0d0en0(self):
        expected = 'zero'
        actual = number2text('-0.0e-0')
        self.assertMultiLineEqual(expected, actual)


class SpellingScientific(TestCase):
    """
    Tests spelling numbers in scientific notation.
    """
    
    def test_float_XXdXXe3(self):
        expected = number2text(12340)
        actual = number2text(12.34e3)
        self.assertMultiLineEqual(expected, actual)
    
    def test_float_XXdXXe2(self):
        expected = number2text(1234)
        actual = number2text(12.34e2)
        self.assertMultiLineEqual(expected, actual)
    
    def test_float_XXdXXe1(self):
        expected = number2text(123.4)
        actual = number2text(12.34e1)
        self.assertMultiLineEqual(expected, actual)
    
    def test_float_XXdXXe0(self):
        expected = number2text(12.34)
        actual = number2text(12.34e0)
        self.assertMultiLineEqual(expected, actual)
    
    def test_float_XXdXXen0(self):
        expected = number2text(12.34)
        actual = number2text(12.34e-0)
        self.assertMultiLineEqual(expected, actual)
    
    def test_float_XXdXXen1(self):
        expected = number2text(1.234)
        actual = number2text(12.34e-1)
        self.assertMultiLineEqual(expected, actual)
    
    def test_float_XXdXXen2(self):
        expected = number2text(.1234)
        actual = number2text(12.34e-2)
        self.assertMultiLineEqual(expected, actual)
    
    def test_float_XXdXXen3(self):
        expected = number2text(.01234)
        actual = number2text(12.34e-3)
        self.assertMultiLineEqual(expected, actual)
    
    def test_string_XXdXXe3(self):
        expected = number2text(12340)
        actual = number2text('12.34e3')
        self.assertMultiLineEqual(expected, actual)
    
    def test_string_XXdXXe2(self):
        expected = number2text(1234)
        actual = number2text('12.34e2')
        self.assertMultiLineEqual(expected, actual)
    
    def test_string_XXdXXe1(self):
        expected = number2text(123.4)
        actual = number2text('12.34e1')
        self.assertMultiLineEqual(expected, actual)
    
    def test_string_XXdXXe0(self):
        expected = number2text(12.34)
        actual = number2text('12.34e0')
        self.assertMultiLineEqual(expected, actual)
    
    def test_string_XXdXXen0(self):
        expected = number2text(12.34)
        actual = number2text('12.34e-0')
        self.assertMultiLineEqual(expected, actual)
    
    def test_string_XXdXXen1(self):
        expected = number2text(1.234)
        actual = number2text('12.34e-1')
        self.assertMultiLineEqual(expected, actual)
    
    def test_string_XXdXXen2(self):
        expected = number2text(.1234)
        actual = number2text('12.34e-2')
        self.assertMultiLineEqual(expected, actual)
    
    def test_string_XXdXXen3(self):
        expected = number2text(.01234)
        actual = number2text('12.34e-3')
        self.assertMultiLineEqual(expected, actual)
    
    def test_float_0d1eXX(self):
        expected = 'one vigintillion'
        actual = number2text(0.1e64)
        self.assertMultiLineEqual(expected, actual)
    
    def test_float_1d0eXX(self):
        expected = 'one vigintillion'
        actual = number2text(1.0e63)
        self.assertMultiLineEqual(expected, actual)
    
    def test_float_0d1enXX(self):
        expected = 'one one vigintillionth'
        actual = number2text(0.1e-62)
        self.assertMultiLineEqual(expected, actual)
    
    def test_float_1d0enXX(self):
        expected = 'one one vigintillionth'
        actual = number2text(1.0e-63)
        self.assertMultiLineEqual(expected, actual)
    
    def test_string_0d1eXX(self):
        expected = 'one vigintillion'
        actual = number2text('0.1e64')
        self.assertMultiLineEqual(expected, actual)
    
    def test_string_1d0eXX(self):
        expected = 'one vigintillion'
        actual = number2text('1.0e63')
        self.assertMultiLineEqual(expected, actual)
    
    def test_string_0d1enXX(self):
        expected = 'one one vigintillionth'
        actual = number2text('0.1e-62')
        self.assertMultiLineEqual(expected, actual)
    
    def test_string_1d0enXX(self):
        expected = 'one one vigintillionth'
        actual = number2text('1.0e-63')
        self.assertMultiLineEqual(expected, actual)


class SpellingDecimal(TestCase):
    """
    Tests spelling numbers with fractions in decimal format.
    """
    
    def test_float_X00XdX(self):
        expected = 'one thousand two and three tenths'
        actual = number2text(1002.3)
        self.assertMultiLineEqual(expected, actual)
    
    def test_float_X0XdXX(self):
        expected = 'one hundred two and thirty-four one hundredths'
        actual = number2text(102.34)
        self.assertMultiLineEqual(expected, actual)
    
    def test_float_XXdX0X(self):
        expected = 'twelve and three hundred four one thousandths'
        actual = number2text(12.304)
        self.assertMultiLineEqual(expected, actual)
    
    def test_float_XdX00X(self):
        expected = 'two and three thousand four ten thousandths'
        actual = number2text(2.3004)
        self.assertMultiLineEqual(expected, actual)
    
    def test_float_dX000X(self):
        expected = 'thirty thousand four one hundred thousandths'
        actual = number2text(.30004)
        self.assertMultiLineEqual(expected, actual)
    
    def test_string_X00XdX(self):
        expected = 'one thousand two and three tenths'
        actual = number2text('1002.3')
        self.assertMultiLineEqual(expected, actual)
    
    def test_string_X0XdXX(self):
        expected = 'one hundred two and thirty-four one hundredths'
        actual = number2text('102.34')
        self.assertMultiLineEqual(expected, actual)
    
    def test_string_XXdX0X(self):
        expected = 'twelve and three hundred four one thousandths'
        actual = number2text('12.304')
        self.assertMultiLineEqual(expected, actual)
    
    def test_string_XdX00X(self):
        expected = 'two and three thousand four ten thousandths'
        actual = number2text('2.3004')
        self.assertMultiLineEqual(expected, actual)
    
    def test_string_dX000X(self):
        expected = 'thirty thousand four one hundred thousandths'
        actual = number2text('.30004')
        self.assertMultiLineEqual(expected, actual)
