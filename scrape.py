from datetime import date, timedelta
from bs4 import BeautifulSoup
import lxml
import requests

base_page = "https://courses.cs.washington.edu/courses/cse333/25au/"
response = requests.get(
    "https://courses.cs.washington.edu/courses/cse333/25au/schedule.html"
)
# raises error if unsuccessful response
response.raise_for_status()


#     context.write(soup.decode())
# fetch all upcoming tasks in the specified timespan from course pages
def get_assignments_in_timespan(timespan: timedelta):
    index = 0
    end_day = date.today().__add__(timespan)

    soup = BeautifulSoup(response.content, "lxml")
    days = soup.select(".sched-day")
    for day in days:
        # get the first assignment link on each day row
        assignment = day.select_one(".sched-assignment-link")
        if assignment is not None:
            link = base_page + str(assignment["href"])
            print(link)
            assignment_soup = BeautifulSoup(requests.get(link).content, "lxml")
            # find all bold tags - need to search for due after
            due_date = assignment_soup.find_all("b")
            
            print(due_date)
            index += 1



if __name__ == "__main__":
    get_assignments_in_timespan(timedelta(1))

