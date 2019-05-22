This script will be used to parse the ISC sans malicious domains and format them in the correct way into
XML to be pushed into a CounterACT lists. Upon running it will start by deleting all list values and
uploading the most updated content from the endpoint (ISC)

    Requirements:
        Python 3: 	https://www.python.org/downloads/
		Forescout: 	- Create 3 lists with the following names: 
						- High Level Sensititivity (DShield)
						- Medium Level Sensititivity (DShield),
						- Low Level Sensititivity (DShield).
					- Create a WebAPI account
					
Change the following in the script

	- Update the /path/to/ for
		- delete.xml 
		- high.xml
		- med.xml
		- low.xml
	- Update the USERNAME@ACCOUNT , PASSWORD with the Forescout API creds created
		
