# kraken_deposit_alerts
This repository will fully build a server that will connect to the **kraken rest api**. The server will check the ednpoint *https://api.kraken.com/0/private/DepositStatus* every 5 minutes. Please check the **Kraken Documentation** for more details: *https://docs.kraken.com/rest/#tag/Account-Data/operation/getTradeVolume*. If there is any new deposits o changes the server will send an alert message to a **Telegram** chat. Following the repository will take you through setting up the aws instances, writing the code and setting up the telegram group.

# Setup
- This will use a **AWS EC2** instance
- You will need to use the **AWS CONSOLE** in the browser
- The instance should be type **t2.micro**
- It will need 1 elastic IP address
- This is assuming you have putty configured or can access the ssh service
  
  # Creating the server
  - Login to the **AWS Console**
  - Check in the top right corner your in the correct region
  - In the search bar search **EC2** click the first option
  - Navigate to the **Instances** tab
  - Click **Launch instances** in the top right corner
  - Select the latest version of **ubuntu** for the **AMI**
  - Architecture must be **64-bit (x86)**
  - Ensure instance type is set to **t2.micro**
  - For **Key pair** create a new one
  - Now select **Launch instance** on the right side
  - The instance may take some time
  
  # Adding Elastic IP to instance
  - Select **Elastic IPs** in the **EC2 Dashboard**
  - Select in the top right corner **Allocate Elastic IP address**
  - Once in the menu click **Allocate**
  - From the **Elastic IPs** page select the IP
  - In the **Actions** drop down in the top right click **Associate Elastic IP addresses**
  - You can go back to the **Instances** page and your instance should now have an elastic IP

  # Creating the Telegram group
  - Open telegram and search for **@botfather**
  - After activating **botfather** send it
  ```
  /newbot
  ```
  - It will prompt you for a series of information like names folllow its directions
  - Make sure you take the **token access** for your bot
  - You will add your **token** into the config.py file under **telegram_token**
  - You will need the **ID** but we first need to add the bot to our server
  - Once the bot is on the server we can get the ID, we will also add to config.py under **telegram_id**
  - This can be quite frustrating since the telegram api is slow
  - you will need to open a browser and navigate to the following page, replacing anything in <> for your own
  - *https://api.telegram.org/bot<telegram_token>/getUpdates*
  - you will need to refresh the page multiple times, you will see an ID for the bot but you need the ID for the group chat, they always start with -
  ```
  "my_chat_member"{"chat"{"id":<group_id>,"title":"BIG_TEST","type":"group","all_members_are_administrators":true}
  ```
- Once your output is looking like this you can put the **group_id** in the config file under **telegram_id**
- verify your server and bot is working run the file in config called telegram.py
- you should see a message from your bot on your group chat if it is working

# Configuration
- This sections assumes you have setup youe **AWS EC2 Instance** using **Ubuntu**
- This also assumes that you can login and connect to your instance via **SSH**
- It will go through setting up the required **Python** and **Service** scripts
- It will not go through the codes logic or maintanance
- You will need the servers ip to be whitelisted by kraken
- You will also need a set of relevant keys for the account

  # Setting up the directories
  - Connect to your new instance via **SSH**
  - we want to run the following commands to properly setup our directories for this server, also make sure you are in the correct directory, you can use the following command to make sure you are
  ```
  cd ~
  ```
  ```
  git --version
  ```
  - If you have git skip the next line, it will only install git on the server
  ```
  sudo apt install git
  ```
  - Verify the installtion with the above command
  - Next we need to clone the repository so we have everything
  ```
  git clone git@github.com:ab7317/kraken_deposit_alerts
  ```
  - We will want to navigate into the services directory
  ```
  cd ~/kraken_deposit_alerts/services
  ```
  - We will want to copy the service we have in there into the correct location so it can run properly
  - We will edit the file in the next section to ensure it is running
  ```
  sudo cp run_scripts.service /etc/systemd/system/
  ```

  # Configuring scripts
  - We will start with the configuration script
  ```
  sudo nano ~/kraken_deposit_alerts/config.py
  ```
  - In here you will need to add your **kraken_key kraken_secret telegram_token and telegram_id**
  - If you do not have all of this information please read through the repository again
  - Next we need to get our python script working, it will require some non standard modules
  - if pip is not installed run the following commands
  ```
  sudo apt-get update
  ```
  ```
  sudo apt-get install python3-pip
  ```
  ```
  pip install requests
  ```
  ```
  pip install pandas
  ```
  - we can now verify our script is working and out config is setup correctly
  ```
  cd ~/kraken_deposit_alerts
  ```
  ```
  python3 monitor.py
  ```
  - Once this script is running we will need to setup the service so the script can run without needing the server open
  ```
  sudo nano /etc/systemd/system/run_scripts.service
  ```
  - We will want to add the full path to the script not **~/** but **/home/<username>/kraken_deposit_alerts**
  - To start the service we run
  ```
  sudo systemctl start run_scripts.service
  ```
  ```
  sudo systemctl status run_scripts.service
  ```
  - If the service is running as expected we should be able to see the printed out from the file (should also be seeing telegram alerts as expected)
  - We can now set the server to run the service on start up so we dont need to worry about manualling starting it after a restart
  ```
  sudo systemctl enable run_scripts.service
  ```

# Code
  # Service file
  - the service file is a **.service**
  - this allows it to run a service on the server
  - if we point the path of the service to run our python script
  - then we wont need to be online for it to run and we can leave the server

  # Python script
  - There are 2 python files
  - confi.py and monitor.py
  - 
