# ALA2022Bookshelf

Github Repository for American Library Assocation Conference 2022 poster titled "Together Again: Combining Print and E-Books on a Virtual Shelf Using Machine Learning."

This poster was accepted and presented at the American Library Association 2022 Conference in Washington D.C. on Saturday, June 25th. The poster was presented
during the Session 1: The Collectors poster session of the conference, focusing on technologies and methods for improving collection efficiency and diversity.

The poster in slide form can be viewed at the following link: https://docs.google.com/presentation/d/1UZ3WI8sv6qYQslsV9gckGdmxAx4KhePzqRnhaToMdU4/edit#slide=id.g7c635b7db5_1_0

## Project Overview

This project originated from the question of how can eBooks be better integrated with physical library books in a collection. University libraries pay thousands of dollars for database and eBook subscriptions, but there are very few physical resources in the library building that allow students to browse those collections with the same ease of walking around in the library. 

In response, we set out to make a sample virtual bookshelf that would house both physical books and eBooks side by side. To accomplish this, we needed a system to catagorize eBooks using the same Library of Congress classification system that physical books are sorted by. A machine learning model was employed to learn the book classifications and sort new eBook data into a SQL database. From there, a html, css, and php website was made to be the prototype virtual bookshelf which pull records from the database and displays them in a visually appealing way.

It follows that the project can be divided into 2 key divisions:

```
1) eBook classification using machine learning.
2) The book/eBook display website
```

This project was done in collaboration and with supervision from Dr. Emily Darowski, former Psychology Subject librarian at Brigham Young University (https://www.linkedin.com/in/emily-darowski-37306824/). 

All code was written by Gregory Knapp. 

## Code Overview

Code is divided into two main folders based on the 2 part project division listed above: BookClassification and Website. 

BookClassificaiton contains the Jupyter notebooks that were used for training the various machine learning models as well as the input data that was scraped from the BYU Harold B. Library website. Additionally, the code used to connect to the SQL database and load all of the physical book and classified eBook data is contained in this folder.

Website contains the html, css, and php files needed to display the bookshelf in browser. 
