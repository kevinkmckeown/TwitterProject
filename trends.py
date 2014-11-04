"""Visualizing Twitter Sentiment Across America"""

from data import word_sentiments, load_tweets
from datetime import datetime
from doctest import run_docstring_examples
from geo import us_states, geo_distance, make_position, longitude, latitude
from maps import draw_state, draw_name, draw_dot, wait, message
from string import ascii_letters
from ucb import main, trace, interact, log_current_line


# Phase 1: The Feelings in Tweets

def make_tweet(text, time, lat, lon):
    """Return a tweet, represented as a python dictionary.

    text  -- A string; the text of the tweet, all in lowercase
    time  -- A datetime object; the time that the tweet was posted
    lat   -- A number; the latitude of the tweet's location
    lon   -- A number; the longitude of the tweet's location

    >>> t = make_tweet("just ate lunch", datetime(2012, 9, 24, 13), 38, 74)
    >>> tweet_words(t)
    ['just', 'ate', 'lunch']
    >>> tweet_time(t)
    datetime.datetime(2012, 9, 24, 13, 0)
    >>> p = tweet_location(t)
    >>> latitude(p)
    38
    """
    return {'text': text, 'time': time, 'latitude': lat, 'longitude': lon}

def tweet_words(tweet):
    """Return a list of the words in the text of a tweet."""
    "*** YOUR CODE HERE ***"
    return extract_words(tweet['text'])

def tweet_time(tweet):
    """Return the datetime that represents when the tweet was posted."""
    "*** YOUR CODE HERE ***"
    return tweet['time'];

def tweet_location(tweet):
    """Return a position (see geo.py) that represents the tweet's location."""
    "*** YOUR CODE HERE ***"
    return make_position(tweet['latitude'],tweet['longitude']);

def tweet_string(tweet):
    """Return a string representing the tweet."""
    return '"{0}" @ {1}'.format(tweet['text'], tweet_location(tweet))

def extract_words(text):
    """Return the words in a tweet, not including punctuation.

    >>> extract_words('anything else.....not my job')
    ['anything', 'else', 'not', 'my', 'job']
    >>> extract_words('i love my job. #winning')
    ['i', 'love', 'my', 'job', 'winning']
    >>> extract_words('make justin # 1 by tweeting #vma #justinbieber :)')
    ['make', 'justin', 'by', 'tweeting', 'vma', 'justinbieber']
    >>> extract_words("paperclips! they're so awesome, cool, & useful!")
    ['paperclips', 'they', 're', 'so', 'awesome', 'cool', 'useful']
    >>> extract_words('@(cat$.on^#$my&@keyboard***@#*')
    ['cat', 'on', 'my', 'keyboard']
    """
    "*** YOUR CODE HERE ***"
    i = 0
    charList = list(text)
    length = len(charList)
    newList = []
    word = ""

    for char in charList:
        length = len(charList)
        i=i+1
        if char not in ascii_letters:
            if word != "":
                newList += [str(word)]
            word = ""
        elif i == length and char in ascii_letters:
            word += char
            newList += [str(word)]
        elif word == ' ':
            newList += [str(word)]
            word = ""
        else:
            word+= char       
    return newList

def make_sentiment(value):
    """Return a sentiment, which represents a value that may not exist.

    >>> positive = make_sentiment(0.2)
    >>> neutral = make_sentiment(0)
    >>> unknown = make_sentiment(None)
    >>> has_sentiment(positive)
    True
    >>> has_sentiment(neutral)
    True
    >>> has_sentiment(unknown)
    False
    >>> sentiment_value(positive)
    0.2
    >>> sentiment_value(neutral)
    0
    """
    assert value is None or (value >= -1 and value <= 1), 'Illegal value'
    "*** YOUR CODE HERE ***"
    return value

def has_sentiment(s):
    """Return whether sentiment s has a value."""
    "*** YOUR CODE HERE ***"
    if s == None:
        return False
    else:
        return True

def sentiment_value(s):
    """Return the value of a sentiment s."""
    assert has_sentiment(s), 'No sentiment value'   #confirms a value exists
    "*** YOUR CODE HERE ***"
    return make_sentiment(s)

def get_word_sentiment(word):
    """Return a sentiment representing the degree of positive or negative
    feeling in the given word.

    >>> sentiment_value(get_word_sentiment('good'))
    0.875
    >>> sentiment_value(get_word_sentiment('bad'))
    -0.625
    >>> sentiment_value(get_word_sentiment('winning'))
    0.5
    >>> has_sentiment(get_word_sentiment('Berkeley'))
    False
    """
    # Learn more: http://docs.python.org/3/library/stdtypes.html#dict.get
    return make_sentiment(word_sentiments.get(word))    # get returns value of given key

def analyze_tweet_sentiment(tweet):
    """ Return a sentiment representing the degree of positive or negative
    sentiment in the given tweet, averaging over all the words in the tweet
    that have a sentiment value.

    If no words in the tweet have a sentiment value, return
    make_sentiment(None).

    >>> positive = make_tweet('i love my job. #winning', None, 0, 0)
    >>> round(sentiment_value(analyze_tweet_sentiment(positive)), 5)
    0.29167
    >>> negative = make_tweet("saying, 'i hate my job'", None, 0, 0)
    >>> sentiment_value(analyze_tweet_sentiment(negative))
    -0.25
    >>> no_sentiment = make_tweet("berkeley golden bears!", None, 0, 0)
    >>> has_sentiment(analyze_tweet_sentiment(no_sentiment))
    False
    """
    average = make_sentiment(None)
    "*** YOUR CODE HERE ***"
    text = tweet_words(tweet)
    total = 0
    counter = 0

    for word in text:
        if has_sentiment(get_word_sentiment(word)) == True:
            total = total + sentiment_value(get_word_sentiment(word)) #total sum of sentiment values
            counter = counter +1
    average = make_sentiment(total/counter) #average sentiment of all words
    return average


# Phase 2: The Geometry of Maps

def find_centroid(polygon):
    """Find the centroid of a polygon.

    http://en.wikipedia.org/wiki/Centroid#Centroid_of_polygon

    polygon -- A list of positions, in which the first and last are the same

    Returns: 3 numbers; centroid latitude, centroid longitude, and polygon area

    Hint: If a polygon has 0 area, use the latitude and longitude of its first
    position as its centroid.

    >>> p1, p2, p3 = make_position(1, 2), make_position(3, 4), make_position(5, 0)
    >>> triangle = [p1, p2, p3, p1]  # First vertex is also the last vertex
    >>> tuple(map(float, find_centroid([p1, p2, p1])))  # A zero-area polygon
    (1.0, 2.0, 0.0)
    """
    # find area

    area = 0
    pos = 0
    
    while len(polygon)-1 > pos:
        area+=(latitude(polygon[pos])*longitude(polygon[pos+1])-(latitude(polygon[pos+1])*longitude(polygon[pos]))) # area equation
        pos = pos + 1   # increment the position index
    area = area * (.5)  # final part of area calculation
    newArea = area      # variable that holds the area of polygon we are working with currently
    
    #if the area of the polygon is 0, this returns the initial position
    if newArea == 0:
        return (latitude(polygon[0]), longitude(polygon[0]), 0)
    
    # finds the central latitude
    # initalize center latitude value and pos value
    centerLat = 0         
    pos = 0
    while len(polygon)-1 > pos:
       # calculate first part of overall latitiude calculation for each polygon
       centerLat += (latitude(polygon[pos])+latitude(polygon[pos+1]))*(latitude(polygon[pos])*longitude(polygon[pos+1])-latitude(polygon[pos+1])*longitude(polygon[pos]))
       pos+=1   # increment the pos variable to access next polygon

    # calculate second part of overall latitude calculation for each polygon
    centerLat = (centerLat)/(6*area)    
        

    #finds the cenral longitude
    pos = 0
    centerLong = 0      # initalize center longitude value and pos value
    while len(polygon)-1 > pos:
        # calculate first part of overall longitude calculation for each polygon
        centerLong += (longitude(polygon[pos])+longitude(polygon[pos+1]))*(latitude(polygon[pos])*longitude(polygon[pos+1])-latitude(polygon[pos+1])*longitude(polygon[pos]))
        pos+=1
    # calculate first part of overall latitude calculation for each polygon
    centerLong = (centerLong)/(6*area) 
     
    
    return (centerLat, centerLong, abs(area))

def find_center(polygons):
    """Compute the geographic center of a state, averaged over its polygons.

    The center is the average position of centroids of the polygons in polygons,
    weighted by the area of those polygons.

    Arguments:
    polygons -- a list of polygons

    >>> ca = find_center(us_states['CA'])  # California
    >>> round(latitude(ca), 5)
    37.25389
    >>> round(longitude(ca), 5)
    -119.61439

    >>> hi = find_center(us_states['HI'])  # Hawaii
    >>> round(latitude(hi), 5)
    20.1489
    >>> round(longitude(hi), 5)
    -156.21763
    """
  
    areaSum = 0
    sumX = 0
    sumY = 0

    #cycle through the shapes in the polygon list
    for shape in polygons:  
        centroid = find_centroid(shape) # returns (x-coordinate, y-coordinate, area)
        areaSum = areaSum + centroid[2] # add area of centroid to total sum for area
        area = centroid[2]
        sumX = sumX + area*centroid[0]  # add (area*x-coordinate of centeroid) to total
        sumY = sumY + area*centroid[1]  # add (area*y-coordinate of centeroid) to total
    genCentX = sumX/areaSum  # calculate the general center of latitude
    genCentY = sumY/areaSum  # calculate the general center of longitude
    
    return make_position(genCentX, genCentY)




# Phase 3: The Mood of the Nation

def find_closest_state(tweet, state_centers):
    """Return the name of the state closest to the given tweet's location.

    Use the geo_distance function (already provided) to calculate distance
    in miles between two latitude-longitude positions.

    Arguments:
    tweet -- a tweet abstract data type
    state_centers -- a dictionary from state names to positions.

    >>> us_centers = {n: find_center(s) for n, s in us_states.items()}
    >>> sf = make_tweet("welcome to san Francisco", None, 38, -122)
    >>> ny = make_tweet("welcome to new York", None, 41, -74)
    >>> find_closest_state(sf, us_centers)
    'CA'
    >>> find_closest_state(ny, us_centers)
    'NJ'
    """
    "*** YOUR CODE HERE ***"
    
    distList = {}
    pos = tweet_location(tweet)
    stateKey = ""
    
    for center in state_centers:
        distance = geo_distance(pos, state_centers[center])
        distList[center] = distance
    for state in distList:
        if distList[state] < distance:
            distance = distList[state]
            stateKey = state
    return stateKey

def group_tweets_by_state(tweets):
    """Return a dictionary that aggregates tweets by their nearest state center.

    The keys of the returned dictionary are state names, and the values are
    lists of tweets that appear closer to that state center than any other.

    tweets -- a sequence of tweet abstract data types

    >>> sf = make_tweet("welcome to san francisco", None, 38, -122)
    >>> ny = make_tweet("welcome to new york", None, 41, -74)
    >>> ca_tweets = group_tweets_by_state([sf, ny])['CA']
    >>> tweet_string(ca_tweets[0])
    '"welcome to san francisco" @ (38, -122)'
    """
    tweets_by_state = {}
    
    '''*** YOUR CODE HERE ***'''
    usCenters = {n: find_center(s) for n, s in us_states.items()}
    
    for tweet in tweets:
        location = find_closest_state(tweet,usCenters)
        if location in tweets_by_state:
            tweets_by_state[location] += [tweet,]
        else:
            tweets_by_state[location] = [tweet,]
            
    return tweets_by_state


def most_talkative_state(term):
    """Return the state that has the largest number of tweets containing term.

    If multiple states tie for the most talkative, return any of them.

    >>> most_talkative_state('texas')
    'TX'
    >>> most_talkative_state('soup')
    'CA'
    """
    tweets = load_tweets(make_tweet, term)  # A list of tweets containing term
    "*** YOUR CODE HERE ***"
    stateCounter = {}
    count = 0
    tweetState= group_tweets_by_state(tweets)
    for state in tweetState:
        for tweet in tweetState[state]:
            if term in tweet_words(tweet):
                count += 1
        stateCounter[state] = count
        count = 0
    mostStateTweet= None
    for stateKey in stateCounter:
        if mostStateTweet == None:
            mostStateTweet = stateCounter[stateKey]
            state=stateKey
        elif stateCounter[stateKey] > mostStateTweet:
            mostStateTweet = stateCounter[stateKey]
            state = stateKey

    return state        

def average_sentiments(tweets_by_state):
    """Calculate the average sentiment of the states by averaging over all
    the tweets from each state. Return the result as a dictionary from state
    names to average sentiment values (numbers).

    If a state has no tweets with sentiment values, leave it out of the
    dictionary entirely.  Do NOT include states with no tweets, or with tweets
    that have no sentiment, as 0.  0 represents neutral sentiment, not unknown
    sentiment.

    tweets_by_state -- A dictionary from state names to lists of tweets
    """
    averaged_state_sentiments = {}
    "*** YOUR CODE HERE ***"
    
    for state in tweets_by_state:
        if len(state) != 0:
            
            sentCount = 0
            totalSent =  0

            for tweet in tweets_by_state[state]:
                
                sentiment = analyze_tweet_sentiment(tweet)
                if sentiment != None:
                    totalSent += sentiment
                    sentCount = sentCount + 1
                
            if sentCount != 0:
                averaged_state_sentiments[state] = totalSent/sentCount
                
    return averaged_state_sentiments


# Phase 4: Into the Fourth Dimension

def group_tweets_by_hour(tweets):
    """Return a dictionary that groups tweets by the hour they were posted.

    The keys of the returned dictionary are the integers 0 through 23.

    The values are lists of tweets, where tweets_by_hour[i] is the list of all
    tweets that were posted between hour i and hour i + 1. Hour 0 refers to
    midnight, while hour 23 refers to 11:00PM.

    To get started, read the Python Library documentation for datetime objects:
    http://docs.python.org/py3k/library/datetime.html#datetime.datetime

    tweets -- A list of tweets to be grouped

    >>> tweets = load_tweets(make_tweet, 'party')
    >>> tweets_by_hour = group_tweets_by_hour(tweets)
    >>> for hour in [0, 5, 9, 17, 23]:
    ...     current_tweets = tweets_by_hour.get(hour, [])
    ...     tweets_by_state = group_tweets_by_state(current_tweets)
    ...     state_sentiments = average_sentiments(tweets_by_state)
    ...     print('HOUR:', hour)
    ...     for state in ['CA', 'FL', 'DC', 'MO', 'NY']:
    ...         if state in state_sentiments.keys():
    ...             print(state, ":", round(state_sentiments[state], 5))
    HOUR: 0
    CA : 0.08333
    FL : -0.09635
    DC : 0.01736
    MO : -0.11979
    NY : -0.15
    HOUR: 5
    CA : 0.00945
    FL : -0.0651
    DC : 0.03906
    MO : 0.1875
    NY : -0.04688
    HOUR: 9
    CA : 0.10417
    NY : 0.25 
    HOUR: 17
    CA : 0.09808
    FL : 0.0875
    MO : -0.1875
    NY : 0.14583
    HOUR: 23
    CA : -0.10729
    FL : 0.01667
    DC : -0.3
    MO : -0.0625
    NY : 0.21875
    """
    tweets_by_hour = {}
    "*** YOUR CODE HERE ***"
    for each_tweet in tweets:
        hour = tweet_time(each_tweet).hour 
        if hour not in tweets_by_hour:
            tweets_by_hour[hour] = [each_tweet,]
        else:
            tweets_by_hour[hour] += [each_tweet,]
            
    return tweets_by_hour



# Interaction.  You don't need to read this section of the program.

def print_sentiment(text='Are you virtuous or verminous?'):
    """Print the words in text, annotated by their sentiment scores."""
    words = extract_words(text.lower())
    layout = '{0:>' + str(len(max(words, key=len))) + '}: {1:+}'
    for word in words:
        s = get_word_sentiment(word)
        if has_sentiment(s):
            print(layout.format(word, sentiment_value(s)))

def draw_centered_map(center_state='TX', n=10):
    """Draw the n states closest to center_state."""
    us_centers = {n: find_center(s) for n, s in us_states.items()}
    center = us_centers[center_state.upper()]
    dist_from_center = lambda name: geo_distance(center, us_centers[name])
    for name in sorted(us_states.keys(), key=dist_from_center)[:int(n)]:
        draw_state(us_states[name])
        draw_name(name, us_centers[name])
    draw_dot(center, 1, 10)  # Mark the center state with a red dot
    wait()

def draw_state_sentiments(state_sentiments):
    """Draw all U.S. states in colors corresponding to their sentiment value.

    Unknown state names are ignored; states without values are colored grey.

    state_sentiments -- A dictionary from state strings to sentiment values
    """
    for name, shapes in us_states.items():
        sentiment = state_sentiments.get(name, None)
        draw_state(shapes, sentiment)
    for name, shapes in us_states.items():
        center = find_center(shapes)
        if center is not None:
            draw_name(name, center)

def draw_map_for_term(term='my job'):
    """Draw the sentiment map corresponding to the tweets that contain term.

    Some term suggestions:
    New York, Texas, sandwich, my life, justinbieber
    """
    tweets = load_tweets(make_tweet, term)
    tweets_by_state = group_tweets_by_state(tweets)
    state_sentiments = average_sentiments(tweets_by_state)
    draw_state_sentiments(state_sentiments)
    for tweet in tweets:
        s = analyze_tweet_sentiment(tweet)
        if has_sentiment(s):
            draw_dot(tweet_location(tweet), sentiment_value(s))
    wait()

def draw_map_by_hour(term='my job', pause=0.5):
    """Draw the sentiment map for tweets that match term, for each hour."""
    tweets = load_tweets(make_tweet, term)
    tweets_by_hour = group_tweets_by_hour(tweets)

    for hour in range(24):
        current_tweets = tweets_by_hour.get(hour, [])
        tweets_by_state = group_tweets_by_state(current_tweets)
        state_sentiments = average_sentiments(tweets_by_state)
        draw_state_sentiments(state_sentiments)
        message("{0:02}:00-{0:02}:59".format(hour))
        wait(pause)

def run_doctests(names):
    """Run verbose doctests for all functions in space-separated names."""
    g = globals()
    errors = []
    for name in names.split():
        if name not in g:
            print("No function named " + name)
        else:
            run_docstring_examples(g[name], g, True, name)

@main
def run(*args):
    """Read command-line arguments and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Run Trends")
    parser.add_argument('--print_sentiment', '-p', action='store_true')
    parser.add_argument('--run_doctests', '-t', action='store_true')
    parser.add_argument('--draw_centered_map', '-d', action='store_true')
    parser.add_argument('--draw_map_for_term', '-m', action='store_true')
    parser.add_argument('--draw_map_by_hour', '-b', action='store_true')
    parser.add_argument('text', metavar='T', type=str, nargs='*',
                        help='Text to process')
    args = parser.parse_args()
    for name, execute in args.__dict__.items():
        if name != 'text' and execute:
            globals()[name](' '.join(args.text))

