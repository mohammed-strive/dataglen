# dataglen

Running the backend service...
To run a local instance, you will need to pull down the code and follow the steps. Their is currently no build for this. It will be remedied in a future commit.

1. pull the code.
2. Create Environment variables
  - FLASK_APP='app'
  - FLASK_ENV='development'
3. Run `flask init-db`
4. Run `flask run`
5. To access the `/api/v1/sensordata` apis, please register on `POST /api/v1/auth/register` with username and password.
4. Access the apis with a Basic Authorization header `Authorization: Basic BASE64ENCODEDSTRING`.

 
