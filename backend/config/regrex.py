
import pandas as pd

from os import path

import sys
sys.path.append('..')
usual_symptom = r'\bs[ô|ố|ó|o]t|ho|m[ê|ệ|e|ẹ]t\s*m[o|ỏ]i\b'
serious_symptom = r'\bkh[o|ó]\s*th[o|ơ|ở]|t[ư|ứ|ú]c\s*ng[ư|ự|u]c|m[â|ấ|a]t\s*kh[a|ả]\s*n[a|ă][|n]g\b'
rare_symptom = r'\b[d|đ]au\s*(h[o|ọ][|n]g|nh[ứ|ư|u]c)|ti[e|ê|]u\s*ch[a|ả]y|m[a|ấ|â]t\s*v[i|ị]\s*gi[á|a]c|t[í|i]m\s*t[a|á]i|n[ô|ổ|o]i\s*m[â|ẩ|a]n\b'

