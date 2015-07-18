__author__ = 'nparslow'

import pstats

p = pstats.Stats('profile.out')
p.strip_dirs().sort_stats(-1).print_stats()