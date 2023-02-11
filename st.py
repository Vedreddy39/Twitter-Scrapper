#pip install streamlit

import streamlit as st
import snscrape.modules.twitter as sntwitter
import pandas as pd


tweets_list = []

st.set_page_config(page_title = "Twitter Scraper", layout = 'wide')
st.subheader("Twitter Scrapper")
st.caption('a project by Ved Reddy')

with st.form(key = 'Twitter_form'):
    search_term = st.text_input('Enter the keyword to search for related tweets')
    limit = st.number_input('How many tweets to scrape?', 50, 5000, step=100)
    #st.write('Select the date range to scrape tweets from')
    #start_date = st.date_input('Enter the start date:', )
    #end_date = st.date_input('Enter the end date:', ) 
    output = st.radio('Select File Format?', ['csv', 'json'])
    file_name = st.text_input('Name the file:', max_chars=20)
    submit_button = st.form_submit_button(label='Search')

def tweet_scraper():
    for tweet in sntwitter.TwitterSearchScraper(search_term).get_items():
      tweets_list.append([tweet.date, tweet.id, tweet.url, tweet.content, tweet.user.username, tweet.replyCount, tweet.retweetCount, tweet.lang, tweet.source, tweet.likeCount])
    
      if len(tweets_list) == limit:
        break
  
if submit_button:
    tweet_scraper()
    df = pd.DataFrame(tweets_list, columns=['date', 'id', 'url', 'content', 'user_name',
                      'reply_count', 'retweet_count', 'language', 'source', 'like_count'])
    st.table(df)

    if output == 'csv':
        st.download_button(label = 'Download CSV file', data = df.to_csv(), mime = 'text/csv')
    
    if output == 'json':
       st.download_button(label = 'Download JSON file', data = df.to_json(), mime = 'application/json')
         
