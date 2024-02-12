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
  - Once the bot is on the server we can get the ID

# Configuration
- This sections assumes you have setup youe **AWS EC2 Instance** using **Ubuntu**
- This also assumes that you can login and connect to your instance via **SSH**
- It will go through setting up the required **Python** and **Service** scripts
- It will not go through the codes logic or maintanance
- You will need the servers ip to be whitelisted by kraken
- You will also need a set of relevant keys for the account

  # Setting up the directories
  - 
