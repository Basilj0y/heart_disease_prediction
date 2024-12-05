Heart Disease Prediction
This project predicts the likelihood of heart disease based on patient data using a machine learning model. It is implemented as a Django web application where users can input medical information and receive predictions in real time.


Features
User-friendly interface to input patient details.
Real-time heart disease prediction using a trained machine learning model.
Encoded and decoded results for better interpretability.
Hosted on a web platform for accessibility


Technologies Used
Programming Language: Python
Framework: Django
Machine Learning: Scikit-learn
Frontend: HTML, CSS, Bootstrap
Notebook Environment: Jupyter Notebook(for data analysis and model training)



Project Features

User Authentication
Registration and login functionality with custom user profiles.
Secure password reset with OTP-based verification.

Health Data Input
Users can input health-related metrics such as height, weight, cholesterol levels, blood sugar levels, and more through an intuitive form.


Machine Learning Prediction
Predicts the likelihood of heart disease using a trained K-Nearest Neighbors (KNN) model.
Handles categorical data with one-hot encoding and scales input features for accurate predictions.

Result Display
Presents prediction results on a user-friendly webpage.
Allows users to start a new prediction or finalize the current one.

Admin Dashboard
A separate interface for administrators to view patient data and manage the system.

User Interaction
Users access the application via the homepage.
They log in or register to enter their details.

Prediction Form
Health metrics are submitted via a form, and the backend processes the data.

Model Processing
Data is preprocessed (e.g., scaled and encoded) to fit the ML model's input requirements.
The KNN model generates a prediction.

Result Presentation
The prediction is displayed on a results page with options to redo 