from flask import Flask, request, make_response, jsonify
import requests
import PricePrediction as pricePred
import AppointmentScheduler as scheduler
import propertySearcher as ps

location = ""
bedroom = 0
size = 0
level = ""
budget = 0
email = ""
name = ""

preferredClusterCount = [0,0,0,0,0,0,0]
firstPreferredCluster = 99
secondPreferredCluster = 99
thirdPreferredCluster = 99
preference1 = 99
preference2 = 99
preference3 = 99

propertyID = ""
projectName = ""
address = ""
recommendedOfferPrice = 0

app = Flask(__name__)

def calculatePreference():

	count = 0
	for i in range (len(preferredClusterCount)):
		if preferredClusterCount[i] > count:
			count = preferredClusterCount[i]
			firstPreferredCluster = i

	count = 0
	for i in range (len(preferredClusterCount)):
		if preferredClusterCount[i] > count and i != firstPreferredCluster:
			count = preferredClusterCount[i]
			secondPreferredCluster = i
			
	count = 0
	for i in range (len(preferredClusterCount)):
		if preferredClusterCount[i] > count and i != firstPreferredCluster and i != secondPreferredCluster:
			count = preferredClusterCount[i]
			thirdPreferredCluster = i  

def updatePreference(preference):
	if preference in ('A1','A2'):
		preferredClusterCount[0] += 1
	elif preference in ('B2','C3'):
		preferredClusterCount[1] += 1
	elif preference in ('A3','C5'):
		preferredClusterCount[2] += 1
	elif preference in ('B5','C4'):
		preferredClusterCount[3] += 1
	elif preference in ('A5','C1'):
		preferredClusterCount[4] += 1
	elif preference in ('B4','C2'):
		preferredClusterCount[5] += 1
	elif preference in ('A4','B1'):
		preferredClusterCount[6] += 1


@app.route('/', methods=['POST'])
def webhook():

	global location
	global bedroom
	global size
	global level
	global budget
	global email
	global name
	global propertyID
	global preference1
	global preference2
	global preference3
	global projectName
	global address
	global recommendedOfferPrice
	

	req = request.get_json(silent=True, force=True)
	intent_name = req["queryResult"]["intent"]["displayName"]

	if intent_name =="GiveLocation":
		location = req["queryResult"]["parameters"]['location']
		print(location)
		response_text = "How many bedrooms and how many square feet (roughly)?"
	elif intent_name =="GiveSize":
		bedroom = req["queryResult"]["parameters"]['bedroom']
		size = req["queryResult"]["parameters"]['size']
		response_text = "Low Floor, Mid Floor or High Floor?"
	elif intent_name =="GiveLevel":
		level = req["queryResult"]["parameters"]['level']
		response_text = "What is your budget (please provide in numeric digits only)"
	elif intent_name =="GiveBudget":
		budget = int(req["queryResult"]["parameters"]['budget'])
		response_text = "What is your name and email address?"
	elif intent_name =="GiveNameAndEmail":
		name = req["queryResult"]["parameters"]['name']  
		print(name)
		email = req["queryResult"]["parameters"]['email']
		response_text = f'Thank you {name}! Before I start searching for your ideal home, I like to find out a bit more about your preference. Please look through the pictures on the right and let me know the three you like the most (please key in the code).'
	elif intent_name =="GivePreference":
		preference1 = req["queryResult"]["parameters"]['preference1']
		preference2 = req["queryResult"]["parameters"]['preference2']
		preference3 = req["queryResult"]["parameters"]['preference3']
		updatePreference(preference1)
		updatePreference(preference2)
		updatePreference(preference3)
		calculatePreference()
		response_text = f'Noted your preference. I will search around and email the shortlisted properties to {email}'
		ps.get_property(email, name, firstPreferredCluster, secondPreferredCluster, thirdPreferredCluster, location, size, budget, bedroom, level)

	elif intent_name =="FeedbackInterestedProperty":
		propertyID = req["queryResult"]["parameters"]['propertyID'][-8:]
		print(f'{propertyID} (typre{type(propertyID)}')
		projectName, district, floorArea, floorNumber, address, preference1, preference2, preference3 = ps.getPropertyDetails(propertyID)

		updatePreference(preference1)
		updatePreference(preference2)
		updatePreference(preference3)
		calculatePreference()
		recommendedOfferPrice = pricePred.getOfferPrice(projectName,district,floorArea,floorNumber)
		response_text = f'Glad to hear that, just to let you know that the fair market price of this property is estimated at {recommendedOfferPrice}. Shall I proceed to arrange a viewing for you?'
	elif intent_name =="FeedbackInterestedProperty - yes":
		response_text = "I will proceed to arrange the earliest available viewing appointment based on your Google Calendar and email you a viewing appointment confirmation."
		scheduler.makeAppointment(email, name, projectName, address, recommendedOfferPrice)
		print(email)
		print(name)
		print(projectName)
		print(address)
		print(recommendedOfferPrice)
	else:
		response_text = "Unable to find a matching intent. Try again."
	return make_response(jsonify({'fulfillmentText': response_text}))

# ***************************
# WEBHOOK MAIN ENDPOINT : END
# ***************************

if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0', port=5000)


