# coding=utf-8
__author__ = 'nparslow'

import re

a = u"Des nos jours, il est vrai que la characteristique principale de la société est la tendance à consommer" \
    u" beaucoup de biens. Cette tendance s'appelle surconsommation et grâce à la publicité, elle influence tous" \
    u" les secteurs de la vie quotidienne."

r = ur'\s*[^\w\s\-]?\s*Des\s*nos\s*jours\s*\s?[^\w\s\-]+\s?\s*il\s*est\s*vrai\s*que\s*la\s*characteristique' \
    ur'\s*principale\s*de\s*la\s*socit'

print re.match(r, a, flags=re.UNICODE)