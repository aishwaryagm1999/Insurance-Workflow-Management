import re  # Feature -> Regular expressions (Used for text cleaning and pattern matching)
from textblob import TextBlob  

def clean(text):
    
    text = re.sub(r'http\S+', '', text)  # Feature -> Regular expressions (Removing URLs from the text)
    
    text = re.sub(r'[^A-Za-z\s]', '', text)  # Feature -> Regular expressions (Removing special characters and numbers)
    return text

def feedback(file_path):
    try:
        with open(file_path, 'r') as file:  # Feature -> Exception handling (Handling file not found error)
            feedbacks1 = file.readlines()  # Feature -> List (Storing each line of the file as an element in a list)

        if not feedbacks1:  # Feature -> List (Checking if list is empty)
            print("No feedback available.")
            return

        polarity = 0
        for feedback in feedbacks1:  # Feature -> Iterators (Iterating over each feedback)
            
            clean_feedback = clean(feedback)  # Feature -> Functions (Using a function to clean text)
            blob = TextBlob(clean_feedback)  
            polarity += blob.sentiment.polarity  # Feature -> Accessing polarity attribute from a dictionary-like object

        avg_polarity = polarity / len(feedbacks1)  # Feature -> List (Using the length of the list)
        
        if avg_polarity > 0.1:
            return "Positive Customer Satisfaction"
        elif avg_polarity < -0.1:
            return "Negative Customer Satisfaction"
        else:
            return "Neutral Customer Satisfaction"
    except FileNotFoundError:  # Feature -> Exception handling (Handling specific file not found exception)
        return "Feedback file not found."


result = feedback('feedback.txt')  # Feature -> Function with keyword arguments (Passing a file path as an argument)
print(result)
