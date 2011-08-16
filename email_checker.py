import imaplib
import pymysql
import twitter
import oauth2 as oauth
import auth

# Connect to mail server via IMAP
M = imaplib.IMAP4(auth.mail_server)
res = M.login(auth.mail_address, auth.mail_password)
res = M.select()
# Search for e-mails with subject "SMS", which is what Google Voice forwarder messages contain.
typ, data = M.search(None, 'SUBJECT', '"SMS"')

# Connect to MySQL database
conn = pymysql.connect(host=auth.mysql_server, 
user=auth.mysql_user, passwd=auth.mysql_password, db=auth.mysql_db)
cur = conn.cursor()
cur.execute("SELECT message_id FROM status")

already_posted = []

# Create a list of posted messages, in case an e-mail was sent multiple times.
for r in cur:
	already_posted.append(r[0])

# Authenticate with the Twitter API
api = twitter.Api(consumer_key=auth.twitter_consumer, 
consumer_secret=auth.twitter.secret, 
access_token_key=auth.twitter_token, 
access_token_secret=auth.twitter_token_secret)

# Loop through the current e-mails and parse out data
for num in data[0].split():
	typ, data = M.fetch(num, '(RFC822)')
	
	content = data[0][1].split('\r\n')
	message_id = ""
	phone_number = ""
	message = ""
	for x in range(len(content)):
		line = content[x]
		if line.find('Message-ID') > -1:
			message_id = line.split(":")[1].strip()
		if line.find('From:') > -1:
			phone_number = line.split('"')[1].strip()
	message = data[0][1].split('Content-Type:')[1]
	message = message.split('\r\n\r\n')[1].replace('\r\n', ' ')

	if message_id not in already_posted:
		cur = conn.cursor()
		# Record this message in our database
		cur.execute('INSERT into status (message_id,phone_number,content) VALUES ("%s", "%s", "%s")' % (message_id, phone_number, message))
		# Post message to Twitter account
		api.PostUpdate(message)

conn.close()
