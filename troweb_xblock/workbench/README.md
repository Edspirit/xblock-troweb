# XBlock SDK Workbench compatible scenarios

## To run TrowebXBlock workbench scenarios

1. Install [XBlock SDK](https://github.com/openedx/xblock-sdk) in parent directory:

   ```bash
   git clone git@github.com:openedx/xblock-sdk.git -b v0.5.2 ../xblock-sdk
   ```

1. create a new virtual environment in xblock-sdk directory and activate it.
    ```bash
    virtualenv -p python3 .venv
    source .venv/bin/activated
    ```

1. install all dependencies for the xblock-sdk:
    ```bash
    make install
    ```


1. Make sure TrowebXBlock is installed into your environment:

   ```bash
   make dev-install
   ```

1. populate the database with the `migrate` command:
   ```bash
    (.venv) ../xblock-sdk/manage.py migrate
   ```

1. Run Workbench:

   ```bash
   (.venv) ../xblock-sdk/manage.py runserver
   ```

1. Go to <http://localhost:8000/> in your browser.