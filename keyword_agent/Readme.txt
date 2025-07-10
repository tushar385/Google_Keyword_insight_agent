
# Keyword Agent

## Overview
The Keyword Agent is designed to find insights for a specific vertical using Google AdWords keyword data. It leverages Snowflake for data storage and retrieval, and provides a user-friendly interface through a Streamlit application.

## Setup Instructions

### 1. Update Snowflake Credentials
Before running the application, you need to update your Snowflake credentials. Open the `snowflake_config.py` file located in the `keyword_agent/agent_core/config` directory and replace the placeholder values with your actual Snowflake account details.



### 2. Set Up OpenAI API Key
You need to export your OpenAI API key in the terminal before running the application. Use the following command:
export OPENAI_API_KEY='your_openai_api_key'


### 3. Running the Application
You can run both the Keyword Agent and the Streamlit application using Docker. The commands to do so are specified in the `docker-compose.yml` file.

#### To run the Streamlit app: 
sudo docker-compose up --build streamlit


#### To run the Keyword Agent:
sudo docker-compose up --build agent



### 4. Results Storage
The results for each vertical are stored in the `insights` directory. You can find the output files there after running the functions.

## Additional Information
- Ensure you have the necessary permissions to access the Snowflake tables specified in your `snowflake_config.py`.

