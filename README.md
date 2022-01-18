# ShaleProfile

I made this to demonstrate my skills relevant to the job description - I have put together a very basic web app in which I have created an API to fetch data from [U.S. Energey Information Administration](https://www.eia.gov/dnav/ng/ng_prod_shalegas_s1_a.htm). 

API documentation can be accessed at [Swagger Documentation](https://shale-gas-production.deta.dev/docs)

I have also built a simple web application to plot some graphs using API which is accessible on following link. [Web Dashboard](http://shaleprofile.eu-central-1.elasticbeanstalk.com/)


## Installation

There are two components in this repo:
- Rest Api
- Web Interface

After cloning this repository follow the installation instruction

### API 
```bash
cd /shale 
pip install -r requirements.txt
uvicorn main:app --reload
```

### Web App
```bash
cd /app 
pip install -r requirements.txt
python application.py
```

## Note
I am using FAST Api and Dash for the first time as I wanted to try, but also wanted to put together something quick to apply for the job ASAP.

There is room for improvement particularly in following areas:
- Error handling and logging
- DAOs (Data Access Objects) in API should be separated from Routers / endpoints
- Add generic sample objects in API documentation
- 