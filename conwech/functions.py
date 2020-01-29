"""
Home to all of the fun stuff, which consists of two main function pairs,
`nameperiod`/`readperiod` and `number2text`/`text2number`. As their
names hopefully suggest, for both pairs, each function is designed to be
the other's inverse (to the extent possible). The intended promise is
that calling one with the output of the other will return the input of
the other, or at least something equivalent, which could be used the
same way in the other direction.
"""

import typing
import conwech.lexicon
import conwech.regexlib
import conwech.exceptions


def nameperiod(zillion: int) -> str:
    """
    Names the period for the given zillion value.
    
    `nameperiod` returns the Conway-Wechsler name for a number with the
    given zillion value. The zillion property of a number in the
    short-scale system is equal to one less than the number of periods
    in the number, where a period is a set of one to three consecutive
    digits often separated by commas. I.e. A zillion value (z)
    represents a period's exponent (x) where z = (x - 3) / 3.
    
    Args:
        zillion (int): The zillion value of the period name.
        
    Returns:
        The name for the period with the given zillion value.
        
    Raises:
        TypeError: If `zillion` is not an int.
        
    Examples:
        >>> from conwech.functions import nameperiod
        >>> nameperiod(4)
        'quadrillion'
        >>> nameperiod(789)
        'novemoctogintaseptingentillion'
        >>> nameperiod(123456789)
        'tresviginticentillisesquinquagintaquadringentillinovemoctogintaseptingentillion'
        
    """
    if not isinstance(zillion, int):
        raise TypeError(
            'zillion argument should be {}; got {}!'.format(
                int, type(zillion)))
    
    # special cases
    if zillion <= 0:
        return '' if zillion else 'thousand'
    
    # generates prefix for each period of the zillion value
    prefixes = (conwech.lexicon.ZILLION_PERIOD_PREFIXES[int(p)]
                for p in '{:,}'.format(zillion).split(','))
    
    # combine prefixes and end with "illion"
    return 'illi'.join(prefixes) + 'illion'


def readperiod(name: str) -> int:
    """
    Convert `name` to its corresponding zillion value.
    
    The inverse function of `nameperiod`, `readperiod` parses the given
    period name by indexing a tuple of valid Conway-Wechsler period
    prefix components with each separate component of period name.
    
    If `period_name` is an empty string, `readperiod` returns -1 for the
    units period (first period).
    
    Args:
        name (str): The period name of any number period.
        
    Returns:
        The zillion value for the period with the given name.
        
    Raises:
        InvalidPeriodNameText: If any sub-component of `period_name`
            is not in conwech.lexicon.ZILLION_PERIOD_PREFIXES.
            
    Examples:
        >>> from conwech.functions import readperiod
        >>> readperiod('quadrillion')
        4
        >>> readperiod('novemoctogintaseptingentillion')
        789
        >>> readperiod('tresviginticentillisesquinquagintaquadringentillinovemoctogintaseptingentillion')
        123456789
        
    """
    if not isinstance(name, str):
        raise TypeError(
            'name argument should be {}; got {}'.format(
                str, type(name)))
    
    # handle special cases
    if name in ['', 'thousand']:
        return -1 if not name else 0
    
    # the name will be easier to parse in its composite parts
    period_prefixes = str(name).replace('illion', '').split('illi')
    
    zillion = ''
    for prefix in period_prefixes:
        # iteration > list comprehension here (for more helpful exceptions)
        if prefix not in conwech.lexicon.ZILLION_PERIOD_PREFIXES:
            raise conwech.exceptions.InvalidPeriodNameText(str(name), prefix)
        zillion += str(conwech.lexicon.ZILLION_PERIOD_PREFIXES.index(prefix)).zfill(3)
        
    # always return zillion as int
    return int(zillion)


def number2text(number: typing.Union[int, float, str]) -> str:
    """
    Construct the English short-scale spelling of the given number.
    
    `number2text` returns the english short-scale spelling for `number`
    which can be any positive or negative number passed as an integer,
    float, or string (as long as that string fits a valid numeric
    pattern; see conwech.regexlib.NUMERIC_STRING).
    
    `number2text` can handle values that exceed traditional limitations
    on numerical types. Pass `number` as a string for values requiring
    more precision or values greater outside the minimum and maximum
    int/float values.
    
    Note:
        `number2text` will also (eventually) be able to interpret a
        pseudo-sum-like string, the format sometimes returned by
        `text2number`. Currently, this functionality is not yet in
        place, but should be implemented soon...ish... Bite me.
        
    Args:
        number (int, float, str): The number to spell.
        
    Returns:
        The spelling of the given number.
        
    Raises:
        InvalidNumericString: If `number` does not follow python's
            conventional formatting for int and float types (see
            conwech.regexlib.NUMERIC_STRING).
            
    Examples:
        >>> from conwech.functions import number2text
        >>> number2text(-123456)
        'negative one hundred twenty-three thousand four hundred fifty-six'
        >>> number2text(4.56e100)
        'forty-five duotrigintillion six hundred untrigintillion'
        >>> number2text('7.89e500')
        'seven hundred eighty-nine quinquasexagintacentillion'
        >>> number2text('-1.2e-9')
        'negative twelve ten billionths'
        
    """
    if not isinstance(number, (int, float, str)):
        raise TypeError(
            'number argument should be {}, {}, or {}; got {}'.format(
                int, float, str, type(number)))
    
    # check for valid input format
    match = conwech.regexlib.NUMERIC_STRING.match(str(number))
    if not match:
        raise conwech.exceptions.InvalidNumericString(number)
    
    # capture and "normalize" components of input number
    bsign, bwhole, bfraction, esign, evalue = match.groups(default='')
    bsign = bsign.replace('+', '').replace('--', '').replace('-', 'negative ')
    exponent = int(esign + (evalue or '0')) - len(bfraction)
    digits = bwhole + bfraction
    position = len(digits) + exponent
    whole = digits[:max(position, 0)]
    numerator = digits[max(position, 0):]
    
    # pad whole to align periods
    whole = '0'*(3 - (max(position, 0) % 3 or 3)) + whole
    whole += '0'*(3 - (len(whole) % 3 or 3))
    
    periods = list()
    zillion = max(position - 1, 0) // 3 - 1
    # spell each period value and name individually
    for period in (int(whole[i:i+3]) for i in range(0, len(whole), 3)):
        if period > 0:
            periods.append(' '.join([conwech.lexicon.NATURAL_NUMBERS_LT_1000[period],
                                     nameperiod(zillion)]))
        zillion -= 1
        
    # add whole spelling to output list
    text = [' '.join(periods).strip(), ]
    if numerator: # handle fractions recursively
        denominator = number2text('1e' + str(abs(exponent))) + 'th'
        denominator = denominator.replace('one ', '').replace(' ', '-')
        text.append(' '.join([number2text(numerator), denominator])
                    + ('s' if int(numerator) > 1 else '')) # plurality
        
    # return "<sign> <whole> and <fraction>" or "zero" if nothing was spelled
    return bsign + (' and '.join(t for t in text if t) or 'zero')


def text2number(text: str) -> str:
    """
    Convert an English short-scale spelling to it's numerical value.
    
    `text2number` attempts to parse `text` and return a numeric string
    containing the corresponding value. The number(s) in the string will
    be in scientific notation.
    
    `text2number` returns a pseudo-sum-like representation if any of the
    periods in the given text would result in adding an unreasonable
    amount of consecutive zeros.
    
    `text2number` will recognize fractions, but only those with a
    base-ten denominator, i.e. those which can be represented with
    decimal digits.
    
    Args:
        text (str): The spelling of a number as a string.
        
    Returns:
        A numeric string representing the value of `text`.
        
    Raises:
        InvalidNumeralString: If `text` does not match the
            required format (see conwech.regexlib.NUMERAL_STRING).
        InvalidPeriodValueText: If any period value in `text`
            is not found in conwech.lexicon.NATURAL_NUMBERS_LT_1000.
        InvalidPeriodNameText: If any period name in `text` is not
            derived from a valid combination of Conway-Wechsler period
            prefixes (see conwech.functions.readperiod).
            
    Examples:
        >>> from conwech.functions import text2number
        >>> text2number('negative one hundred twenty-three one thousandths')
        '-1.23456789e5'
        >>> text2number('one millinillinillion and two one millinillinillionths')
        '1e3000003 + 2e-3000003'
        
    """
    if not isinstance(text, str):
        raise TypeError(
            'text argument should be {}; got {}'.format(
                str, type(text)))
    
    # check for valid input format
    match = conwech.regexlib.NUMERAL_STRING.match(text)
    if not match:
        raise conwech.exceptions.InvalidNumeralString(text)
    
    # reused iterative functionality
    def iterperiods(number_text):
        for period_value, period_name in conwech.regexlib.PERIOD_STRING.findall(number_text):
            period_value = period_value.replace('zero', '')
            
            # raise exception for invalid period values
            if period_value not in conwech.lexicon.NATURAL_NUMBERS_LT_1000:
                raise conwech.exceptions.InvalidPeriodValueText(period_value, period_name)
            
            # yields pairs of (value, zillion)
            yield (conwech.lexicon.NATURAL_NUMBERS_LT_1000.index(period_value),
                   3 * readperiod(period_name) + 3)
            
    # get period information for each portion of input text
    sign, whole, numerator, denominator = match.groups(default='')
    sign = sign.replace('positive ', '').replace('negative ', '-').replace('--', '')
    # correct numerator exponents (this line assumes denominator is a multiple of ten)
    denominator = ('one ' + denominator.replace('-', ' ')).replace('one ten', 'ten')
    whole, numerator, denominator = [list(iterperiods(t)) for t in (whole, numerator, denominator)]
    fraction = [(v, e - (denominator[0][1] + str(denominator[0][0]).count('0')))
                for v, e in numerator]
    
    periods = dict()
    # combine whole and fraction for all unique parts
    for value, exponent in (whole + fraction)[::-1]:
        periods[exponent + 3], periods[exponent] = divmod(periods.get(exponent, 0) + value, 1000)
        
    periods = ((str(v), e) for e, v in sorted(periods.items(), reverse=True) if v)
    numbers = [next(periods, ('0', 0)), ]
    for value, exponent in periods:
        digits, previous = numbers[-1]
        difference = previous - exponent
        if difference > 10000:
            numbers.append((value, exponent))
        else:
            numbers[-1] = digits + value.zfill(difference), exponent
            
    # return string representing the sum of numbers in normalized scientific notation
    return sign + ' {} '.format(sign or '+').join(
        v[:1] + ('.' + v[1:]).rstrip('.0') + ('e' + str(e + len(v[1:]))).rstrip('e')
        for v, e in numbers)
