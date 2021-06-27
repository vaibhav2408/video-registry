# video-registry

### Clone the project:

	1) cd ~
	2) git clone git@github.com:vaibhav2408/video-registry.git
	3) cd video-registry

### Pre-requisites:

	1) Run - sudo vi /var/keys.txt
	2) Add the valid API key(s) to the file (each line contains 1 api key, no comma needed at the end of the line)
        Example of file content-
            <API-KEY-1>
            <API-KEY-2>
            ...
	3) Ensure that the ports 5000 & 9200 are NOT in use already

### To start the container init & the service
    
    chmod +x run.sh
    ./run.sh
    
    Note:
    This will perform the following actions:
      1) Download & run the Elasticsearch:7.13.2 container
      2) Build the app docker container
      3) Run the project container

### View the APIs

    Open the preffered view in your browser:
        1) Interactive view: http://0.0.0.0:5000/docs/
        2) Non-interactive view - http://0.0.0.0:5000/redoc/

#### APIS

     1) To get all the stored videos:
         http://0.0.0.0:5000/videos-registry/v1/collections?limit=200&offset=0
         
        NOTE:
            You can set the limit & offset as per your choice
    
     2) To query the stored data:
         http://0.0.0.0:5000/videos-registry/v1/search?limit=50&offset=0&query=football player
         
        NOTE:
            query: The search string
            You can set the limit & offset as per your choice


### Development summary
    Programming language: python (version: 3.8 or above) 
    Webframework: FastAPI
    Dependency management: Poetry
    Database: Elasticsearch

    * The project is dockerized
    * APIs for fetching & searching all stored videos
    * A background task to fetch newly published videos 
    * Support for multiple API keys
    * Search capability enabled on the video's Title/Description fields

### Developer Notes

    1) Check code linting issues:
        poetry run lint
    
    2) Fix code linting issues:
        poetry run fix-lint
    
    3) Run code locally: 
        a) install poetry: pip3 install poetry
        b) install the required packages: poetry install
        c) Update the elasticsearch hostname accordingly at (app/core/config.py:41)
        d) run the service: poetry run
    
    4) To add new dependancy to the project:
        a) poetry add <module-name>

    5) To add new dev dependancy to the project:
        a) poetry add -D <module-name>

    6) Build new docker image:
        poetry run build
