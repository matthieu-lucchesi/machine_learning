import pandas as pd

df = pd.read_csv("machine_learning/lol/data/2024_lol.csv")

def extract_picks(game_data, side):
    picks = (
        game_data[game_data['side'] == side]
        .sort_values('participantid')['champion']
        .dropna()
        .astype(str)
        .tolist()
    )
    # Retourne une liste de 5 picks (complète avec '' si moins de 5)
    return picks + [''] * (5 - len(picks))

def extract_bans(row):
    # Retourne une liste de 5 bans (complète avec '' si moins de 5)
    bans = [str(row[f'ban{i}']) if pd.notna(row[f'ban{i}']) else '' for i in range(1, 6)]
    return bans

rows = []
for gameid in df['gameid'].unique():
    game_data = df[df['gameid'] == gameid]

    blue = game_data[game_data['side'] == 'Blue']
    red = game_data[game_data['side'] == 'Red']

    if blue.empty or red.empty:
        continue

    blue_row = blue.iloc[0]
    red_row = red.iloc[0]

    picks_blue = extract_picks(game_data, 'Blue')
    picks_red = extract_picks(game_data, 'Red')
    bans_blue = extract_bans(blue_row)
    bans_red = extract_bans(red_row)

    rows.append({
        'gameid': gameid,
        'team_blue': blue_row['teamname'],
        'team_red': red_row['teamname'],
        'league': blue_row['league'],      # Ajout de la ligue
        'patch': blue_row['patch'],        # Ajout du patch
        'pick_blue_1': picks_blue[0],
        'pick_blue_2': picks_blue[1],
        'pick_blue_3': picks_blue[2],
        'pick_blue_4': picks_blue[3],
        'pick_blue_5': picks_blue[4],
        'pick_red_1': picks_red[0],
        'pick_red_2': picks_red[1],
        'pick_red_3': picks_red[2],
        'pick_red_4': picks_red[3],
        'pick_red_5': picks_red[4],
        'ban_blue_1': bans_blue[0],
        'ban_blue_2': bans_blue[1],
        'ban_blue_3': bans_blue[2],
        'ban_blue_4': bans_blue[3],
        'ban_blue_5': bans_blue[4],
        'ban_red_1': bans_red[0],
        'ban_red_2': bans_red[1],
        'ban_red_3': bans_red[2],
        'ban_red_4': bans_red[3],
        'ban_red_5': bans_red[4],
        'result': 0 if blue_row['result'] == 1 else 1  # 0 = Blue win, 1 = Red win
    })

df_final = pd.DataFrame(rows)
df_final.to_csv("machine_learning/lol/data/lol_pre_match_dataset.csv", index=False)
print(f"{len(df_final)} lignes exportées.")