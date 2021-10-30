# Introduction 
TODO: Give a short introduction of your project. Let this section explain the objectives or the motivation behind this project. 

# Getting Started
TODO: Guide users through getting your code up and running on their own system. In this section you can talk about:
1.	Installation process
2.	Software dependencies
3.	Latest releases
4.	API references

# Build and Test
- There are 4 main folder in Hume-Chatbot:

	- backend
	
	- frontend
	
	- update/API_UPDATE_DATA
	
	- tmt_address-master

- To run all APIs, follow these requirements and commands:

	- There are 2 requirements files in folder "backend" and "tmt_address-master", need install all libraries dependencies by following command:
		
		> pip install -r requirements.txt
		
	- Then, set the directory for backend by command:
	
		> pip install -e .
		
	- These commands run all APIs for chatbot:
		
		- In folder "backend":
		 	
		> cd backend
		> python app.py
		
		- In folder "frontend":
		 	
		> cd frontend
		> npm start
		
		- In folder "update/API_UPDATE_DATA":
		 	
		> cd update/API_UPDATE_DATA
		> python api_update_product.py
		
		- In folder "tmt_address-master":
		 	
		> cd tmt_address-master
		> python app.py
		
- ** P/s: If need to a new create chatbot: **

	- Use Postman or alternative Postman tools to access API. 
	
	- Set input for API create-chatbot:
	
		- Method: POST
		
		- URL: http://{ip}:{port}/api/create-chatbot
		
			Example: http://localhost:5050/api/create-chatbot
		
		- Headers: 
			
			KEY: Content-Type
			
			VALUE: application/json
			
		- Body: select "raw" and add this json:
		
			> {
			"name":"hume",
			"address":"25 Nguyễn Minh châu phường phú trung tân phú hcm",
			"ship_provider":
			[
			    {
				"type":"GHN",
				"shopid":"1266853",
				"shoptoken":"zCV1eKl1Bdxg3fKG9XkyfJOrBOBHwNsFn1c0Vk"
			    }
			],
			"category":"shopping"
		    }
		    
	- Then, click "Send" button:
		
		- If create successfully, return "success_create_chatbot"
		
		- else return 500 error
		
		- if bot exists, return "duplicate"
		
		
	
	

# Contribute
TODO: Explain how other users and developers can contribute to make your code better. 

If you want to learn more about creating good readme files then refer the following [guidelines](https://docs.microsoft.com/en-us/azure/devops/repos/git/create-a-readme?view=azure-devops). You can also seek inspiration from the below readme files:
- [ASP.NET Core](https://github.com/aspnet/Home)
- [Visual Studio Code](https://github.com/Microsoft/vscode)
- [Chakra Core](https://github.com/Microsoft/ChakraCore)