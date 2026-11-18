import pandas as pd
import numpy as np

def build_relational_pressure_system(pressure_cutoff=60, knockout_only=False):
    df = pd.read_csv("ball_by_ball.csv")
    matches = pd.read_csv("matches.csv")
    comps = pd.read_csv("competitions.csv")
    p11 = pd.read_csv("playing_eleven.csv")
    mapping = pd.read_csv("competition_team_player_mapping.csv")
    teams = pd.read_csv("teams.csv")

    df['overid'] = pd.to_numeric(df['overid'], errors='coerce')
    df['runs'] = pd.to_numeric(df['runs'], errors='coerce').fillna(0)
    df['is_wicket'] = df['is_wicket'].astype(str).str.strip().str.lower() == 'true'
    df = df.dropna(subset=['overid', 'striker_name', 'bowler_name']).copy()

    matches['knock_out_flag'] = matches['knock_out'].astype(str).str.strip().str.lower() == 'true'
    match_meta = matches[['match_id', 'comp_id', 'stage', 'knock_out_flag', 'venue_country']].merge(
        comps[['comp_id', 'comp_name', 'match_format', 'season']], on='comp_id', how='left'
    )
    df = df.merge(match_meta, on='match_id', how='left')

    if knockout_only:
        df = df[df['knock_out_flag']].copy()

    inn_col = next((c for c in ['innings', 'inning', 'innings_id'] if c in df.columns), None)

    if inn_col:
        df = df.sort_values(['match_id', inn_col, 'overid']).reset_index(drop=True)
        grp = df.groupby(['match_id', inn_col])

        df['ball_num'] = grp.cumcount() + 1
        df['balls_remaining'] = (120 - df['ball_num'] + 1).clip(lower=1)
        df['cum_runs'] = grp['runs'].cumsum() - df['runs']
        df['wickets_fallen'] = grp['is_wicket'].cumsum() - df['is_wicket'].astype(int)

        inn_totals = df.groupby(['match_id', inn_col])['runs'].sum().reset_index()
        first_inn = inn_totals[inn_totals[inn_col] == 1][['match_id', 'runs']].rename(columns={'runs': 'target'})
        first_inn['target'] = first_inn['target'] + 1
        df = df.merge(first_inn, on='match_id', how='left')

        is_chase = df[inn_col] == 2
        runs_needed = (df['target'] - df['cum_runs']).clip(lower=0)
        rrr = np.where(is_chase, (runs_needed / df['balls_remaining']) * 6, np.nan)
        crr = (df['cum_runs'] / df['ball_num'].clip(lower=1)) * 6

        chase_urgency = np.clip((rrr - 6.0) * 5.0, 0, 40)
        set_urgency = np.where(
            df['overid'] >= 16, 22 + (df['overid'] - 15) * 3.6,
            np.where((df['overid'] <= 6) & (df['wickets_fallen'] >= 2), 28, (df['overid'] / 20.0) * 18)
        )
        urgency_score = np.where(is_chase, chase_urgency, set_urgency)

        wicket_score = np.clip((df['wickets_fallen'] / 8.0) * 35.0, 0, 35)

        chase_closeness = np.where(
            (rrr >= 8.0) & (rrr <= 15.5), 25 - np.abs(rrr - 11.5) * 3.5,
            np.where(rrr > 15.5, 8, 5)
        ).clip(0, 25)
        set_closeness = np.where((df['wickets_fallen'] >= 4) & (crr < 7.0), 22, 10)
        closeness_score = np.where(is_chase, chase_closeness, set_closeness)

        ko_bonus = np.where(df['knock_out_flag'].fillna(False), 10.0, 0.0)
        df['MPI'] = (urgency_score + wicket_score + closeness_score + ko_bonus).clip(0, 100).round(1)
    else:
        df['MPI'] = np.where(df['overid'] >= 16, 75.0, 35.0)

    df['Situation'] = np.where(df['MPI'] >= pressure_cutoff, 'High Pressure', 'Ordinary')

    p11['batting_order'] = pd.to_numeric(p11['batting_order'], errors='coerce')
    p11['is_wk_flag'] = p11['is_wk'].astype(str).str.strip().str.lower() == 'true'

    player_roles = p11.groupby('player_id', as_index=False).agg(
        Avg_Order=('batting_order', 'mean'),
        Is_WK=('is_wk_flag', 'any')
    )

    def label_position(row):
        if row['Is_WK']:
            return "Wicketkeeper"
        if pd.isna(row['Avg_Order']):
            return "All-Round / Bowler"
        if row['Avg_Order'] <= 3.5:
            return "Top Order (1-3)"
        if row['Avg_Order'] <= 5.5:
            return "Middle Order (4-5)"
        return "Finisher / Lower (6+)"

    player_roles['Role Profile'] = player_roles.apply(label_position, axis=1)

    map_enriched = mapping.merge(
        teams[['comp_id', 'team_id', 'team_name']],
        on=['comp_id', 'team_id'], how='left', suffixes=('', '_ref')
    )
    map_enriched['Team'] = map_enriched['team_name'].fillna(map_enriched.get('team_name_ref', 'Unknown'))

    def get_primary_team(series):
        s = series.dropna()
        if s.empty:
            return "Unknown"
        m = s.mode()
        return str(m.iloc[0]) if not m.empty else str(s.iloc[0])

    player_meta = map_enriched.groupby('player_name', as_index=False).agg(
        player_id=('player_id', 'first'),
        Primary_Team=('Team', get_primary_team),
        Competitions=('comp_name', lambda x: ', '.join(sorted(set(x.dropna()))[:2]))
    ).merge(player_roles[['player_id', 'Role Profile']], on='player_id', how='left')
    player_meta['Role Profile'] = player_meta['Role Profile'].fillna("Specialist")

    regime_summary = df.groupby('Situation', as_index=False).agg(
        Deliveries=('runs', 'count'),
        Avg_MPI=('MPI', 'mean'),
        Avg_Runs=('runs', 'mean'),
        Wicket_Rate_Pct=('is_wicket', lambda x: x.mean() * 100)
    )
    regime_summary['Share (%)'] = ((regime_summary['Deliveries'] / max(len(df), 1)) * 100).round(1)
    regime_summary['Avg_MPI'] = regime_summary['Avg_MPI'].round(1)
    regime_summary['Run Rate'] = (regime_summary['Avg_Runs'] * 6).round(2)
    regime_summary['Wicket_Rate_Pct'] = regime_summary['Wicket_Rate_Pct'].round(2)

    ord_bat = df[df['Situation'] == 'Ordinary'].groupby('striker_name', as_index=False).agg(
        Ord_Runs=('runs', 'sum'), Ord_Balls=('runs', 'count')
    )
    ord_bat = ord_bat[ord_bat['Ord_Balls'] >= 15]
    ord_bat['Ordinary SR'] = (ord_bat['Ord_Runs'] / ord_bat['Ord_Balls']) * 100

    hi_bat = df[df['Situation'] == 'High Pressure'].groupby('striker_name', as_index=False).agg(
        Pressure_Runs=('runs', 'sum'),
        Pressure_Balls=('runs', 'count'),
        Matches=('match_id', 'nunique')
    )
    hi_bat = hi_bat[hi_bat['Pressure_Balls'] >= 10]
    hi_bat['Pressure SR'] = (hi_bat['Pressure_Runs'] / hi_bat['Pressure_Balls']) * 100

    m_bat = df[df['Situation'] == 'High Pressure'].groupby(['striker_name', 'match_id'], as_index=False).agg(
        mr=('runs', 'sum'), mb=('runs', 'count')
    )
    m_bat['msr'] = (m_bat['mr'] / m_bat['mb']) * 100
    bat_std = m_bat.groupby('striker_name', as_index=False)['msr'].std().fillna(45)
    bat_std['Consistency'] = (100 / (1 + (bat_std['msr'] / 100))).round(1)

    bat_df = ord_bat.merge(hi_bat, on='striker_name').merge(bat_std[['striker_name', 'Consistency']], on='striker_name')
    bat_df = bat_df.merge(player_meta, left_on='striker_name', right_on='player_name', how='left')
    bat_df['SR Lift'] = (bat_df['Pressure SR'] - bat_df['Ordinary SR']).round(1)
    bat_df['Ordinary SR'] = bat_df['Ordinary SR'].round(1)
    bat_df['Pressure SR'] = bat_df['Pressure SR'].round(1)
    bat_df['Clutch Rating'] = (
        (bat_df['Pressure SR'] * 0.45) +
        (bat_df['SR Lift'].clip(lower=-40) * 0.35) +
        (bat_df['Consistency'] * 0.20)
    ).round(1)

    bat_df = bat_df.rename(columns={'striker_name': 'Player Name', 'Primary_Team': 'Team'})[
        ['Player Name', 'Team', 'Role Profile', 'Competitions', 'Matches', 'Ordinary SR', 'Pressure SR', 'SR Lift', 'Consistency', 'Clutch Rating']
    ].sort_values('Clutch Rating', ascending=False).reset_index(drop=True)

    ord_bowl = df[df['Situation'] == 'Ordinary'].groupby('bowler_name', as_index=False).agg(
        Ord_Runs=('runs', 'sum'), Ord_Balls=('runs', 'count')
    )
    ord_bowl = ord_bowl[ord_bowl['Ord_Balls'] >= 18]
    ord_bowl['Ordinary Econ'] = (ord_bowl['Ord_Runs'] / ord_bowl['Ord_Balls']) * 6

    hi_bowl = df[df['Situation'] == 'High Pressure'].groupby('bowler_name', as_index=False).agg(
        Pressure_Runs=('runs', 'sum'),
        Pressure_Balls=('runs', 'count'),
        Wickets=('is_wicket', 'sum'),
        Matches=('match_id', 'nunique')
    )
    hi_bowl = hi_bowl[hi_bowl['Pressure_Balls'] >= 12]
    hi_bowl['Pressure Econ'] = (hi_bowl['Pressure_Runs'] / hi_bowl['Pressure_Balls']) * 6
    hi_bowl['Wkts_Per_Over'] = hi_bowl['Wickets'] / (hi_bowl['Pressure_Balls'] / 6)

    m_bowl = df[df['Situation'] == 'High Pressure'].groupby(['bowler_name', 'match_id'], as_index=False).agg(
        mr=('runs', 'sum'), mb=('runs', 'count')
    )
    m_bowl['mecon'] = (m_bowl['mr'] / m_bowl['mb']) * 6
    bowl_std = m_bowl.groupby('bowler_name', as_index=False)['mecon'].std().fillna(3.5)
    bowl_std['Consistency'] = (100 / (1 + (bowl_std['mecon'] / 6))).round(1)

    bowl_df = ord_bowl.merge(hi_bowl, on='bowler_name').merge(bowl_std[['bowler_name', 'Consistency']], on='bowler_name')
    bowl_df = bowl_df.merge(player_meta, left_on='bowler_name', right_on='player_name', how='left')
    bowl_df['Econ Saved'] = (bowl_df['Ordinary Econ'] - bowl_df['Pressure Econ']).round(2)
    bowl_df['Ordinary Econ'] = bowl_df['Ordinary Econ'].round(2)
    bowl_df['Pressure Econ'] = bowl_df['Pressure Econ'].round(2)
    bowl_df['Clutch Rating'] = (
        ((12 - bowl_df['Pressure Econ']).clip(lower=0) * 6) +
        (bowl_df['Wkts_Per_Over'] * 18) +
        (bowl_df['Econ Saved'] * 5) +
        (bowl_df['Consistency'] * 0.25)
    ).round(1)

    bowl_df = bowl_df.rename(columns={'bowler_name': 'Player Name', 'Primary_Team': 'Team'})[
        ['Player Name', 'Team', 'Competitions', 'Matches', 'Ordinary Econ', 'Pressure Econ', 'Econ Saved', 'Wickets', 'Consistency', 'Clutch Rating']
    ].sort_values('Clutch Rating', ascending=False).reset_index(drop=True)

    return df, regime_summary, bat_df, bowl_df
