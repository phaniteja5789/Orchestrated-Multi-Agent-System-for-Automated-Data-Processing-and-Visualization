from langchain_community.utilities.requests import RequestsWrapper
import json
import psycopg2
from langchain.tools import BaseTool,StructuredTool,tool



@tool
def RequestAndInsertTool(state):

    '''
    Requests an endpoint "https://randomuser.me/api/" and returns the required information like Name,Gender,Country as a dictionary of the person as output 

    '''
    requests_wrapper = RequestsWrapper()

    information_url = "https://randomuser.me/api/"

    response = requests_wrapper.get(information_url)

    response_json = json.loads(response)

    response_dict = (dict)(response_json)

    query_dict = response_dict["results"][0]

    gender = query_dict["gender"]

    name = query_dict["name"]["first"] + " " + query_dict["name"]["last"]

    country = query_dict["location"]["country"]


    try:

        conn = psycopg2.connect(
        host="localhost",
        database="agent",
        user="postgres",
        password="Phaniteja5789@",
        port="5432"
        )

        # Create a cursor object
        cur = conn.cursor()

        # Create the table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS Person (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            gender VARCHAR(10),
            country VARCHAR(50)
        );
        """

        cur.execute(create_table_query)
        
        # Insert the data into the table
        cur.execute(
            "INSERT INTO Person (name, gender, country) VALUES (%s, %s, %s)",
            (name, gender,country)
        )

        conn.commit()
        return 0
    
    except Exception as e:
        print(e)
        return 100

