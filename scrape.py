from bs4 import BeautifulSoup
import lxml
import requests

base_page = "https://courses.cs.washington.edu/courses/cse333/25au/"
response = requests.get("https://courses.cs.washington.edu/courses/cse333/25au/schedule.html")
index = 0
# raises error if unsuccessful response
response.raise_for_status()
soup = BeautifulSoup(response.content, 'lxml')
days = soup.select('.sched-day')
for day in days: 
    # get the first assignment link on each day row 
    assignment = day.select_one(".sched-assignment-link")
    if assignment is not None:
        link = base_page + str(assignment["href"])
        print(link)
        with open(str(index) + ".txt", "w") as file:
            file.write(requests.get(link).text) 
            index += 1
#     context.write(soup.decode())