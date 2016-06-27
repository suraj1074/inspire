import json

import flask
import httplib2

from apiclient import discovery
from oauth2client import client
import createDraft
from apiclient import errors

import MySQLdb
import config

app = flask.Flask(__name__,static_folder='/home/sjha/development/gmail/templates')

resultText = ""
try:
	database = MySQLdb.connect(config.settings['host'],config.settings['user'],\
		config.settings['password'],config.settings['database_name'] )
except MySQLdb.Error, e:
 	print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])

@app.route('/')
def index():
  if 'credentials' not in flask.session:
    return flask.redirect(flask.url_for('oauth2callback'))
  credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
  if credentials.access_token_expired:
    return flask.redirect(flask.url_for('oauth2callback'))
  else:
    return flask.render_template('test.html')

@app.route('/oauth2callback')
def oauth2callback():
  flow = client.flow_from_clientsecrets(
      'client_secret.json',
      scope='https://mail.google.com/',
      redirect_uri=flask.url_for('oauth2callback', _external=True),
      )
  if 'code' not in flask.request.args:
    auth_uri = flow.step1_get_authorize_url()
    return flask.redirect(auth_uri)
  else:
    auth_code = flask.request.args.get('code')
    credentials = flow.step2_exchange(auth_code)
    flask.session['credentials'] = credentials.to_json()
    return flask.redirect(flask.url_for('index'))

def getService():
	credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
	http_auth = credentials.authorize(httplib2.Http())
	service = discovery.build('gmail', 'v1', http = http_auth)
	return service

@app.route('/sendMail',methods=['GET','POST'])
def sendMail():
	tempJnvIds = flask.request.args.get('jnvs')
	jnvids = tempJnvIds.split(", ")
	inspire_date = flask.request.args.get('inspire_date')

	resultText = ""
	service = getService()
	for jnvid in jnvids:
		cursor = database.cursor()
		sql = """SELECT a.`jnv_email`,a.`jnv_id`,b.`principal_name`,b.`principal_gender` \
				FROM `jnv_info` a, `principal_info` b \
				WHERE a.`jnv_id` = b.`principal_jnv` AND jnv_id = %s"""
		try:
   			cursor.execute(sql,int(jnvid))
   			numrows = cursor.rowcount
   			if(numrows != 1):
   				print "some error occured"
   				continue
   			else:
   				result = cursor.fetchone()
   				to_mail = result[0]
   				from_mail = 'dnjha240@gmail.com'
   				message_body =  ""
   				if(result[3] == 1):
   					message_body += "Dear "+result[2]+" Sir,\n"
   				else:
   					message_body += "Dear "+result[2]+" Madam,\n"

   				message_body += "We want to organise an inspire session in your school. Allow us."	
   				message_subject = "Permission to conduct Inspire Session on " + str(inspire_date)

   				message = createDraft.CreateMessage(from_mail,to_mail,message_subject,message_body)
  				sentMail = createDraft.sendMessage(service,'me',message)
  				thread_id = sentMail["threadId"]
  				print result[1]

  				inspire_add_sql = "INSERT INTO `inspire_info`( `inspire_jnv`, `step_1` , `inspire_date`) VALUES (%s,%s,%s)"
  				try:
  					cursor.execute(inspire_add_sql,(int(result[1]),50,inspire_date))
  					database.commit()
  					inspire_id = cursor.lastrowid
  					print "inspire_id " + str(inspire_id)
  					mail_add_sql = "INSERT INTO `mail`(`inspire_id`, `thread` ,`mail_type`) VALUES (%s,%s,%s)"
  					try:
  						cursor.execute(mail_add_sql,(int(inspire_id),thread_id,1))
  						database.commit()
  					except MySQLdb.Error, e:
  						resultText += "MySQL Error [%d]: %s" % (e.args[0], e.args[1])

  				except MySQLdb.Error, e:
  					resultText += "MySQL Error [%d]: %s" % (e.args[0], e.args[1])

  				resultText +=  json.dumps(result,ensure_ascii=False)
   		except MySQLdb.Error, e:
			resultText += "MySQL Error [%d]: %s" % (e.args[0], e.args[1])

   	return resultText   

@app.route('/getThread',methods=['GET','POST'])
def getThread(thread_id):
	output = {}
	# thread_id = "154042973386ec60"
	service = getService()
	user_id = 'me'
	try:
		thread = service.users().threads().get(userId=user_id, id=thread_id).execute()
		messages = thread['messages']
		# return json.dumps(messages)
		kaamWalaMsg = messages[-1]
		for header in kaamWalaMsg["payload"]["headers"]:
			if(header["name"].lower() == "from"):
				output["from"] = header["value"]

		output["msg"] = kaamWalaMsg["snippet"]

	except errors.HttpError as error:
		print('An error occurred: %s' % error)

	return output

@app.route('/getJnvNames',methods=['GET','POST'])
def getJnvNames():
	resultText = ""
	cursor = database.cursor()
	sql = "SELECT jnv_id,jnv_name FROM `jnv_info` WHERE 1"
	try:
		cursor.execute(sql)
		numrows = cursor.rowcount
		print numrows
		results = cursor.fetchall()
		for row in results:
			resultText += "<option value="+str(row[0])+">"+row[1]+"</option>"
	except MySQLdb.Error, e:
		resultText += "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
		return resultText

	return resultText

@app.route('/currentInspire',methods=['GET','POST'])
def currentInspire():
	resultText = ""
	cursor = database.cursor()
	sql = """SELECT b.`jnv_name`, a.`inspire_date`, a.`step_1`, a.`step_2`, a.`step_3`, a.`power_break`, c.`thread`,d.`principal_contactNo`, a.`inspire_id` \
 		FROM `inspire_info` a, `jnv_info` b, `mail` c , `principal_info` d\
 		WHERE a.`inspire_jnv` = b.`jnv_id` AND c.`inspire_id` = a.`inspire_id` AND d.`principal_jnv` = b.`jnv_id` AND c.`mail_type` = 1 LIMIT 5"""
	try:
		cursor.execute(sql)
		numrows = cursor.rowcount
		print numrows
		results = cursor.fetchall()
		for row in results:
			thread_info = getThread(row[6])
			resultText += "<div class='inspire_wrapper'>"
			resultText += "<h2 class='inspireHeader'>Inspire at JNV " + str(row[0]) + " on "+ str(row[1]) +" </h2>"

			# step 1 starts here
			resultText += "<div class='step_1'>"
			if(row[2] >= 50):
				resultText += "<input type='checkbox' checked='checked' disabled>"
				resultText += "<span> Mail sent to JNV </span>"
			else:
				resultText += "<span> Mail is not sent to JNV </span>"
			if("from" in thread_info):
				resultText += "<span> Last msg by : "+ thread_info["from"] + "</span>"
			if("msg" in thread_info):
				resultText += "<span> Last msg : " + thread_info["msg"] + "</span>"
			resultText += "<span>Princiapl Contact : "+str(row[7])+"</span>"
			if(row[2] == 100):
				resultText += "<input type='checkbox' checked='checked' disabled>"
				resultText += "<span>Confirmed visit to JNV</span>"
			else:
				resultText += "<input type='checkbox' disabled>"
				resultText += "<button class='confirm_step1_button'>Confirm</button>"
				resultText += "<form class='confirm_step1_form'>"
				resultText += "<input type='hidden' name='inspire_id' value='"+str(row[8])+"'>"
				resultText += "<span>Inspire on <span>" 
				resultText += "<input class='inspire_date_step1' name='inspire_date_step1' type='text' value='"+str(row[1])+"'>"
				resultText += "<input type='radio' name='confirm_method' value='call' checked>By Call<br>"
				resultText += "<input type='radio' name='confirm_method' value='mail'>By Mail<br>"
				resultText += "<input type='radio' name='confirm_method' value='other'>Others<br>"
				resultText += "<textarea name='comment'>Comment</textarea>"
				resultText += "<input type='submit' value='confirm' class='confirm_step1'>"
				resultText += "</form>"	
			resultText += "</div>"
			# step 1 ends
			# step 2 starts
			resultText += "<div class='step_2'>"
			if(row[2] == 100):
				if(row[3] == 0):
					resultText += "<a href='#' class='select_volunteer' id='"+str(row[8])+"'>Select volunteer</a>"
				elif(row[3] == 50):
					resultText += "<input type='checkbox' checked='checked' disabled>"
					resultText += "Mail sent to volunteers"
					resultText += "<button class='confirm_step2_button'>Confirm</button>"
					resultText += "<form class='confirm_step2_form'>"
					resultText += "<input type='hidden' name='inspire_id' value='"+str(row[8])+"'>"
					resultText += "<span>Confirm Inspire date on <span>" 
					resultText += "<input class='inspire_date_step2' name='inspire_date_step2' type='text' value='"+str(row[1])+"'>"
					resultText += "<input type='radio' name='confirm_method' value='call' checked>By Call<br>"
					resultText += "<input type='radio' name='confirm_method' value='mail'>By Mail<br>"
					resultText += "<input type='radio' name='confirm_method' value='other'>Others<br>"
					resultText += "<textarea name='comment'>Comment</textarea>"
					resultText += "<input type='submit' value='confirm' class='confirm_step2'>"
					resultText += "</form>"
				else:
					resultText += "<input type='checkbox' checked='checked' disabled>"
					resultText += "Mail sent to volunteers"
					resultText += "<input type='checkbox' checked='checked' disabled>"
					resultText += "Visit confirmed"
			else:
				resultText += "<p>Nothing Here</p>"
			resultText += "</div>"
			# step 2 ends
			# step 3 starts
			resultText += "<div class='step_3'>"
			if(row[2] == 100 and row[3] == 100):
				pass
			else:
				resultText += "<p>Nothing Here</p>"
			resultText += "</div>"
			# step 3 ends
			if(row[5] == 0):
				resultText += "<button class='addPowerBreak'>Add Power Break</button>"
			else:
				resultText += "<button class='removePowerBreak'>Remove Power Break</button>"

			resultText += "</div>"
	except MySQLdb.Error, e:
		resultText += "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
		return resultText

	return resultText

@app.route('/preview',methods=['GET','POST'])
def preview():
	tempJnvIds = flask.request.args.get('jnvs')
	jnvids = tempJnvIds.split(", ")
	inspire_date = flask.request.args.get('inspire_date')
	
	resultText = ""
	for jnvid in jnvids:
		cursor = database.cursor()
		sql = """SELECT a.`jnv_email`,a.`jnv_id`,b.`principal_name`,b.`principal_gender` \
				FROM `jnv_info` a, `principal_info` b \
				WHERE a.`jnv_id` = b.`principal_jnv` AND jnv_id = %s"""
		try:
   			cursor.execute(sql,int(jnvid))
   			numrows = cursor.rowcount
   			if(numrows != 1):
   				print "some error occured"
   				continue
   			else:
   				result = cursor.fetchone()
   				to_mail = result[0]
   				from_mail = 'dnjha240@gmail.com'
   				message_subject = "Inspire Session on " + inspire_date
   				message_body =  ""
   				if(result[3] == 1):
   					message_body += "Dear "+result[2]+" Sir,\n"
   				else:
   					message_body += "Dear "+result[2]+" Madam,\n"
   				message_body += "We want to conduct a session in ur school.\n Thanks."
   				resultText += "<div class='preview_mail_div'>"
   				resultText += "<form method='POST' class='preview_mail'>"
   				resultText += "<input type='hidden' name='jnv_id' value='"+jnvid+"'>"
   				resultText += "<input type='hidden' name='inspire_date' value='"+inspire_date+"'>"
   				resultText += "to_mail : "
   				resultText += "<input type='text' name='to_mail' value='"+to_mail+"'><br>"
   				resultText += "from_mail : "
   				resultText += "<input type='text' name='from_mail' value='"+from_mail+"'><br>"
   				resultText += "subject : "
   				resultText += "<input type='text' name='message_subject' value='"+message_subject+"'><br>"
   				resultText += "message_body : "
   				resultText += "<textarea name='message_body'>"+message_body+"</textarea>"
   				resultText += "<input type='submit' value='send mail'>"
   				resultText += "</form>"
   				resultText += "</div>"

   		except MySQLdb.Error, e:
			resultText += "MySQL Error [%d]: %s" % (e.args[0], e.args[1])

	return resultText

@app.route('/previewVolunteerMail',methods=['GET','POST'])
def previewVolunteerMail():
	tempVolunteerIds = flask.request.args.get('volunteers')
	volunteers = tempVolunteerIds.split(", ")

	resultText = ""
	for volunteer in volunteers:
		cursor = database.cursor()
		sql = """SELECT `volunteer_id`, `volunteer_name`, `volunteer_email` \
			FROM `volunteer_info` WHERE `volunteer_id` = %s"""
		try:
   			cursor.execute(sql,int(volunteer))
   			numrows = cursor.rowcount
   			if(numrows != 1):
   				print "some error occured"
   				continue
   			else:
   				result = cursor.fetchone()
   				to_mail = result[0]
   				from_mail = 'dnjha240@gmail.com'
   				message_subject = "Inspire Session on "
   				message_body =  ""

   		except MySQLdb.Error, e:
			resultText += "MySQL Error [%d]: %s" % (e.args[0], e.args[1])

	return resultText

@app.route('/sendPreviewedMail',methods=['GET','POST'])
def sendPreviewedMail():
	to_mail = flask.request.args.get('to_mail')
	from_mail = flask.request.args.get('from_mail')
	message_subject = flask.request.args.get('message_subject')
	message_body = flask.request.args.get('message_body')
	jnv_id = flask.request.args.get('jnv_id')
	inspire_date = flask.request.args.get('inspire_date')

	cursor = database.cursor()
	service = getService() 
	message = createDraft.CreateMessage(from_mail,to_mail,message_subject,message_body)
  	sentMail = createDraft.sendMessage(service,'me',message)
  	thread_id = sentMail["threadId"]
  	print thread_id

  	resultText = ""

  	inspire_add_sql = "INSERT INTO `inspire_info`( `inspire_jnv`, `step_1` , `inspire_date`) VALUES (%s,%s,%s)"
  	try:
  		cursor.execute(inspire_add_sql,(jnv_id,10,inspire_date))
  		database.commit()
  		inspire_id = cursor.lastrowid
  		print "inspire_id " + str(inspire_id)
  		mail_add_sql = "INSERT INTO `mail`(`inspire_id`, `thread`,mail_type) VALUES (%s,%s,%s)"
  		try:
  			cursor.execute(mail_add_sql,(int(inspire_id),thread_id,1))
  			database.commit()
  			resultText += "Inspire added"

  		except MySQLdb.Error, e:
  			resultText += "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
			return resultText

  	except MySQLdb.Error, e:
  		resultText += "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
		return resultText

	return resultText

@app.route('/confirm_step1',methods=['GET','POST'])
def confirm_step1():
	inspire_date = flask.request.args.get('inspire_date')
	inspire_id = flask.request.args.get('inspire_id')
	comment = flask.request.args.get('comment')
	cursor = database.cursor()
	resultText = ""
	sql = "UPDATE `inspire_info` SET `inspire_date`=%s,`step_1`= %s ,`comment`=%s WHERE `inspire_id` = %s"
	try:
		cursor.execute(sql,(inspire_date,100,comment,int(inspire_id)))
  		database.commit()
  		resultText += "Added"
	except MySQLdb.Error, e:
		resultText += "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
		return resultText
	
	return resultText

@app.route('/getVolunteers',methods=['GET','POST'])
def getVolunteers():
	resultText = ""
	cursor = database.cursor()
	sql = "SELECT `volunteer_id`, `volunteer_name` FROM `volunteer_info` WHERE 1"
	try:
		cursor.execute(sql)
		numrows = cursor.rowcount
		if(numrows > 0):
			results = cursor.fetchall()
			for row in results:
				resultText += "<option value='"+str(row[0])+"'>"+row[1]+"</option>"
	except MySQLdb.Error, e:
		resultText += "MySQL Error [%d]: %s" % (e.args[0], e.args[1])

	return resultText
  	

if __name__ == '__main__':
  import uuid
  app.secret_key = str(uuid.uuid4())
  app.debug = True
  app.run()