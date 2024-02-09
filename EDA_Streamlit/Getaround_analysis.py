import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Function to load data
@st.cache_data
def load_data():
    return pd.read_excel('Data/get_around_delay_analysis.xlsx')

# Load the data
df = load_data()

# We can see that the column checkout contain None values
# We will replace them by 0
df['delay_at_checkout_in_minutes'] = df['delay_at_checkout_in_minutes'].fillna(0)



# Title of the app
st.title('Getaround Delay Analysis')

# Show the raw data
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(df)
    
# Show full data
if st.checkbox('Show full data'):
    st.subheader('Full data')
    st.write(df)

# Show columns names
if st.checkbox('Show columns names'):
    st.subheader('Columns names')
    st.write(df.columns)

# Show data types
if st.checkbox('Show data types'):
    st.subheader('Data types')
    st.write(df.dtypes)
    
# Show shape of the data
if st.checkbox('Show shape of the data'):
    st.subheader('Shape of the data')
    st.write(df.shape)

# Show summary of the data
if st.checkbox('Show summary of the data'):
    st.subheader('Summary of the data')
    st.write(df.describe())

    # Select a column
    col = st.selectbox('Select a column', df.columns)
    st.write(df[col].describe())
    
    # Plot distribution of the column
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.histplot(df[col].dropna(), bins=30, kde=False, ax=ax)
    ax.set_title('Distribution of {}'.format(col))
    ax.set_xlabel(col)
    ax.set_ylabel('Count')
    st.pyplot(fig)

# Divider
st.write('---')

# Create a section
st.subheader('Exploration')

# Description of the data
st.write('The data contains information about the rentals of Getaround in Paris between 2019-01-01 and 2020-12-31.')

# Show the number of rentals by state
def plot_rental_by_state(data):
    # Define a color map for the states
    state_colors = {"canceled": "#d62728", "ended": "#1f77b4"}
    
    # Ensure sns.set() or sns.set_palette() is called outside the function to apply globally
    sns.set_theme(style="white")  # Optional: sets the Seaborn theme
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Use the 'palette' parameter to assign specific colors based on 'state' values
    sns.countplot(y='state', data=data, palette=state_colors, orient='v', ax=ax)
    
    ax.set_title('Number of Rentals by State')
    ax.set_xlabel('State')
    ax.set_ylabel('Count')
    return fig

st.subheader('Number of Rentals by State')
st.pyplot(plot_rental_by_state(df))

# Comment
st.write('The number of rentals that have been canceled is very low compared to the number of rentals that have ended. We will focus on rentals that have ended.')

# Now taking only rentals that have ended
df_ended = df[df.state == 'ended']
st.write('Number of rentals that have ended: {}'.format(df_ended.shape[0]))

# Create a new categorical column for late rentals in 'On time' and 'Late'
df['is_late'] = df['delay_at_checkout_in_minutes'].apply(lambda x: 'Late' if x > 0 else 'On time')


# Show the number of rentals by checkin type
def plot_rental_by_checkin_type(data):
    # Set the color palette
    checkin_type_colors = ['#1f77b4', '#ff7f0e']  # Blue and orange for different check-in types
    
    sns.set_theme(style="white")  # Sets the Seaborn theme
    
    fig, ax = plt.subplots(figsize=(12, 6))
    # Plot with specified colors for check-in types
    sns.countplot(y='checkin_type', data=data, palette=checkin_type_colors, ax=ax)
    
    ax.set_title('Number of Rentals by Check-in Type')
    ax.set_xlabel('Check-in Type')
    ax.set_ylabel('Count')
    return fig

st.subheader('Number of Rentals by Check-in Type')
st.pyplot(plot_rental_by_checkin_type(df))

# Comment
st.write('The number of rentals with a mobile check-in is much higher than the number of rentals with a connect check-in.')

# Show the number of late rentals by checkin type
def plot_late_rental_by_checkin_type(data):
    # Set the color palette
    checkin_type_colors = ['#ff7f0e', '#1f77b4']  # Blue and orange for different check-in types
    
    
    
    sns.set_theme(style="white")  # Sets the Seaborn theme
    
    fig, ax = plt.subplots(figsize=(12, 6))
    # Plot with specified colors for checkin types
    sns.countplot(y='checkin_type', data=data, palette=checkin_type_colors, ax=ax)
    
    ax.set_title('Number of Late Rentals by Check-in Type')
    ax.set_xlabel('Check-in Type')
    ax.set_ylabel('Count')
    return fig

st.subheader('Number of Late Rentals by Check-in Type')
st.pyplot(plot_late_rental_by_checkin_type(df_ended[df_ended['delay_at_checkout_in_minutes'] > 0]))

# Calculate the number of rentals, late rentals, and share of late rentals for each check-in type
number_of_rentals_mobile = df_ended[df_ended['checkin_type'] == 'mobile'].shape[0]
number_of_late_rentals_mobile = df_ended[(df_ended['checkin_type'] == 'mobile') & (df_ended['delay_at_checkout_in_minutes'] > 0)].shape[0]
share_of_late_rentals_mobile = number_of_late_rentals_mobile / number_of_rentals_mobile *100

number_of_rentals_connect = df_ended[df_ended['checkin_type'] == 'connect'].shape[0]
number_of_late_rentals_connect = df_ended[(df_ended['checkin_type'] == 'connect') & (df_ended['delay_at_checkout_in_minutes'] > 0)].shape[0]
share_of_late_rentals_connect = number_of_late_rentals_connect / number_of_rentals_connect *100

# Dataframe with numeric data, the number of rentals that ended, the number of late rentals and the share of late rentals
df_summary = pd.DataFrame({
    'number_of_rentals': [df_ended.shape[0], df_ended[df_ended['delay_at_checkout_in_minutes'] > 0].shape[0], df_ended[df_ended['delay_at_checkout_in_minutes'] > 0].shape[0] / df_ended.shape[0] * 100],
    'mobile': [number_of_rentals_mobile, number_of_late_rentals_mobile, share_of_late_rentals_mobile],
    'connect': [number_of_rentals_connect, number_of_late_rentals_connect, share_of_late_rentals_connect]
}, index=['Total', 'Late', 'Share of Late Rentals (%)'])

# Show the summary
st.subheader('Summary')
st.write(df_summary)

# Comment
st.write('The share of late rentals is 52"%" of all rentals, this is a major issue.')


# Change column checkin_type to categorical
df_ended['checkin_type'] = df_ended['checkin_type'].astype('category')

# Change colum state to categorical
df_ended['state'] = df_ended['state'].astype('category')

# Show interactions between columns
# hue = 'checkin_type' to show the interactions between checkin_type and other columns
#PLot interactions between delay_at_checkout_in_minutes and checkin_type
def plot_delay_by_checkin_type(data):
    # Set the color palette
    checkin_type_colors = ['#ff7f0e', '#1f77b4']  # Blue and orange for different check-in types
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(x='delay_at_checkout_in_minutes', y='checkin_type', data=data, ax=ax, whis=1.5, palette=checkin_type_colors)
    ax.set_title('Delay at Checkout by Check-in Type')
    ax.set_xlabel('Delay at Checkout in Minutes')
    ax.set_ylabel('Check-in Type')
    ax.set_xlim(-400, 1000)
    return fig


st.subheader('Delay at Checkout by Check-in Type')
st.pyplot(plot_delay_by_checkin_type(df_ended))

# Comment
st.write('The median delay at checkout is higher for mobile check-in than for connect check-in, the delays are also more pronounced.')

# Divider
st.write('---')

# Add a late window slider
st.subheader('Late Window')
late_window = st.slider('Select a late window (in minutes)', min_value=0, max_value=500, value=120)

# Filter the data based on the selected late window
df_late = df_ended[(df_ended['delay_at_checkout_in_minutes'] > - late_window) & (df_ended['delay_at_checkout_in_minutes'] < 0)]

# Share of rentals late at checkout by checkin type
def plot_share_of_late_rentals_by_checkin_type(data):
    # Set the color palette
    checkin_type_colors = ['#ff7f0e', '#1f77b4']  # Blue and orange for different check-in types
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='checkin_type', y='delay_at_checkout_in_minutes', data=data, ax=ax, estimator=lambda x: len(x) / len(data) * 100, palette=checkin_type_colors)
    ax.set_title('Share of Rentals Late at Checkout by Check-in Type')
    ax.set_xlabel('Check-in Type')
    ax.set_ylabel('Share of Rentals Late at Checkout')
    return fig

st.subheader('Share of Rentals Late at Checkout by Check-in Type')
st.pyplot(plot_share_of_late_rentals_by_checkin_type(df_late))

# Calculate the number of rentals late at checkout for each check-in type using the filtered data
number_of_late_rentals_by_checkin_type = df_late.groupby('checkin_type').size()

# Share in percent
number_of_late_rentals_by_checkin_type_percent = number_of_late_rentals_by_checkin_type / df_ended.shape[0] * 100

st.write('Number of rentals late at checkout for connect: {} ({:,.1f}%)'.format(number_of_late_rentals_by_checkin_type['connect'], number_of_late_rentals_by_checkin_type_percent['connect']))
st.write('Number of rentals late at checkout for mobile: {} ({:,.1f}%)'.format(number_of_late_rentals_by_checkin_type['mobile'], number_of_late_rentals_by_checkin_type_percent['mobile']))

# Plot the relation between the number of rentals late at checkout total, and by checkin type and the late window
def plot_number_of_late_rentals_by_late_window(data):
    # Prepare data for 'connect' checkin_type
    data_late = data.groupby('delay_at_checkout_in_minutes').size().reset_index().rename(columns={0: 'number_of_late_rentals'})
    data_connect = data[data['checkin_type'] == 'connect'].groupby('delay_at_checkout_in_minutes').size().reset_index().rename(columns={0: 'number_of_late_rentals_connect'})
    data_mobile = data[data['checkin_type'] == 'mobile'].groupby('delay_at_checkout_in_minutes').size().reset_index().rename(columns={0: 'number_of_late_rentals_mobile'})
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(x='delay_at_checkout_in_minutes', y='number_of_late_rentals', data=data_late, ax=ax, color='green')
    sns.lineplot(x='delay_at_checkout_in_minutes', y='number_of_late_rentals_connect', data=data_connect, ax=ax, color='orange')
    sns.lineplot(x='delay_at_checkout_in_minutes', y='number_of_late_rentals_mobile', data=data_mobile, ax=ax, color='blue')
    ax.set_title('Number of Rentals Late at Checkout by Late Window')
    ax.set_xlabel('Late Window in Minutes')
    ax.set_ylabel('Number of Rentals Late at Checkout')
    return fig

st.subheader('Number of Rentals Late at Checkout by Late Window')
st.pyplot(plot_number_of_late_rentals_by_late_window(df_late))

# Comment
st.write('The number of rentals late at checkout decreases with the late window. The number of rentals late at checkout for connect is higher than for mobile.')

# Divider
st.write('---')

# Create a section
st.subheader('Data Analysis')

# Finding an optimal delay between rentals
# Create a new column with the delay between rentals
df_ended['delay_between_rentals_in_minutes'] = df_ended['time_delta_with_previous_rental_in_minutes'] - df_ended['delay_at_checkout_in_minutes']

# Plot the distribution of the delay between rentals
def plot_delay_between_rentals(data):
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.histplot(data['delay_between_rentals_in_minutes'], bins=100, kde=True, ax=ax)
    ax.set_title('Distribution of Delay Between Rentals')
    ax.set_xlabel('Delay Between Rentals in Minutes')
    ax.set_ylabel('Count')
    # Add xlim
    ax.set_xlim(-1000, 1500)
    return fig

st.subheader('Distribution of Delay Between Rentals')
st.pyplot(plot_delay_between_rentals(df_ended))

# Comment
st.write('The distribution of the delay between rentals is right skewed, the negatives are rentals where the primary person was late to return the car. There are two peaks, the most important is around 0, and it represents the rentals that are slightly late or just on time, this is the element we can act on. The second peak represents the rentals that are on time.')

# Plot the distribution of the delay between rentals by checkin type
def plot_delay_between_rentals_by_checkin_type(data):
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(x='delay_between_rentals_in_minutes', y='checkin_type', data=data, ax=ax, whis=1.5)
    ax.set_title('Delay Between Rentals by Check-in Type')
    ax.set_xlabel('Delay Between Rentals in Minutes')
    ax.set_ylabel('Check-in Type')
    ax.set_xlim(-1000, 1500)
    return fig

st.subheader('Delay Between Rentals by Check-in Type')
st.pyplot(plot_delay_between_rentals_by_checkin_type(df_ended))

# Comment
st.write('The delay for mobile rentals are close to 0 which means that the primary person is on time or slightly late.')

# How does max delay affect the number of rentals?
# Plot delay between rentals with a slider for max delay
def plot_delay_between_rentals_with_max_delay(data, min_delay):
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.histplot(data['delay_between_rentals_in_minutes'], bins=100, kde=True, ax=ax)
    # vertical line for min delay
    ax.axvline(- min_delay, color='red')
    ax.set_title('Distribution of Delay Between Rentals')
    ax.set_xlabel('Delay Between Rentals in Minutes')
    ax.set_ylabel('Count')
    # Add xlim
    ax.set_xlim(-1000, 1500)
    return fig

st.subheader('Distribution of Delay Between Rentals with Min Delay')
min_delay = st.slider('Min Delay', 0, 1000, 180)
st.pyplot(plot_delay_between_rentals_with_max_delay(df_ended, min_delay))

# Comment
st.write('The application of the delay is shown by a red vertical line, further left than the line, these cases will be difficult to avoid, the first peak we mentionned before now will be included in the on time return due to the delay.')

# Distribution of delay at checkout depending on the min delay
def plot_delay_at_checkout_with_max_delay(data):
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.histplot(data['delay_at_checkout_in_minutes'], bins=10000, kde=False, ax=ax)
    ax.set_title('Distribution of Delay at Checkout considering Min Delay')
    ax.set_xlabel('Delay at Checkout in Minutes')
    ax.set_ylabel('Count')
    # vertical line for min delay
    ax.axvline( min_delay, color='red')
    # Add xlim
    ax.set_xlim(-400, 1000)
    return fig

st.subheader('Distribution of Delay at Checkout with Min Delay')
st.pyplot(plot_delay_at_checkout_with_max_delay(df_ended))

# Comment
st.write('The distribution of the delay at checkout shows negative what is in advance or on time, and positive what is late. The red vertical line shows the min delay, the rentals that are late but less than the min delay will be considered on time.')

# Which share of our owner’s revenue would potentially be affected by the feature?
# Total number of rentals that ended
total_number_of_rentals = df_ended.shape[0]
st.write('Total number of rentals that ended: {}'.format(total_number_of_rentals))
# Affected rentals by min delay
affected_rentals = df_ended[(df_ended['delay_at_checkout_in_minutes'] > 0 ) & (df_ended['delay_at_checkout_in_minutes'] < min_delay)].shape[0]
st.write('Affected rentals by min delay: {}'.format(affected_rentals))
# Share of affected rentals
share_of_affected_rentals = affected_rentals / total_number_of_rentals
# Share of unaffected rentals
share_of_unaffected_rentals = 1 - share_of_affected_rentals
# Pie plot
def plot_share_of_affected_rentals(data):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.pie([share_of_affected_rentals, share_of_unaffected_rentals], labels=['Affected Rentals', 'Unaffected Rentals'], autopct='%1.1f%%', startangle=90)
    ax.set_title('Share of Affected Rentals')
    return fig

st.subheader('Share of Affected Rentals')
st.pyplot(plot_share_of_affected_rentals(df_ended))

# Comment
st.write('The share of affected rentals is 42.3"%" of all rentals for a delay of 180 minutes, the implications are quite high.')

# Calculate the number of rentals, late rentals, and share of late rentals for each check-in type
number_of_rentals_mobile = df_ended[df_ended['checkin_type'] == 'mobile'].shape[0]
number_of_late_rentals_mobile_min_delay = df_ended[(df_ended['checkin_type'] == 'mobile') & (df_ended['delay_at_checkout_in_minutes'] > min_delay)].shape[0]
share_of_late_rentals_mobile_min_delay = number_of_late_rentals_mobile_min_delay / number_of_rentals_mobile *100
difference_mobile = number_of_late_rentals_mobile - number_of_late_rentals_mobile_min_delay
difference_mobile_percent = difference_mobile / number_of_late_rentals_mobile * 100

number_of_rentals_connect = df_ended[df_ended['checkin_type'] == 'connect'].shape[0]
number_of_late_rentals_connect_min_delay = df_ended[(df_ended['checkin_type'] == 'connect') & (df_ended['delay_at_checkout_in_minutes'] > min_delay)].shape[0]
share_of_late_rentals_connect_min_delay = number_of_late_rentals_connect_min_delay / number_of_rentals_connect *100
difference_connect = number_of_late_rentals_connect - number_of_late_rentals_connect_min_delay
difference_connect_percent = difference_connect / number_of_late_rentals_connect * 100

# Dataframe with numeric data, the number of rentals that ended, the number of late rentals and the share of late rentals
df_summary = pd.DataFrame({
    'number_of_rentals': [df_ended.shape[0],
                        df_ended[df_ended['delay_at_checkout_in_minutes'] > 0].shape[0],
                        df_ended[df_ended['delay_at_checkout_in_minutes'] > 0].shape[0] / df_ended.shape[0]*100,
                        df_ended[df_ended['delay_at_checkout_in_minutes'] > min_delay].shape[0],
                        df_ended[df_ended['delay_at_checkout_in_minutes'] > min_delay].shape[0] / df_ended.shape[0]*100,
                        df_ended[df_ended['delay_at_checkout_in_minutes'] > 0].shape[0] - df_ended[df_ended['delay_at_checkout_in_minutes'] > min_delay].shape[0],
                        (df_ended[df_ended['delay_at_checkout_in_minutes'] > 0].shape[0] - df_ended[df_ended['delay_at_checkout_in_minutes'] > min_delay].shape[0])/df_ended[df_ended['delay_at_checkout_in_minutes'] > 0].shape[0]*100],
    'mobile': [number_of_rentals_mobile, number_of_late_rentals_mobile, share_of_late_rentals_mobile, number_of_late_rentals_mobile_min_delay , share_of_late_rentals_mobile_min_delay, difference_mobile, difference_mobile_percent],
    'connect': [number_of_rentals_connect, number_of_late_rentals_connect, share_of_late_rentals_connect, number_of_late_rentals_connect_min_delay , share_of_late_rentals_connect_min_delay, difference_connect, difference_connect_percent],
}, index=['Total', 'Late without feature', 'Share of Late Rentals (%)', 'Late with Feature', 'Share of Late Rentals (%)', 'Difference', 'Difference (%)'])

# Show the summary
st.subheader(f'Table of data with the Feature : {min_delay} minutes')
st.write(df_summary)

# Comment
st.write('This table provide a summary of the numeric key parameters with and without the feature to show the impact. It is important to look at the diminution of late return with the feature, and for each checkin type. As it may not be as important to implement for the connect case instead of the mobile case. Howver, a small delay may still be useful')

# Conclusion
st.subheader('Conclusion')
st.write('The feature will have a positive impact on the number of late rentals, and the share of late rentals. Now the key element is to find the right delay that will optimise the case, on one hand the delay should be as small as possible to not impact the product, but at the same time it should be implemented in order to improve the issue of late return.')


# Create a figure and a set of subplots
fig, ax = plt.subplots()

# Create a line plot in function of min delay in a range of 0 to 500
y = []
x = []
# Calculate the percentage difference
for i in range(0, 500):
    y_temp = (df_ended[df_ended['delay_at_checkout_in_minutes'] > 0].shape[0] - df_ended[df_ended['delay_at_checkout_in_minutes'] > i].shape[0])/df_ended[df_ended['delay_at_checkout_in_minutes'] > 0].shape[0]*100
    y.append(y_temp)
    x.append(i)

ax.plot(x, y)


# Set the title and labels
ax.set_title('Percentage Difference in Late Rentals')
ax.set_ylabel('Percentage')
ax.set_xlabel('Min Delay')
# vertical line for min delay
ax.axvline( min_delay, color='red')
# Display the plot
st.pyplot(fig)

