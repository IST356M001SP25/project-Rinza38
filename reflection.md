# Reflection

Student Name:  Philip Cheuk
Student Email:  pcheuk@syr.edu

## Instructions

Reflection is a key activity of learning. It helps you build a strong metacognition, or "understanding of your own learning." A good learner not only "knows what they know", but they "know what they don't know", too. Learning to reflect takes practice, but if your goal is to become a self-directed learner where you can teach yourself things, reflection is imperative.

- Now that you've completed the assignment, share your throughts. What did you learn? What confuses you? Where did you struggle? Where might you need more practice?
- A good reflection is: **specific as possible**,  **uses the terminology of the problem domain** (what was learned in class / through readings), and **is actionable** (you can pursue next steps, or be aided in the pursuit). That last part is what will make you a self-directed learner.
- Flex your recall muscles. You might have to review class notes / assigned readings to write your reflection and get the terminology correct.
- Your reflection is for **you**. Yes I make you write them and I read them, but you are merely practicing to become a better self-directed learner. If you read your reflection 1 week later, does what you wrote advance your learning?

Examples:

- **Poor Reflection:**  "I don't understand loops."   
**Better Reflection:** "I don't undersand how the while loop exits."   
**Best Reflection:** "I struggle writing the proper exit conditions on a while loop." It's actionable: You can practice this, google it, ask Chat GPT to explain it, etc. 
-  **Poor Reflection** "I learned loops."   
**Better Reflection** "I learned how to write while loops and their difference from for loops."   
**Best Reflection** "I learned when to use while vs for loops. While loops are for sentiel-controlled values (waiting for a condition to occur), vs for loops are for iterating over collections of fixed values."

`--- Reflection Below This Line ---`

Working on the Electric Vehicle Population Analysis project allowed me to combine my interest in sustainability with the technical skills I've developed in data processing and visualization. The project involved building a complete data pipeline, from extracting raw EV registration data through an API, cleaning and transforming it with Pandas, to finally presenting insights through an interactive Streamlit dashboard. One of the biggest challenges was handling the geospatial data, particularly parsing the "POINT" strings into usable latitude and longitude coordinates. I overcame this by creating robust helper functions with thorough error handling, which I then validated through unit tests. The dashboard development pushed me to think about user experience, leading me to implement dynamic filters and responsive visualizations that adjust based on the selected data range. I'm particularly proud of how the map visualization automatically zooms based on data density and provides clear feedback when location data is missing.  

The project also reinforced the importance of writing modular, maintainable code. By structuring the project into distinct components, data extraction, transformation, and visualization. I was able to test each part independently and ensure reliability. If I were to expand this project, I'd integrate additional datasets like charging station locations to provide richer context, and explore machine learning techniques to forecast future EV adoption trends. This experience not only improved my technical abilities in Python and data analysis but also taught me how to turn raw data into meaningful, user-friendly insights. Most importantly, it showed me how powerful data visualization can be in telling compelling stories about real-world trends.