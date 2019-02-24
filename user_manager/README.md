# Auth0 User Manager

This is intended to be a "Delegated Administration + Metadata Editor" tool. The
Delegated Administration extension is great, but does not allow editing of a
user's metadata (`user_metadata` and `app_metadata`).

Auth0 login is set up. The app requires only that you be logged in. Additional
access control should be implemented in Auth0 using a rule.

After logging in, the app displays the profile of the logged in user. Currently
it displays only the data from the JWT. Needs integration with the Management
API to pull the entire user profile.

![Auth0 User Manager](https://github.com/dmark/auth0-flask-utilities/blob/master/screenshots/Screenshot%202019-02-24%2009.47.32.png)