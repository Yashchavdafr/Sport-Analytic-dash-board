import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Load your IPL data
script = Path(__file__).parent.parent
data_path = script / "data" / "ipl_2024_deliveries.csv"
ipl_data = pd.read_csv(data_path)

# Fixing match_id extraction
ipl_data['match_id'] = ipl_data['match_id'].astype(str).str[-2:-1]

st.title("IPL 2024 Analysis")
tab1, tab2, tab3 = st.tabs(["Overall Analysis", "Team Wise Analysis", "Player Wise Analysis"])

with tab1:
    overall_tab = st.container()

    top_teams_avg_runs_per_over = ipl_data.groupby('batting_team')['total_runs'].sum().reset_index()
    top_teams_avg_runs_per_over['overs'] = ipl_data.groupby('batting_team')['match_id'].count().reset_index(name='overs')['overs']
    top_teams_avg_runs_per_over['avg_runs_per_over'] = top_teams_avg_runs_per_over['total_runs'] / top_teams_avg_runs_per_over['overs']
    top_teams_avg_runs_per_over = top_teams_avg_runs_per_over.nlargest(5, 'avg_runs_per_over')
    overall_tab.write(px.bar(top_teams_avg_runs_per_over, x='batting_team', y='avg_runs_per_over', title='Top 5 Teams by Average Runs per Over'))

    top_teams_strike_rate = ipl_data.groupby('batting_team')['striker'].count().reset_index(name='balls_faced')
    top_teams_strike_rate['strike_rate'] = (ipl_data.groupby('batting_team')['total_runs'].sum().reset_index(name='runs')['runs'] / top_teams_strike_rate['balls_faced']) * 100
    top_teams_strike_rate = top_teams_strike_rate.nlargest(5, 'strike_rate')
    overall_tab.write(px.bar(top_teams_strike_rate, x='batting_team', y='strike_rate', title='Top 5 Teams by Strike Rate'))

    top_teams_economy_rate = ipl_data.groupby('bowling_team')['total_runs'].sum().reset_index()
    top_teams_economy_rate['overs'] = ipl_data.groupby('bowling_team')['match_id'].count().reset_index(name='overs')['overs']
    top_teams_economy_rate['economy_rate'] = top_teams_economy_rate['total_runs'] / top_teams_economy_rate['overs']
    top_teams_economy_rate = top_teams_economy_rate.nsmallest(5, 'economy_rate')
    overall_tab.write(px.bar(top_teams_economy_rate, x='bowling_team', y='economy_rate', title='Top 5 Teams by Economy Rate'))

    top_teams_avg_wickets_per_over = ipl_data.groupby('bowling_team')['wicket_type'].count().reset_index(name='wickets')
    top_teams_avg_wickets_per_over['overs'] = ipl_data.groupby('bowling_team')['match_id'].count().reset_index(name='overs')['overs']
    top_teams_avg_wickets_per_over['avg_wickets_per_over'] = top_teams_avg_wickets_per_over['wickets'] / top_teams_avg_wickets_per_over['overs']
    top_teams_avg_wickets_per_over = top_teams_avg_wickets_per_over.nlargest(5, 'avg_wickets_per_over')
    overall_tab.write(px.bar(top_teams_avg_wickets_per_over, x='bowling_team', y='avg_wickets_per_over', title='Top 5 Teams by Average Wickets per Over'))

    top_batsmen_runs = ipl_data.groupby('striker')['total_runs'].sum().reset_index()
    top_batsmen_runs = top_batsmen_runs.nlargest(5, 'total_runs')
    overall_tab.write(px.bar(top_batsmen_runs, x='striker', y='total_runs', title='Top 5 Batsmen by Runs'))

    top_bowlers_wickets = ipl_data[ipl_data['wicket_type'].notnull()].groupby('bowler')['wicket_type'].count().reset_index(name='wickets')
    top_bowlers_wickets = top_bowlers_wickets.nlargest(5, 'wickets')
    overall_tab.write(px.bar(top_bowlers_wickets, x='bowler', y='wickets', title='Top 5 Bowlers by Wickets'))

    top_fielders_catches = ipl_data[~ipl_data['fielder'].isnull()].groupby('fielder')['fielder'].count().reset_index(name='catches')
    top_fielders_catches = top_fielders_catches.nlargest(5, 'catches')
    overall_tab.write(px.bar(top_fielders_catches, x='fielder', y='catches', title='Top 5 Fielders by Catches'))

    top_teams_wins = ipl_data.groupby('batting_team')['match_id'].count().reset_index(name='wins')
    top_teams_wins = top_teams_wins.nlargest(5, 'wins')
    overall_tab.write(px.bar(top_teams_wins, x='batting_team', y='wins', title='Top 5 Teams by Total Wins'))

with tab2:
    team_tab = st.container()

    selected_team = team_tab.selectbox("Select a team", ipl_data['batting_team'].unique())

    team_data = ipl_data[ipl_data['batting_team'] == selected_team]

    team_image = team_tab.image(f"{script}/assets/teams/{selected_team.lower().replace(' ', '_')}_logo.png", width=200)

    team_runs = team_data.groupby('match_id')['total_runs'].sum().reset_index()
    team_tab.write(px.bar(team_runs, x='match_id', y='total_runs', title=f'{selected_team} Performance'))

    team_wickets = team_data[team_data['wicket_type'].notnull()].groupby('match_id')['wicket_type'].count().reset_index(name='wickets')
    team_tab.write(px.bar(team_wickets, x='match_id', y='wickets', title=f'{selected_team} Wickets'))

    team_avg_runs_per_over = team_data.groupby('match_id')['total_runs'].sum().reset_index()
    team_avg_runs_per_over['overs'] = team_data.groupby('match_id')['match_id'].count().reset_index(name='overs')['overs']
    team_avg_runs_per_over['avg_runs_per_over'] = team_avg_runs_per_over['total_runs'] / team_avg_runs_per_over['overs']
    team_tab.write(px.line(team_avg_runs_per_over, x='match_id', y='avg_runs_per_over', title=f'{selected_team} Average Runs per Over'))

    team_top_scorers = team_data.groupby('striker')['total_runs'].sum().reset_index()
    team_top_scorers = team_top_scorers.nlargest(5, 'total_runs')
    team_tab.write(px.bar(team_top_scorers, x='striker', y='total_runs', title=f'{selected_team} Top Scorers'))

    team_top_wicket_takers = team_data[team_data['wicket_type'].notnull()].groupby('bowler')['wicket_type'].count().reset_index(name='wickets')
    team_top_wicket_takers = team_top_wicket_takers.nlargest(5, 'wickets')
    team_tab.write(px.bar(team_top_wicket_takers, x='bowler', y='wickets', title=f'{selected_team} Top Wicket Takers'))

    team_best_bowling_figures = team_data[team_data['wicket_type'].notnull()].groupby('bowler')['wicket_type'].count().reset_index(name='wickets')
    team_best_bowling_figures = team_best_bowling_figures.nlargest(5, 'wickets')
    team_tab.write(px.bar(team_best_bowling_figures, x='bowler', y='wickets', title=f'{selected_team} Best Bowling Figures'))

    team_most_valuable_players = team_data.groupby('striker')['total_runs'].sum().reset_index()
    team_most_valuable_players['wickets'] = team_data[team_data['wicket_type'].notnull()].groupby('bowler')['wicket_type'].count().reset_index(name='wickets')['wickets']
    team_most_valuable_players['value'] = team_most_valuable_players['total_runs'] + team_most_valuable_players['wickets']
    team_most_valuable_players = team_most_valuable_players.nlargest(5, 'value')
    team_tab.write(px.bar(team_most_valuable_players, x='striker', y='value', title=f'{selected_team} Most Valuable Players'))

    team_economy_rate = team_data.groupby('bowler')['total_runs'].sum().reset_index()
    team_economy_rate['overs'] = team_data.groupby('bowler')['match_id'].count().reset_index(name='overs')['overs']
    team_economy_rate['economy_rate'] = team_economy_rate['total_runs'] / team_economy_rate['overs']
    team_tab.write(px.bar(team_economy_rate, x='bowler', y='economy_rate', title=f'{selected_team} Economy Rate'))

    team_strike_rate = team_data.groupby('striker')['total_runs'].sum().reset_index()
    team_strike_rate['balls_faced'] = team_data.groupby('striker')['striker'].count().reset_index(name='balls_faced')['balls_faced']
    team_strike_rate['strike_rate'] = (team_strike_rate['total_runs'] / team_strike_rate['balls_faced']) * 100
    team_tab.write(px.bar(team_strike_rate, x='striker', y='strike_rate', title=f'{selected_team} Strike Rate'))

    team_average = team_data.groupby('striker')['total_runs'].sum().reset_index()
    team_average['balls_faced'] = team_data.groupby('striker')['striker'].count().reset_index(name='balls_faced')['balls_faced']
    team_average['average'] = team_average['total_runs'] / team_average['balls_faced']
    team_tab.write(px.bar(team_average, x='striker', y='average', title=f'{selected_team} Average'))

with tab3:
    player_tab = st.container()

    selected_player = player_tab.selectbox("Select a player", ipl_data['striker'].unique())

    player_data = ipl_data[ipl_data['striker'] == selected_player]

    player_image = player_tab.image(f"{script}/assets/players/{selected_player.lower().replace(' ', '_')}_logo.png", width=200)

    player_runs = player_data.groupby('match_id')['total_runs'].sum().reset_index()
    player_tab.write(px.bar(player_runs, x='match_id', y='total_runs', title=f'{selected_player} Performance'))

    player_avg_runs_per_over = player_data.groupby('match_id')['total_runs'].sum().reset_index()
    player_avg_runs_per_over['overs'] = player_data.groupby('match_id')['match_id'].count().reset_index(name='overs')['overs']
    player_avg_runs_per_over['avg_runs_per_over'] = player_avg_runs_per_over['total_runs'] / player_avg_runs_per_over['overs']
    player_tab.write(px.line(player_avg_runs_per_over, x='match_id', y='avg_runs_per_over', title=f'{selected_player} Average Runs per Over'))

    player_strike_rate = player_data.groupby('match_id')['total_runs'].sum().reset_index()
    player_strike_rate['balls_faced'] = player_data.groupby('match_id')['striker'].count().reset_index(name='balls_faced')['balls_faced']
    player_strike_rate['strike_rate'] = (player_strike_rate['total_runs'] / player_strike_rate['balls_faced']) * 100
    player_tab.write(px.line(player_strike_rate, x='match_id', y='strike_rate', title=f'{selected_player} Strike Rate'))

    player_top_scores = player_data.groupby('match_id')['total_runs'].sum().reset_index()
    player_top_scores = player_top_scores.nlargest(5, 'total_runs')
    player_tab.write(px.bar(player_top_scores, x='match_id', y='total_runs', title=f'{selected_player} Top Scores'))

    player_best_strikes = player_data.groupby('match_id')['total_runs'].sum().reset_index()
    player_best_strikes['balls_faced'] = player_data.groupby('match_id')['striker'].count().reset_index(name='balls_faced')['balls_faced']
    player_best_strikes['strike_rate'] = (player_best_strikes['total_runs'] / player_best_strikes['balls_faced']) * 100
    player_best_strikes = player_best_strikes.nlargest(5, 'strike_rate')
    player_tab.write(px.bar(player_best_strikes, x='match_id', y='strike_rate', title=f'{selected_player} Best Strikes'))

    player_wickets = player_data[player_data['wicket_type'].notnull()].groupby('match_id')['wicket_type'].count().reset_index(name='wickets')
    player_tab.write(px.bar(player_wickets, x='match_id', y='wickets', title=f'{selected_player} Wickets'))