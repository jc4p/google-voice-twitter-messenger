Google Voice Powered Twitter Messenger
=============

This Python application will check a specific e-mail address for e-mails forwarded from Google Voice and automatically posts them to Twitter using the Twitter API.

How to
------

Since Google Voice does not have an official API yet, and the one you can find by packet sniffing is too complicated for this task, this program uses e-mail forwarding built into Google Voice.

To use: Add an e-mail address to your Google Voice account and fill out auth.py and set up a cron script to run email_checker.py.

To retrieve the token and token_secret attributes for auth.py, please follow [this guide on Twitter](https://dev.twitter.com/docs/auth/oauth/single-user-with-examples) for retrieving a single user access token using OAuth.

####NOTE:
A new forwarder e-mail address is not absolutely necessary for this code as Google allows IMAP connections to regular GMail accounts, but this application originally lived on shared hosting that did not allow external HTTPS connections. To use the GMail account connected to your Google Voice account, enter this information in auth.py:
    auth.mail_server = "imap.gmail.com"
    auth.mail_address = "your_account@gmail.com" # The @gmail.com is necessary, if you use Google for your domain substitute your domain name.
    auth.mail_password = "your password"

If using your main Google account with this program, consider using Google's [two-step authentication system](https://www.google.com/accounts/SmsAuthConfig) so that you can give this script an application specific passphrase.