import pandas as pd
from openpyxl import load_workbook
import re
from mplsoccer import PyPizza, add_image, FontManager
import matplotlib.pyplot as plt
import streamlit as st 
####################################
st.set_page_config(
    page_title= 'Pizza Charts - Egyptian League 23/24',
    layout='centered',
    page_icon= '🍕'
)

st.title('Pizza Charts - Egyptian League 23/24')
st.subheader('Choose the team name and the player name')

#st.sidebar.success('Player Pizza Charts')


player_season_stats_percentiles = pd.read_excel(r"Egyptian League 23-24 Player Season Stats.xlsx")
#print (df.head())
##########################################################################
split_team_names = player_season_stats_percentiles['team_name'].str.split(', ')

# Flatten the lists into a single list
flattened_team_names = [team for sublist in split_team_names for team in sublist]

# Get unique values and sort them
teams_names = sorted(set(flattened_team_names))

#print(teams_names)
############# VARIABLES ########
# Streamlit selectbox for team
team_name_var = st.selectbox('Select a team : ', teams_names, index=0) # Default value to be the first value


# Filter the DataFrame based on the selected team
filtered_df = player_season_stats_percentiles[player_season_stats_percentiles['team_name'].str.contains(team_name_var, na=False)]
    
# Streamlit selectbox for player
player_name_var = st.selectbox('Select a player : ',    
                                filtered_df['match_name'].sort_values().unique(), 
                                index=0) #default value is the first value


#IN CASE I WANT TO SHOW THE PLAYER NAME SELECT BOX ONLYYYY AFTER SELEECTING A TEAM 

# Streamlit selectbox for team
#team_name_var = st.selectbox('Select a team : ', teams_names, index=None)

# Ensure team_name_var is not None and is a valid string
#if team_name_var:
#    # Filter the DataFrame based on the selected team
#    filtered_df = player_season_stats_percentiles[player_season_stats_percentiles['team_name'].str.contains(team_name_var, na=False)]
    
#    # Streamlit selectbox for player
#    player_name_var = st.selectbox('Select a player : ', 
#                                   filtered_df['match_name'].sort_values().unique(), 
#                                   index=None)
#else:
#    st.write("Please select a valid team.")



# GET POISTION GROUP

# Filter by player name and team name (using str.contains for the team name)
position_group = list(player_season_stats_percentiles[
    (player_season_stats_percentiles['match_name'] == player_name_var) &
    (player_season_stats_percentiles['team_name'].str.contains(team_name_var, na=False))
]['PositionGroup'].reset_index(drop=True))

# If there are results, get the first one
position_group = position_group[0] if position_group else None
print(position_group)


# Define params for each position group
position_group_params = {
    'Goalkeepers': ['GK Successful Distribution p90 Percentile','Successful Launches p90 Percentile'
                    , 'Clean Sheets p90 Percentile', 'Goals Conceded p90 Percentile', 'Goals Conceded Inside Box p90 Percentile',
                    'Penalties Saved p90 Percentile','Catches p90 Percentile', 'Punches p90 Percentile','Saves Made p90 Percentile'
                    ,'Saves Made from Inside Box p90 Percentile'],
    
    'Full Backs': ['Goal Assists p90 Percentile','Chances Created p90 Percentile', 'Successful Crosses open play p90 Percentile', 
                    'ProgressivePasses p90 Percentile', 'FinalThirdPasses p90 Percentile',
                   'Tackles Won p90 Percentile','Total Clearances p90 Percentile', 'Interceptions p90 Percentile','Recoveries p90 Percentile', 'Duels won % p90 Percentile',
                     'Total Fouls Won p90 Percentile'],
    
    'Center Backs':['Total Clearances p90 Percentile', 'Interceptions p90 Percentile','Recoveries p90 Percentile','Tackles Won p90 Percentile',
                      'Aerial Duels won p90 Percentile','Ground Duels won p90 Percentile',
                      'Clean Sheets p90 Percentile', 'Goals Conceded p90 Percentile','Goals Conceded Inside Box p90 Percentile',
                      'Open Play Pass Success % p90 Percentile', 'ProgressivePasses p90 Percentile', 'FinalThirdPasses p90 Percentile'],
    
    'Midfielders': ['Goals p90 Percentile', 'Goal Assists p90 Percentile','Open Play Pass Success % p90 Percentile', 'Through balls p90 Percentile',
                    'FinalThirdPasses p90 Percentile', 'ProgressivePasses p90 Percentile', 'Chances Created p90 Percentile',
                    'Touches p90 Percentile','Dribbles success % p90 Percentile','Dispossessed p90 Percentile', 'Duels won % p90 Percentile',
                      'Tackles Won p90 Percentile','Recoveries p90 Percentile', 'Times Tackled p90 Percentile'],
    
    'Wingers': ['Goals p90 Percentile', 'Goal Assists p90 Percentile','Chances Created p90 Percentile', 'Successful Crosses open play p90 Percentile',
                'ProgressivePasses p90 Percentile', 'FinalThirdPasses p90 Percentile',
                'Touches p90 Percentile','Total Touches In Opposition Box p90 Percentile', 'Dribbles success % p90 Percentile', 'Overruns p90 Percentile','Dispossessed p90 Percentile','Total Fouls Won p90 Percentile'],
    
    'Strikers': ['Goals p90 Percentile','Headed Goals p90 Percentile', 'Goal Assists p90 Percentile','Successful Lay-offs p90 Percentile','Chances Created p90 Percentile',
                 'ProgressivePasses p90 Percentile',
                  'Total Shots p90 Percentile','Shots On Target ( inc goals ) p90 Percentile', 'Shots Per Goal p90 Percentile','Conversion Rate p90 Percentile'
                 'Total Touches In Opposition Box p90 Percentile',  
                  'Aerial Duels won p90 Percentile','Ground Duels won p90 Percentile','Offsides p90 Percentile']
}

params = position_group_params[position_group]
#print(params)

##################################################

# Filter for the player and check if the team_name is in the 'team_name' column
values = player_season_stats_percentiles[
    (player_season_stats_percentiles['match_name'] == player_name_var) &
    (player_season_stats_percentiles['team_name'].str.contains(team_name_var, na=False))
][params].reset_index(drop=True)

#values
#################################################################

#GET TEAM NAME 
team_name_viz=player_season_stats_percentiles[((player_season_stats_percentiles['team_name'].str.contains(team_name_var, na=False)) == True) & 
(player_season_stats_percentiles['match_name'] == player_name_var)] ['team_name']

team_name_viz= list(team_name_viz)
team_name_viz= team_name_viz[0].replace(', ', ' / ')
#team_name_viz
############################################################
#CONVERT VALUES INTO INTEGER
values = list(player_season_stats_percentiles[
    (player_season_stats_percentiles['match_name'] == player_name_var) &
    (player_season_stats_percentiles['team_name'].str.contains(team_name_var, na=False))
][params].values.flatten().astype(int))

############################################################
#REMOVE THE P90 FORM THE STAT NAME
params = [param.replace(' p90 Percentile', '') for param in params]

############################################################
# CHANGE THE FORMAT 
d=[]
for word in params:
   s=re.sub( r"([A-Z])", r" \1", word).split()
   d.append(' '.join(s))
params=d


#params
############################################################
# instantiate PyPizza class
# FontManager for custom font
font_normal = FontManager('https://raw.githubusercontent.com/googlefonts/roboto/main/'
                          'src/hinted/Roboto-Regular.ttf')

# Create a full pizza chart without segment lines
baker = PyPizza(
    params=params,                  # Multiple statistics
    background_color="#0e1117",     # Background color
    straight_line_color="#F2F2F2",  # Match the background to hide straight lines
    straight_line_lw=1,             # Set linewidth for straight lines to 0 (invisible)
    last_circle_color="#F2F2F2",    # Color for the last circle line
    last_circle_lw=1.5,               # Linewidth for the outermost circle
    other_circle_lw=1,              # No lines between circles
    inner_circle_size=5            # Size of inner circle
)

# Plot the pizza
fig, ax = baker.make_pizza(
    values,                          # List of values
    figsize=(10, 10.5),                # Adjust the figsize according to your need
    color_blank_space="same",        # Fill blank space with the same color
    slice_colors=['#1A78CF']*len(values),  # Uniform color for the slices (to make it look cohesive)
    value_colors=['#F2F2F2']*len(values),  # Color for the value text
    value_bck_colors=['#1A78CF']*len(values),  # Color for value background
    blank_alpha=0.4,                 # Alpha for blank-space colors
    kwargs_slices=dict(
        edgecolor="#F2F2F2", zorder=2, linewidth=1  # Set linewidth to 0 to avoid slice lines
    ),                               # Values to be used when plotting slices
    kwargs_params=dict(
        color="#F2F2F2", fontsize=14,
        fontproperties=font_normal.prop, va="center"
    ),                               # Values for parameter labels
    kwargs_values=dict(
        color="#F2F2F2", fontsize=14,
        fontproperties=font_normal.prop, zorder=3,
        bbox=dict(
            edgecolor="#F2F2F2", facecolor="cornflowerblue",
            boxstyle="round,pad=0.1", lw=1
        )
    )                                # Values for the actual stat numbers
)
# add title
fig.text(
    0.515, 0.97, f'{player_name_var} - {team_name_viz}', size=20,
    ha="center", color="#F2F2F2"
)

# add subtitle
fig.text(
    0.515, 0.942,
    f'Per 90 Percentile Rank vs {position_group} | 23/24',
    size=15,
    ha="center", color="#F2F2F2"
)

# add credits
notes = 'Players only with minimum 10 90s (900 Mins)'
CREDIT_1 = "Data: Opta"
CREDIT_2 = "Inspired by: McKay Johns"

fig.text(
    0.99, 0.005, f"{notes}\n{CREDIT_1}\n{CREDIT_2}", size=14,
    color="#F2F2F2",
    ha="right"
)

fig.text(
    0.03, 0.005, "Twitter : \nAfrican Football Analytics", size=14,
    color="#F2F2F2",
    ha="left"
)
# Display the pizza chart in Streamlit
st.pyplot(fig)

with st.expander("Metric Glossary"):
    st.write("""
    This is the glossary for all the metrics used in this analysis. Each metric is explained in detail below:

    - **Overrun**: Heavy touch in a dribble.
    - **Progressive Passes**: A pass that moves the ball closer to the opponent goal by 25% & at least 5 m vertically.
    - **Second Assist** : The last action of a player from the goalscoring team, prior to an Assist by a teammate.
    - **Lay-off** : A pass by a striker who has received the ball with his back to goal and is played back towards team-mates.
    - **Dispossessed** : Player is dispossessed on the ball by an opponent – no dribble involved.
    - **GK Distribution** : Actions where the goalkeeper successfully distributes the ball to a teammate.
    - **GK Launches**  : long balls launched forward into an area of the pitch rather than to a specific team-mate.
    - **Other Goals** : Goals scored using any body part other than the right foot, left foot, or the head. 
    """)