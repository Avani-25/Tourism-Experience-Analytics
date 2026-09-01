🌍 **Tourism Experience Analytics**

Classification, Prediction, and Recommendation System for tourism data — built as an end-to-end data science project covering data cleaning, EDA, machine learning, and deployment.

---
📌 **Overview**

This project analyzes tourism transaction data to:

Predict the rating a user might give an attraction (Regression)
Classify a user's likely visit mode — Business, Couples, Family, Friends, Solo (Classification)
Recommend attractions based on user preferences and attraction similarity (Recommendation System)

All three are deployed together in an interactive Streamlit app.

---
🛠️ **Tech Stack**

Python · Pandas · Scikit-learn · Streamlit · Matplotlib/Seaborn · Excel/openpyxl

---
🤖 **Models**

Task	Model	                                    Key Metric	                                              Result
Regression (Rating)	                         Random Forest (tuned)	                                        R²	
Classification (Visit Mode)	                 Random Forest (balanced)	                                   Accuracy	
Recommendation (Collaborative)	                Item-based CF	                                             RMSE	
Recommendation (Content-Based)	               Type-similarity	                                      Consistency check

---
🔑 **Key Insights**

Nature & Wildlife Areas is the most-visited attraction type; Water Parks has the highest average rating.

Ratings skew heavily positive (4–5 stars) across nearly all visit modes and attraction types.

Visit mode has only a weak relationship with rating, making it a harder prediction target.

Only 30 of 1,698 catalog attractions have rating history — motivating a hybrid recommendation approach (collaborative + content-based).

---



