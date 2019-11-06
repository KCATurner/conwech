"""
Home to a set of tuples containing number name and period suffix
component strings. These tuples are defined in such a way that indexing
them will return the appropriate text (all lowercase) for the index
given.
"""

import conwech.regexlib


NATURAL_NUMBERS_LT_20 = ('', 'one', 'two', 'three', 'four',
                         'five', 'six', 'seven', 'eight', 'nine',
                         'ten', 'eleven', 'twelve', 'thirteen', 'fourteen',
                         'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen')
"""
Tuple of 20 strings where each member is the english word for its index
with the exception of an empty string for 0.
"""

NATURAL_DECADES_LT_100 = ('', 'ten', 'twenty', 'thirty', 'forty',
                          'fifty', 'sixty', 'seventy', 'eighty', 'ninety')
"""
Tuple of 10 strings where each member is the english word for 10 times
its index with the exception of an empty string for 0.
"""


NATURAL_NUMBERS_LT_100 = NATURAL_NUMBERS_LT_20 \
                         + tuple('-'.join((NATURAL_DECADES_LT_100[__ // 10],
                                           NATURAL_NUMBERS_LT_20[__ % 10])
                                          ).strip('-') for __ in range(20, 100))
"""
Tuple of 100 strings where each member is the english word for its
index with one exception. For functional purposes, the first (zeroth)
index of lexicon's `INTEGERS_LT_1000` tuple is an empty string as
opposed to being the string literal 'zero'.

Note:
    It probably goes without saying, but the only real reason to use
    `NATURAL_NUMBERS_LT_100` instead of `NATURAL_NUMBERS_LT_1000` is for
    matters where efficiency is a heavy concern.
    
Examples:
    >>> from conwech.lexicon import NATURAL_NUMBERS_LT_100
    >>> NATURAL_NUMBERS_LT_100[7]
    'seven'
    >>> NATURAL_NUMBERS_LT_100[13]
    'thirteen'
    >>> NATURAL_NUMBERS_LT_100[99]
    'ninety-nine'
    >>> INTEGERS_LT_100[0:3]
    ('', 'one', 'two')
    
"""


NATURAL_NUMBERS_LT_1000 = NATURAL_NUMBERS_LT_100 \
                          + tuple(' hundred '.join((NATURAL_NUMBERS_LT_100[__ // 100],
                                                    NATURAL_NUMBERS_LT_100[__ % 100])
                                                   ).strip() for __ in range(100, 1000))
"""
Tuple of 1000 strings where each member is the english word for its
index with one exception. For functional purposes, the first (zeroth)
index of lexicon's `INTEGERS_LT_1000` tuple is an empty string as
opposed to being the string literal 'zero'.

Examples:
    >>> from conwech.lexicon import NATURAL_NUMBERS_LT_1000
    >>> NATURAL_NUMBERS_LT_1000[7]
    'seven'
    >>> NATURAL_NUMBERS_LT_1000[13]
    'thirteen'
    >>> NATURAL_NUMBERS_LT_1000[999]
    'nine hundred ninety-nine'
    >>> NATURAL_NUMBERS_LT_1000[0:3]
    ('', 'one', 'two')
    
"""


_UNIQUE_PERIOD_PREFIXES = ('n', 'm', 'b', 'tr', 'quadr', 'quint',
                           'sext', 'sept', 'oct', 'non')
"""
Unique period prefixes for single digit base-illion values.
"""


_UNIT_PREFIX_COMPONENTS = ('', 'un', 'duo', 'tre', 'quattuor',
                           'quinqua', 'se', 'septe', 'octo', 'nove')
"""
Prefix components for the units digit of a base-illion period.
"""


_TENS_PREFIX_COMPONENTS = ('', 'deci', 'viginti', 'triginta',
                           'quadraginta', 'quinquaginta', 'sexaginta',
                           'septuaginta', 'octoginta', 'nonaginta')
"""
Prefix components for the tens digit of a base-illion period.
"""


_HUND_PREFIX_COMPONENTS = ('', 'centi', 'ducenti', 'trecenti',
                           'quadringenti', 'quingenti', 'sescenti',
                           'septingenti', 'octingenti', 'nongenti')
"""
Prefix components for the hundreds digit of a base-illion period.
"""


def __build_base_illion_prefixes():
    """
    Constructs prefixes for all base-illion periods from subcomponents.
    """
    result = list(_UNIQUE_PERIOD_PREFIXES)
    
    for period in range(10, 1000):
        # build prefix from lexical components
        base_illion = str(period).zfill(3)
        prefix = str(_UNIT_PREFIX_COMPONENTS[int(base_illion[-1])]
                     + _TENS_PREFIX_COMPONENTS[int(base_illion[-2])]
                     + _HUND_PREFIX_COMPONENTS[int(base_illion[-3])])
        
        # catch and correct exceptions
        if int(base_illion[-1]) in (3, 6, 7, 9):
            prefix = conwech.regexlib.PREFIX_COMBINATION_EXCEPTION_X.sub('x', prefix)
            prefix = conwech.regexlib.PREFIX_COMBINATION_EXCEPTION_S.sub('s', prefix)
            prefix = conwech.regexlib.PREFIX_COMBINATION_EXCEPTION_M.sub('m', prefix)
            prefix = conwech.regexlib.PREFIX_COMBINATION_EXCEPTION_N.sub('n', prefix)
            
        # prefix shouldn't end in "a" or "i"
        result.append(prefix.rstrip('ai'))
        
    return tuple(result)


PERIOD_PREFIXES_LT_1000 = __build_base_illion_prefixes()
"""
Prefixes for all base-illion period values. Indexing this tuple with a
base-illion period value will return the appropriate Conway-Wechsler
prefix (everything before the "illi"/"illion").

All prefixes are constructed using the appropriate sub-prefix
combinations and exception rules defined by the Conway-Wechsler naming
system.

The first prefix is 'n' (for building 'nilli' components) and the next
nine prefixes are based on the standard number names adopted before the
inception of the Conway-Wechsler system.

Examples:
    >>> from conwech.lexicon import PERIOD_PREFIXES_LT_1000
    >>> PERIOD_PREFIXES_LT_1000[:10]
    ('n', 'm', 'b', 'tr', 'quadr', 'quint', 'sext', 'sept', 'oct', 'non')
    >>> tuple(prefix + 'illon' for prefix in PERIOD_PREFIXES_LT_1000[1:5])
    ('million', 'billion', 'trillion', 'quadrillion', 'quintillion')
    >>> PERIOD_PREFIXES_LT_1000[12]
    'duodec'
    >>> PERIOD_PREFIXES_LT_1000[345]
    'quinquaquadragintatrecent'
    >>> 'illi'.join(PERIOD_PREFIXES_LT_1000[int(p)] for p in '12,000,345'.split(','))) + 'illion'
    'duodecillinilliquinquaquadragintatrecentillion'
    >>> PERIOD_PREFIXES_LT_1000[106]
    'sexcent'
    >>> PERIOD_PREFIXES_LT_1000[600]
    'sescent'
    
"""
