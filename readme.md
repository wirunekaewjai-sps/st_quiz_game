# get started
```sh
# install dependencies from requirements.txt
pip install -r requirements.txt

# run the app locally
streamlit run streamlit_app.py
```

# create a local secret file for development on ".streamlit/secrets.toml"
```toml
[connections.snowflake]
account = "YOUR_ACCOUNT_IDENTIFIER"
user = "YOUR_USERNAME"
password = "YOUR_PASSWORD"
role = "SYSADMIN"
warehouse = "COMPUTE_WH"
database = "QUIZ_GAME"
schema = "PUBLIC"
```

# update network policy for allow your device to connect snowflake database
1. check and copy your current IP: https://www.whatismyip.com/
2. login to Snowflake UI
3. go to "Governance & security" > "Network policies"
4. create new network policy then create network rule and add your IP
5. network policy will not active by default then activate it by click on "..." button and select "Activate On Account"
