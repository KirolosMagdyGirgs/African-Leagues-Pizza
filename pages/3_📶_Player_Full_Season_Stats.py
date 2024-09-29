import pandas as pd
import streamlit as st

st.set_page_config(
    page_title= 'Player Full Season Stats - Egyptian League 23/24',
    layout='wide',
    page_icon= '📶'
)

st.title('Player Full Season Stats - Egyptian League 23/24')

# Load the Excel file
player_full_season_stats_percentiles_df = pd.read_excel(r"Egyptian League 23-24 Player full Season Stats.xlsx")

# Split and flatten position groups
split_position_groups = player_full_season_stats_percentiles_df['Position Group'].str.split(', ')
flattened_position_groups = [team for sublist in split_position_groups for team in sublist]
position_groups = sorted(set(flattened_position_groups))

# Streamlit selectbox for position group
position_group_var = st.selectbox('Select a position:', position_groups, index=0)
player_full_season_stats_percentiles_df = player_full_season_stats_percentiles_df[player_full_season_stats_percentiles_df['Position Group'] == position_group_var]

# Define the columns that contain 'Percentile'
percentile_columns = [col for col in player_full_season_stats_percentiles_df.columns if 'Percentile' in col]

# Define the columns that doens't have Percentile' and add the '90s' column
full_columns = [col for col in player_full_season_stats_percentiles_df.columns if  'Percentile' not in col]
# Add '90s' column explicitly for formatting
full_columns.append('90s')



# Apply the gradient color formatting using pandas' background_gradient
styled_df = player_full_season_stats_percentiles_df.style.background_gradient(
    subset=percentile_columns, cmap='RdYlGn'  # Red to Yellow to Green gradient
).format(
   subset=['90s'], formatter="{:.2f}"  # Format only numeric columns with 2 decimal places
)

# Display the styled DataFrame in Streamlit
st.dataframe(styled_df)

##, height=750   add this to increase the height in the page

with st.expander("Metric Glossary"):
    st.write("""
    This is the glossary for some of the metrics used in this analysis:

    - **Overrun**: Heavy touch in a dribble.
    - **Progressive Passes**: A pass that moves the ball closer to the opponent goal by 25% & at least 5 m vertically.
    - **Second Assist** : The last action of a player from the goalscoring team, prior to an Assist by a teammate.
    - **Lay-off** : A pass by a striker who has received the ball with his back to goal and is played back towards team-mates.
    - **Dispossessed** : Player is dispossessed on the ball by an opponent – no dribble involved.
    - **GK Distribution** : Actions where the goalkeeper successfully distributes the ball to a teammate.
    - **GK Launches**  : long balls launched forward into an area of the pitch rather than to a specific team-mate.
    - **Other Goals** : Goals scored using any body part other than the right foot, left foot, or the head. 
    """)
