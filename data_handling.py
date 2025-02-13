import pandas as pd


def params_from_excel(path):
    # Grab data from Excel sheet.
    data = pd.read_excel(path, index_col='Parameter')
    m1 = data.iloc[0]['Value']
    m2 = data.iloc[1]['Value']
    k1 = data.iloc[2]['Value']
    c1 = data.iloc[3]['Value']
    k2 = data.iloc[4]['Value']

    return m1, m2, k1, c1, k2


def write_to_excel(path, t, sprung_disp, unsprung_disp):
    data = pd.DataFrame(columns=['Road Displacement (m)', 'Unsprung Mass Displacement (m)',
                                 'Sprung Mass Displacement (m)'])
    data['Road Displacement (m)'] = t
    data['Unsprung Mass Displacement (m)'] = unsprung_disp
    data['Sprung Mass Displacement (m)'] = sprung_disp

    data.to_excel(path)
