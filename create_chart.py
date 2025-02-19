import sys
import pandas as pd

# To be used independently of main.py

# positions = {'1b', 'first base', '2b', 'second base', '3b', 'third base', 'ss', 'shortstop', 'lf','left field', 'left side', 'cf', 'center field', 'up the middle', 'rf', 'right field', 'right side', 'p', 'pitcher', 'c', 'catcher'}

def create_chart():
    team = sys.argv[1]
    first_name = sys.argv[2]
    last_name = sys.argv[3]

    # read in data from csv files
    df = pd.read_csv(f'spray_charts/{team}/{first_name}_{last_name}.csv')
    first = df.loc[df['Positions'] == '1b', '#'].values[0] + df.loc[df['Positions'] == 'first base', '#'].values[0]
    second = df.loc[df['Positions'] == '2b', '#'].values[0] + df.loc[df['Positions'] == 'second base', '#'].values[0]
    third = df.loc[df['Positions'] == '3b', '#'].values[0] + df.loc[df['Positions'] == 'third base', '#'].values[0]
    ss = df.loc[df['Positions'] == 'ss', '#'].values[0] + df.loc[df['Positions'] == 'shortstop', '#'].values[0]
    lf = df.loc[df['Positions'] == 'lf', '#'].values[0] + df.loc[df['Positions'] == 'left field', '#'].values[0] + df.loc[df['Positions'] == 'left side', '#'].values[0]
    cf = df.loc[df['Positions'] == 'cf', '#'].values[0] + df.loc[df['Positions'] == 'center field', '#'].values[0] + df.loc[df['Positions'] == 'up the middle', '#'].values[0]
    rf = df.loc[df['Positions'] == 'rf', '#'].values[0] + df.loc[df['Positions'] == 'right field', '#'].values[0] + df.loc[df['Positions'] == 'right side', '#'].values[0]
    pitcher = df.loc[df['Positions'] == 'p', '#'].values[0] + df.loc[df['Positions'] == 'pitcher', '#'].values[0]
    catcher = df.loc[df['Positions'] == 'c', '#'].values[0] + df.loc[df['Positions'] == 'catcher', '#'].values[0]

    print(first_name, last_name)
    print("1B: ", first)
    print("2B: ", second)
    print("3B: ", third)
    print("SS: ", ss)
    print("LF: ", lf)
    print("CF: ", cf)
    print("RF: ", rf)
    print("P: ", pitcher)
    print("C: ", catcher)



if __name__ == "__main__":
    create_chart()