# uploader

pre-install： yarn install, pip install aiofiles, pip install -U scikit-learn scipy matplotlib 
backend start ：cd backend run node server.js
front end start ： yarn start



# FastAPI 
backend start: uvicorn backend.main:app --reload 

# Changes
11/05: backend port is changed from 8080 to 8000. 



# Example Input
- Table to impute: rail_ridership
- Column to impute: time_period_id
- Input query: SELECT * FROM rail_ridership
- Foreign keys: line_id:lines,line_id; station_id:stations,station_id; time_period_id:time_periods,time_period_id


