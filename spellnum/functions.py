"""
Functions of the spellnum module.
"""

import spellnum.lexicon
import spellnum.regexlib
import spellnum.exceptions


def get_period_name(base_illion):
    """
    Constructs the period name/suffix from tuples of lexical components
    using each digit in the given base-illion value; currently limited
    to base-illion values less than 1000 (millinillion).
    
    :param int base_illion: the base-illion value of the period name
    :return str: the name for the period with the given base-illion value
    """
    
    if not isinstance(base_illion, int):
        raise TypeError('base_illion must be an integer!')
    
    if base_illion < 0:
        return ''
    elif base_illion < 10:
        return spellnum.lexicon.UNIQUE_PERIODS[base_illion]
    elif base_illion >= 1000:
        # TODO: handling this with recursion is basically daring the user to go insane with scientific notation...
        return get_period_name(base_illion // 1000)[:-2]\
               + get_period_name(base_illion % 1000).replace('thousand', 'nillion')
    
    # build suffix from lexical components
    hund, tens, unit = (int(digit) for digit in str(base_illion).zfill(3))
    suffix = spellnum.lexicon.PERIOD_COMPONENTS_UNIT[unit]\
             + spellnum.lexicon.PERIOD_COMPONENTS_TENS[tens]\
             + spellnum.lexicon.PERIOD_COMPONENTS_HUND[hund] + 'llion'
    
    # catch and correct lexical component combination exceptions
    if spellnum.lexicon.PERIOD_COMPONENTS_UNIT[unit] in ('tre', 'se', 'septe', 'nove'):
        suffix = spellnum.regexlib.X_LEXICAL_EXCEPTION.sub(repl='x', string=suffix)
        suffix = spellnum.regexlib.S_LEXICAL_EXCEPTION.sub(repl='s', string=suffix)
        suffix = spellnum.regexlib.M_LEXICAL_EXCEPTION.sub(repl='m', string=suffix)
        suffix = spellnum.regexlib.N_LEXICAL_EXCEPTION.sub(repl='n', string=suffix)
        
    return suffix.replace('allion', 'illion')


def num2txt(number):
    """
    Constructs the English short-scale spelling of the given number.
    
    :param number: an int float or numeric string to be spelled
    :return str: the spelling of the given number as a string
    """
    
    # check for valid input format
    match = spellnum.regexlib.VALID_NUMERIC_STRING.match(str(number))
    if not match:
        raise spellnum.exceptions.InvalidNumericalFormat(number)
    
    # capture and "normalize" components of input number
    sign, whole, fraction, exponent = match.groups(default='')
    digits = whole + fraction
    exponent = int(exponent or 0) - len(fraction)
    position = len(digits) + exponent
    whole = digits[:max(position, 0)]
    fraction = digits[max(position, 0):]
    
    # handle negative numbers recursively
    if sign == '-' and digits:
        return 'negative ' + num2txt(str(number).lstrip('-'))
    
    # pad whole to align periods
    base_illion = max(position - 1, 0) // 3 - 1
    whole = '0'*(3 - (max(position, 0) % 3 or 3)) + whole
    whole = whole + '0'*(3 - (len(whole) % 3 or 3))
    
    periods = []
    # spell each period in whole
    for period in (int(whole[i:i+3]) for i in range(0, len(whole), 3)):
        if period > 0:
            periods.append(' '.join([spellnum.lexicon.INTEGERS_LT_1000[period],
                                     get_period_name(base_illion=base_illion)]))
        base_illion -= 1
        
    # combine periods into single string
    delimiter = ' ' # TODO: Should I make the delimiter a keyword argument?
    whole = delimiter.join(periods).strip(delimiter)
    
    # handle fractions recursively
    if fraction:
        denominator = 10**-exponent
        fraction = '{} {}th{}'.format(num2txt(fraction),
                                      num2txt(denominator),
                                      's' if int(fraction) > 1 else '')
        
    return whole + ' and ' + fraction if whole and fraction else whole or fraction or 'zero'


def txt2num(spelling):
    """"""
    # handle negatives recursively
    if spelling.startswith('negative'):
        return '-{}'.format(txt2num(spelling.replace('negative', '', 1)))
    
    whole = spelling.strip()
    match = spellnum.regexlib.FRACTION_SPELLING_FORMAT.match(whole)
    if match: # handle fractions recursively
        whole, numerator, denominator = match.groups(default='')
        numerator, denominator = int(txt2num(numerator)), int(txt2num(denominator))
        return '{}.{}'.format(int(txt2num(whole)) + (numerator // denominator),
                              str(numerator % denominator).zfill(str(denominator).count('0')))
    
    # TODO: This is going to be broken now that we can spell to infinity...
    suffixes = spellnum.lexicon.UNIQUE_PERIODS \
               + tuple(get_period_name(b) for b in range(21, 1000))
    
    result = 0
    period = list()
    for word in str(spelling).split():
        if word not in ('hundred',) + spellnum.lexicon.INTEGERS_LT_100:
            # TODO: raise more meaningful exception on index failure...
            value = spellnum.lexicon.INTEGERS_LT_1000.index(' '.join(period))
            result += value * (10**((suffixes.index(word) + 1) * 3))
            period = list()
        else:
            period.append(word)
            
    result += spellnum.lexicon.INTEGERS_LT_1000.index(' '.join(period))
    return str(result)
