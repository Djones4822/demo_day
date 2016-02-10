# b4-demo-day-g1
uTakeout  

## General
For some, the most important factor about any given location is the food. uTakeout helps you 

## How To Use SteamScout
1. Sign up to make an account
2. Use the link sent to your email to validate your account
3. Search for games
4. Set a scout to email you when a game drops down to a price you set
5. SteamScout will email you automatically if any of your games hit your preferences.

- You can update/delete your set price scouts at any time.

Below will be transferred over to GH issues.

### Optional Future Features

+ Paginate games library, currently causes significant lag. SQL alchemy has something built in for pagination
+ Make it mobile friendly, add media queries
+ Improve Settings page. - Improved it to look better.
+ Add percentage threshold option for preferences
+ Color divs in preferences so that users can see how close their set price is to the current price.
+ Implement Flask blueprints
+ validate each integer in the amount threshold form
+ make the individual games look pretty - Improved it, but it could be better..
+ Change generic variables to be more specific. Ex. form should should be login_form
+ Add to the settings page when no preferences are set.
+ Add a default currency on games page
+ Add button/link to the settings page which link to game search ''Add New Scout''

### Completed:
+ see if theres a way to include game cover art, trailers, etc in the individual game page
+ Change Preferences so that once an email goes out with that preference,
either delete the preference or mark it so that it doesn't get sent out again in the next report.
+ Convert game games to links to games steam store page. (available in the API)
+ User must be authenticated before saving games.
+ Set up email notifications and integrate with some type of scheduling system.
+ set up the gamesDB to automatically refresh every 24 hours. - Cron Job
+ 404 screen is broken. Image not loading.
- Flashes
- configure a way for steamscout to email users. - Flask-Mail
- Update button in user's settings page.
- set up user preferences
- Set up email account validations
- format price data. Currently "$4.99" displays as "499" - changed format_prices to make it easier
- Ideally, figure a way to only put games into the gamesDB.
    - if not 2, protect the site from apps that dont have a price_info section.
- build way to search through games library - Basic Functionality
- Changes amount format, list view on settings
- Improve Navbar in base (log out column adding problems)
- Split components into separate files. App.py is too big for one file.