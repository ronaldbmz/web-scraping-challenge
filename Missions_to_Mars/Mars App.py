#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 00:41:46 2021

@author: tiffanyelle
"""

from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)

#Making mongo db connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")
mars = mongo.db.mars

#Inserting the data into table for the first time
(data,df) = scrape_mars.scrape()
mars.update(
    {},
    data,
    upsert=True
)

@app.route('/')
def index():
    mars = mongo.db.mars.find_one()
    return render_template('mars_index.html', mars=mars, tables=df.to_html(classes='table'))


@app.route('/scrape')
def scrape():
    mars = mongo.db.mars
    (data,df) = scrape_mars.scrape()
    mars.update(
        {},
        data,
        upsert=True
    )
    mars = mongo.db.mars.find_one()
    render_template('mars_index.html', mars=mars, tables=df.to_html(classes='table'))
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(port=5000)
