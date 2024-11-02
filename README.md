PROJECT - INSURANCE WORKFLOW MANAGEMENT by AISHWARYA GIRISH MENON & ADITHI S

# Insurance Workflow Management System

## Overview
The Insurance Workflow Management System (IWMS) is a comprehensive web application designed to streamline the management of insurance policies, claims, and customer interactions while improving the efficiency and security of insurance workflows. The application provides seamless features such as user account creation, policy management, real-time alerts, customer feedback analysis, and fraud detection. Built using Python, HTML, and CSS, IWMS integrates machine learning (ML) and natural language processing (NLP) to offer a reliable, intelligent solution for insurance companies to enhance customer experience and operational security.

## Features

### 1. User Account Management
   - **User Registration and Login**: Users can register and log in, creating personalized accounts with secure credentials.
   - **Profile Management**: Users can view and manage their account information, with a navigation bar for easy access across the application.
   - **QR Code Verification**: Each policy is verified through a QR code, ensuring data security and authenticity.

### 2. Policy Management
   - **Policy Registration**: Users can explore various insurance policies (e.g., Car, Bike, Travel, Health, Business) and select options based on their needs.
   - **Detailed Forms**: Each policy type has a specific form to collect relevant information (e.g., car model, health conditions).
   - **Policy Overview**: Registered policies are displayed with key details, and users can initiate claims directly from their account dashboard.
   - **Real-time Notifications**: SMS alerts are sent to users when new policies are created, claims are submitted, and renewals or expirations are upcoming.

### 3. Coverage Details
   - **Comprehensive Information**: Users have access to detailed descriptions of each insurance policy type, including coverage details, inclusions, and exclusions.
   - **Centralized Info Centre**: All coverage information is accessible through an Info Centre, with consistent visual styling to ensure clarity.

### 4. Customer Feedback and Satisfaction Detection
   - **Feedback Collection**: Customers can submit feedback through a dedicated support interface.
   - **NLP-Based Sentiment Analysis**: Feedback is analyzed with TextBlob, an NLP library, to detect sentiment (positive, neutral, negative).
   - **Feedback Management**: Customer satisfaction is categorized based on feedback sentiment, allowing for efficient handling of support cases and follow-up.

### 5. Alert System
   - **Policy Creation Alerts**: SMS notifications are sent to users upon successful policy creation.
   - **Claim Status Notifications**: When a claim is processed, users receive updates via SMS.
   - **Expiration Reminders**: Automatic alerts are sent to users when their policies are nearing expiration, enabling timely renewals.
   - **Twilio Integration**: Twilio API is integrated for reliable SMS delivery, ensuring secure and instant communication with users.

### 6. Claim Processing and Fraud Detection
   - **Claim Collection**: Users can submit claims for their policies, which are stored and managed in the application’s database.
   - **Random Forest Classifier for Fraud Detection**: A machine learning model trained on insurance data identifies potential fraudulent claims by analyzing claim patterns and flagging suspicious entries.
   - **Policy Data Management**: All claim and policy updates are saved in JSON format, enhancing data accessibility and integrity.
   - **QR Code Generation**: QR codes are generated for each policy, offering an added layer of security for policy validation.

## Technical Specifications

### Libraries and Frameworks
- **Python**: Primary programming language for back-end logic, ML model training, and NLP processing.
- **HTML/CSS**: Front-end languages for structuring and styling the user interface.
- **OpenCV**: Used for image processing and handling any image-based requirements.
- **TensorFlow**: Facilitates the development of ML models, particularly the fraud detection model.
- **TextBlob**: NLP library used for sentiment analysis in customer feedback.
- **Twilio API**: Integrates SMS functionality to send real-time alerts to users.
- **LabelImg**: Image annotation tool used for creating labeled datasets for any visual data processing.

### Machine Learning
- **Random Forest Classifier**: Trained model used to detect fraudulent claims based on historical data. The classifier flags suspicious entries, which can be reviewed by administrators for further action.

### Data Storage and Processing
- **JSON**: Used to store policy and claim information in a structured format, ensuring efficient data retrieval and updates.
- **Database Interaction**: The system retrieves, stores, and updates user-specific policy information to maintain accurate records and provide up-to-date notifications.

## Usage

### User Journey
1. **Account Creation**: Users start by creating an account, with options to register or log in if they are returning users.
2. **Policy Selection**: After login, users can browse policy options and fill out forms to register their chosen policy.
3. **Claim Submission**: Users can submit claims on their policies and receive real-time notifications regarding their claim status.
4. **Feedback Submission**: Users can provide feedback, which is automatically analyzed for sentiment to help improve customer experience.
5. **Alerts**: SMS notifications inform users about policy updates, upcoming renewals, and other important actions.
6. **Policy Verification**: Users can verify policies using the generated QR code, ensuring security and authenticity.

### Developer and Management Interaction
- **User Information Management**: Developers can access user information and feedback to manage operations and enhance service quality.
- **Feedback Analysis**: Negative feedback triggers alerts to management, allowing for quick resolution of user issues.
- **Fraud Detection**: The fraud detection model identifies potentially fraudulent claims, enabling administrators to take necessary action.

## Installation and Setup
1. Clone this repository.
2. Install the required libraries with `pip install -r requirements.txt`.
3. Configure the Twilio API with your credentials for SMS functionality.
4. Run the application server using `python app.py`.
5. Access the application through `http://localhost:5000` in your web browser.
