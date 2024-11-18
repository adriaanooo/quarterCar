import pandas as pd
from math import *


def load_from_excel(path):
    # Grab data from Excel sheet.
    data = pd.read_excel(path, index_col='Parameter')
    m1 = data.iloc[0]['Value'] / 4  # Same stuff
    m2 = data.iloc[1]['Value'] + m1
    k1 = data.iloc[2]['Value']
    c1 = data.iloc[3]['Value'] * 2 * m1 * sqrt(k1 / m1)
    k2 = data.iloc[4]['Value']

    return m1, m2, k1, c1, k2


def write_to_excel(path, t, m1, m2):
    data = pd.DataFrame(columns=['Road Displacement (m)', 'Unsprung Mass Displacement (m)',
                                 'Sprung Mass Displacement (m)'])
    data['Road Displacement (m)'] = t
    data['Unsprung Mass Displacement (m)'] = m2
    data['Sprung Mass Displacement (m)'] = m1

    data.to_excel(path)