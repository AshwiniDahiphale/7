import streamlit as st
import pandas as pd
import preprocess,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

df=pd.read_csv('athlete_events.csv')
region_df=pd.read_csv('noc_regions.csv')

df=preprocess.preprocess(df,region_df)

st.sidebar.title("Olympics Analysis")
st.sidebar.image('https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png')
user_menu=st.sidebar.radio(
    'Select An Option',
    ('Medal Tally','Overall Analysis','Country Wise Analysis','Athlete Wise Analysis')
)
if user_menu=="Medal Tally":
    st.sidebar.header("Medal Tally")
    years,country=helper.country_year_list(df)
    selected_year=st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select country", country)

    medal_tally=helper.fetch_medal_tally(df, selected_year, selected_country)
    if selected_year =='Overall' and selected_country == 'Overall':
        st.title('Overall Tally')
    if selected_year !='Overall' and selected_country =='Overall':
        st.title("Medal Tally In " + str(selected_year) +" Olympics")
    if selected_year =='Overall' and selected_country!='Overall':
        st.title(selected_country+" Overall Performance")
    if selected_year!='Overall' and selected_country !='Overall':
        st.title(selected_country +" Performance in "+str(selected_year)+" Olympics")
    st.dataframe(medal_tally)

if user_menu =='Overall Analysis':
    editions=df['Year'].unique().shape[0]-1
    Cities = df['City'].unique().shape[0]
    Sports = df['Sport'].unique().shape[0]
    Events=df['Event'].unique().shape[0]
    Athelets = df['Name'].unique().shape[0]
    Nations = df['region'].unique().shape[0]

    st.title('Top Statistics')
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(Cities)
    with col3:
        st.header("Sport")
        st.title(Sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(Events)
    with col2:
        st.header("Athelets")
        st.title(Athelets)
    with col3:
        st.header("Nations")
        st.title(Nations)

    nations_over_time = helper.data_over_time(df,'region')
    fig = px.line(nations_over_time, x="count", y="Year")
    st.title("Participating Nations Over the years")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df,'Event')
    fig = px.line(events_over_time, x="count", y="Year")
    st.title("Events  Over the years")
    st.plotly_chart(fig)

    athlete_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athlete_over_time, x="count", y="Year")
    st.title("Athletes  Over the years")
    st.plotly_chart(fig)

    st.title("No. of Events over time (Every Sport)")
    fig,ax=plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax=sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
    st.pyplot(fig)

    st.title("Most Successfull Athletes")
    SL=df['Sport'].unique().tolist()
    SL.sort()
    SL.insert(0,'Overall')

    Selected_sport=st.selectbox('Select a Sport',SL)
    x= helper.most_successfull(df,Selected_sport)
    st.table(x)

if user_menu == 'Country Wise Analysis':

    st.sidebar.title('Country Wise Analysis')
    cl=df['region'].dropna().unique().tolist()
    cl.sort()
    selected_country=st.sidebar.selectbox('Selected Country',cl)

    country_df=helper.year_wise_tally(df,selected_country)
    fig = px.line(country_df, y="Medal", x="Year")
    st.title(selected_country + " Medal Tally Over the years")
    st.plotly_chart(fig)

    st.title(selected_country + " Excels in the following sports")
    pt=helper.country_event_heatmap(df,selected_country)
    fig,ax=plt.subplots(figsize=(20,20))
    ax=sns.heatmap(pt,annot=True)

    st.pyplot(fig)

    st.title("Top 10 Athletes of "+ selected_country)
    top10_df=helper.most_successful_countrywise(df,selected_country)
    st.table(top10_df)

if user_menu == 'Athlete Wise Analysis':
    athletes_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athletes_df['Age'].dropna()
    x2 = athletes_df[athletes_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athletes_df[athletes_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athletes_df[athletes_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sport = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                    'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                    'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                    'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                    'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                    'Tennis', 'Golf', 'Softball', 'Archery',
                    'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                    'Rhythmic Gymnastics', 'Rugby Sevens',
                    'Beach Volleyball', 'Triathlon', 'Rugby', 'Lacrosse', 'Polo',
                    'Cricket', 'Ice Hockey']
    for sport in famous_sport:
        temp_df = athletes_df[athletes_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt sports(Gold Medalist)")
    st.plotly_chart(fig)

    for sport in famous_sport:
        temp_df = athletes_df[athletes_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Silver']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt sports(Silver Medalist)")
    st.plotly_chart(fig)

    st.title("Men Vs Women Participating Over the Years")
    final=helper.men_vs_women(df)
    fig=px.line(final,x='Year',y=['Male','Female'])
    st.plotly_chart(fig)


