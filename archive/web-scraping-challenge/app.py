# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 20:59:21 2021

@author: brook
"""

#%%

from flask import Flask, render_template, redirect
import pymongo


#%%

# Instantiate flask app
app = Flask(__name__)


#%%

# Connect to MongoDB
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# Connect to mars_app MongoDB database
db = client.mars_app

# Connect to mars collection of mars_app MongoDB database
mars_coll = db.mars


#%%

@app.route('/')
def index():
    
    mars_data = mars_coll.find_one()
    
    return(render_template('index.html', mars_data=mars_data))

#%%
    
@app.route('/scrape')
def scrape():
    
    # this is the py script with all of the scraping functions
    import scrape_mars
    
    # Gather document (dictionary) to insert into mars collection named mars_dict
    # scrape_all() was created in teh scrape_mars.py file and is accessed by import (see above)
    mars_dict = scrape_mars.scrape_all()
    
    # Upsert into the mars collection (preferred to avoid duplicates)
    mars_coll.update_one({}, {'$set': mars_dict}, upsert=True)
    
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)



