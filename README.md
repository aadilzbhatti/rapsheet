# Rapsheet
## Description
This is an application I designed in Django. The application allows you to search 
for an album (which must be available on Spotify) and examine its current appeal
based on sentiment collected from tweets about the album. 

## Technologies used
The application's back-end is written in Python using the Django framework. The front-end 
is written in HTML, CSS, and Javascript. The app makes extensive use of the D3.js library, 
which is used for creating SVG graphics. Its use here is for visualizing the sentiment 
analysis done in the back-end. The APIs utilized include the Twitter API, Alchemy API, 
and the Spotify API. The Spotify API is used for finding an album title based on a search; 
the Twitter API is used for gathering tweets based on the album title; the Alchemy API is used for 
analyzing each tweet and computing a sentiment value for the tweet. 

## Installation
Install `command line tools`:
    
    xcode-select -install
    
Install `brew`:
    
    ruby -e “$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)”

    brew doctor
    
Install `Python(3.4)`:
    
    brew install python3

To check if this worked, run the command `python3` in your terminal. If the Python 3 console comes up,
you have succeeded. 

## Using the code
To work with this app on your own machine, just fork the repository
    
    git clone https://github.com/prevosis/rapsheet.git

and run
 
    pip install -r requirements.txt
    
This will install the dependencies used by the app if you do not already have them. 
    
You will then need an AlchemyAPI key as well as TwitterAPI keys, 
which you should place in a file called `secrets.py`, in the main `raptweets` directory. You can create
this file with `touch secrets.py`. You can get the Alchemy and Twitter API keys from 
[here](http://www.alchemyapi.com/api/register.html) and [here](https://apps.twitter.com/app/new), respectively. 
`secrets.py` looks like this:

    ALCHEMY_CODES = [
        ''
    ]
    TWITTER_CODES = [
        {
            'CONSUMER_KEY': '',
            'CONSUMER_SECRET': '',
            'ACCESS_TOKEN': '',
            'ACCESS_SECRET': ''
        },
    ]
    
Where the empty strings should have API keys in your file.

Then, run 

    python3 manage.py runserver
    
and go to localhost:8000/raptweets/ to access the home page. 
