## 💡 Overview
In this project, I use supervised machine learning techniques to predict individual preferences for perfumes based on various attributes such as brand, release year, fragrance notes, and user ratings. The objective is to identify and quantify the factors that significantly influence preference decisions, enabling personalised fragrance recommendations.

## 🧠 ML Approaches
- **Classification Algorithms**: Use Logistic Regression to classify perfumes into preferred or not preferred categories.
- **Feature Engineering**: Extract and select significant features from fragrance notes using natural language processing (NLP) techniques, and encode categorical data for model ingestion.
- **Model Evaluation**: Employ LOOCV and metrics such as accuracy, F1-score, and AUC-ROC to evaluate model performance and ensure robustness.
- **Hyperparameter Tuning**: Apply grid search and random search to fine-tune model parameters for optimal performance.
  
## 👩🏻‍💻 Tech Stack
- **Python**: The core language used for implementing data processing, model building, and evaluation scripts.
- **Scikit-learn**: Provides a wide range of tools for machine learning model development, evaluation, and hyperparameter tuning.
- **Pandas & NumPy**: Essential for efficient data manipulation, cleaning, and numerical operations.
- **Matplotlib & Seaborn**: For generating insightful visualizations of the data and model results.
- **NLTK/SpaCy**: For processing and analysing the textual data within fragrance notes, aiding in feature extraction.
