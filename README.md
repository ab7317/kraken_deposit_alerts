# kraken_deposit_alerts
This repository will fully build a server that will connect to the **kraken rest api**. The server will check the ednpoint **https://api.kraken.com/0/private/DepositStatus** every 5 minutes. Please check the **Kraken Documentation** for more details: https://docs.kraken.com/rest/#tag/Account-Data/operation/getTradeVolume. If there is any new deposits o changes the server will send an alert message to a **Telegram** chat. Following the repository will take you through setting up the aws instances, writing the code and setting up the telegram group.

# Setup
- This will use a **AWS EC2** instance
- You will need to use the **AWS CONSOLE** in the browser
- The instance should be type **t2.micro**
- It will need 1 elastic IP address
  
  # Creating the server
  - Login to the **AWS Console**
  - check in the top right corner your in the correct region
  - In the search bar search **EC2** click the first option
  - Navigate to the **Instances** tab
  - click **Launch instances** in the top right corner
  - Select the latest version of **ubuntu** for the **AMI**
  - Architecture must be **64-bit (x86)**
  - 
  
  # Adding Elastic IP to instance
  - Select **Elastic IPs** in the **EC2 Dashboard**
  - Select in the top right corner **Allocate Elastic IP address**
  - Once in the menu click **Allocate**
  - From the **Elastic IPs** page select the IP
  - In the **Actions** drop down in the top right click **Associate Elastic IP addresses**
  - You can go back to the **Instances** page and your instance should now have an elastic IP
