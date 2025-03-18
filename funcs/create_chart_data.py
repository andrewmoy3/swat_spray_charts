import pandas as pd
import string

positions = {'1b', 'first base', '2b', 'second base', '3b', 'third base', 'ss', 'shortstop', 'lf','left field', 'left side', 'left center', 'cf', 'center field', 'up the middle', 'rf', 'right field', 'right side', 'right center', 'p', 'pitcher', 'c', 'catcher'}
def create_chart_data(plays, team, first_name, last_name):
    spray_chart = {pos: {'hit': 0, 'out': 0, 'misc': 0} for pos in positions}
    if not plays.empty:
        plays.to_csv('test.csv')
        for play in plays:
            pos = ball_hit_to(play)
            if pos:
                type = type_of_play(play)
                if type:
                    # print(play, ":", type)
                    spray_chart[pos][type] += 1
                else:
                    spray_chart[pos]["misc"] += 1
                
    ## write spray chart to csv
    if sum(sum(inner_dict.values()) for inner_dict in spray_chart.values())> 50:
        print(first_name, last_name, sum(sum(inner_dict.values()) for inner_dict in spray_chart.values()))
    # df = pd.DataFrame.from_dict(spray_chart, orient='index', columns=['#'])
    df = pd.DataFrame.from_dict(spray_chart, orient='index')
    # df.index.name = "Positions"
    df = df.reset_index().rename(columns={"index": "Category"})
    # df = df.reset_index()
    if sum(sum(inner_dict.values()) for inner_dict in spray_chart.values()) > 10:
        df.to_csv(f'spray_charts/{team}/{first_name}_{last_name}.csv', index=False)

# Find where the ball is hit to by returning first position found in string
def ball_hit_to(play):
    play = play.replace(",", "").split(';')[0]
    tokens = play.translate(str.maketrans("", "", string.punctuation)).split()
    if tokens[0] == 'to' or tokens[0] == 'advanced' or tokens[0] == 'walked' or tokens[0] == 'stole' or tokens[0] == 'pinch':
        return None
    if len(tokens) > 1:
        two_word = tokens[0] + tokens[1] 
        if two_word == 'struckout' or two_word == 'outat' or two_word == 'caughtstealing':
            return None
    if len(tokens) > 2 and tokens[0] + tokens[1] + tokens[2] == 'hitbypitch':
        return None
    
    for i in range(len(tokens)):
        word = tokens[i].lower()
        if i > 0:
            two_word = (tokens[i-1] + ' ' + tokens[i]).lower()
        else:
            two_word = None  
        if i > 1:
            three_word = (tokens[i-2] + ' ' + tokens[i-1] + ' ' + tokens[i]).lower()
        else:
            three_word = None  
        
        for pos in positions:
            if pos == word or pos == two_word or pos == three_word:
                return pos

hits = ['singled', 'doubled', 'tripled', 'homered']
outs = ['flied', 'grounded', 'lined', 'fouled', 'popped', ]
misc = ['error', 'fielder\'s']
def type_of_play(play):
    play = play.replace(",", "").split(';')[0]
    tokens = play.translate(str.maketrans("", "", string.punctuation)).split()
    for hit in hits:
        if hit in tokens:
            return 'hit'
    for out in outs:
        if out in tokens:
            return 'out'
    for m in misc:
        if m in tokens:
            return 'misc'
        
