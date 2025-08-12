# AWS Deployment Guide: Personal Expense Tracker

This guide explains how to deploy your Flask-based Personal Expense Tracker on AWS using EC2 (for the app), RDS (for the database), and CloudWatch (for monitoring and alerts).

---

## 1. Launch an EC2 Instance
- Go to the AWS EC2 Console.
- Click **Launch Instance** and select an Ubuntu Server (e.g., 22.04 LTS).
- Choose an instance type (t2.micro is free tier eligible).
- Create or select a key pair for SSH access.
- Configure the security group:
  - Allow **SSH (22)** from your IP.
  - Allow **HTTP (80)** from anywhere (0.0.0.0/0).
  - (Optional) Allow **TCP 5000** for direct Flask access.
- Launch the instance.

## 2. Connect to Your EC2 Instance
- Download your key pair (.pem) if you haven't already.
- Set permissions and connect:
  ```bash
  chmod 400 your-key.pem
  ssh -i your-key.pem ubuntu@<EC2_PUBLIC_IP>
  ```

## 3. Install System Packages
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip python3-venv git nginx -y
```

## 4. Clone Your Project
```bash
git clone <your-repo-url>
cd ExpenseTrackerApp
```

## 5. Set Up Python Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 6. Set Up AWS RDS (MySQL or PostgreSQL)
- Go to the AWS RDS Console.
- Create a new database instance (MySQL or PostgreSQL).
- Note the **endpoint**, **username**, **password**, and **database name**.
- In RDS security group, allow inbound traffic from your EC2 instance (add EC2's security group as a source).

## 7. Configure Environment Variables
- On EC2, create a `.env` file in your project root:
  ```env
  FLASK_CONFIG=production
  SECRET_KEY=your-secret-key
  DATABASE_URL=mysql+pymysql://<username>:<password>@<rds-endpoint>:3306/<dbname>
  ```
  *(Adjust for PostgreSQL if needed)*

## 8. Initialize the Database
- If using Flask-Migrate:
  ```bash
  flask db upgrade
  ```
- Or, if your app auto-creates tables:
  ```bash
  python run.py
  ```

## 9. Run the Flask App with Gunicorn
```bash
pip install gunicorn
# Start the app (use the correct app object if not 'app')
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

## 10. Set Up Nginx as a Reverse Proxy
- Create a new Nginx config (e.g., `/etc/nginx/sites-available/expense_tracker`):
  ```nginx
  server {
      listen 80;
      server_name _;

      location / {
          proxy_pass http://127.0.0.1:5000;
          proxy_set_header Host $host;
          proxy_set_header X-Real-IP $remote_addr;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          proxy_set_header X-Forwarded-Proto $scheme;
      }
  }
  ```
- Enable the config and restart Nginx:
  ```bash
  sudo ln -s /etc/nginx/sites-available/expense_tracker /etc/nginx/sites-enabled/
  sudo nginx -t
  sudo systemctl restart nginx
  ```

## 11. Set Up CloudWatch Monitoring & Alerts
- In AWS Console, go to **CloudWatch**.
- Create alarms for EC2 (CPU, memory, disk) and RDS (CPU, connections, storage).
- Set up notifications (email/SNS) for alarms.
- (Optional) Install CloudWatch Agent on EC2 for detailed metrics:
  ```bash
  sudo apt install amazon-cloudwatch-agent -y
  # Configure as per AWS documentation
  ```

## 12. Access Your Application
- Open your browser and go to `http://<EC2_PUBLIC_IP>`
- Your app should be live!

---

**Tips:**
- Always keep your `.env` and secrets private.
- Use a domain name and SSL (Let's Encrypt) for production.
- Regularly monitor CloudWatch for alerts and performance.

---

This guide covers the full deployment pipeline for your Flask app with AWS infrastructure and monitoring.
