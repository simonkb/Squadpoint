# The Squadpoint Website
## Introduction
Squadpoint is a web application that allows users interested in team sports to compete, interact, reserve courts in an easy organized way at any time and place using their smartphones or computers.

The main goal of this application is to create a friendly platform for people in love with competitive racket sports(tennis, table tennis, badminton, and padel) to find an easy way to reserve courts and find opponents. All within a friendly contained environment full of sportsmanship spirit.

It's a very smooth way to register and secure your reservation for sport courts without worrying about it being taken. In addition, to finding other opponent teams to add a spice of competition.

Squadpoint intends to be the main organizer and intermediate application between racket sport lovers and the courts owners. It gives a platform to our participants to reserve courts,and  compete easily.

## Distinctiveness and Complexity
Regarding the *distinctiveness*, my application does not have any significant relation with the other projects I have completed in the series. As is all mentioned in the introduction section my application provides services for racket sports lovers and racket sports courts owners.

When it comes to *complexity*, my web application utilizes Django incorporating eight  models in [models.py](models.py) file and thirteen views functions in [views.py](views.py) file on the back-end. In the front-end, I have used JavaScript along with HTML and CSS. 

## Contents of the project files 
The project contains multiple files and directories all required to run a Django web application. 

**The Squadpoint app directory contains the following files:** 
* [models.py](models.py) file contains all eight models of the Squadpoint application. 
* [views.py](views.py) file contains all thirteen view functions of the application.
* [urls.py](urls.py) file contains the url pattern of all the paths of the application. 
* In addition, there are other files created by default.

**The Squadpoint app directory contains the following directories:** 

* *static/squadpoint directory* contains static file 'capstone.js', which contains some JavaScript code of the project.
* *templates/squadpoint directory* contains all the html templates of the project. Here we have one [layout.html](squadpoint/layout.html) file and eleven other template html files that extends the [layout.html](squadpoint/layout.html) namely [index.html](squadpoint/index.html), [login.html](squadpoint/login.html), [register.html](squadpoint/register.html), [search.html](squadpoint/search.html), [sport_zone.html](squadpoint/sport_zone.html), [sport_court.html](squadpoint/sport_court.html), [bookings.html](squadpoint/bookings.html), [matches.html](squadpoint/matches.html), [notifications.html](squadpoint/notifications.html), [profile.html](squadpoint/profile.html), and [about.html](squadpoint/about.html). Most of these templates contain a significant amount of JavaScript codes in side their script tags.  The [layout.html](squadpoint/layout.html) file also contains the CSS styles for the entire project inside its style tag. 
* In addition, there are other directories like *migrations* in the squadpoint directory. 


**The Capstone project directory contains the following files:** 

* [settings.py](settings.py) file contains the basic configurations of the project.
* [urls.py](urls.py) contains url pattern which incorporates the paths for admin and the installed app.
* And other files

## Running my web application
Make a pull request and get the entire project folder to your computer. Then you can use the command 'python manage.py runserver'.

## Additional information
This is developing project that can include more functionalities according to my design, however, I have decided to submit it after completing the first complete phase to complete this course in time.
