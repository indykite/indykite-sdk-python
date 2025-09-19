# IndyKite Python SDK spaces example

Create an AppSpace, an application, an application agent and get application agent credentials

## Requirements

* Python >= 3.10
* IndyKite account: Accounted created by logging in on <https://console.indykite.id/>
* Customer created on <https://console.indykite.id/>
* Service account created on <https://console.indykite.id/> under the above customer

## Installation

* Copy example to local environment
* In the spaces directory, run:

  ```sh
  pipenv install
  pipenv shell
  ```

* Credentials: export the file as env variable in CLI (setex for Windows)

  ```sh
  export INDYKITE_SERVICE_ACCOUNT_CREDENTIALS_FILE=path_to_service_account_file
  ```

* In spaces directory, run:

  ```sh
  flask run
  ```

* You should get:

  ```sh
  Running on http://127.0.0.1:5000
  ```
