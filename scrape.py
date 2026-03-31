from datetime import date, timedelta
from bs4 import BeautifulSoup
import lxml
import requests

base_page = "https://courses.cs.washington.edu/courses/cse333/25au/"
response = requests.get(
    "https://courses.cs.washington.edu/courses/cse333/25au/schedule.html"
)
response.raise_for_status()


def get_assignments_in_timespan(timespan: timedelta):
    index = 0
    end_day = date.today().__add__(timespan)

    soup = BeautifulSoup(response.content, "lxml")
    days = soup.select(".sched-day")
    for day in days:
        assignment = day.select_one(".sched-assignment-link")
        if assignment is not None:
            link = base_page + str(assignment["href"])
            print(link)
            assignment_soup = BeautifulSoup(requests.get(link).content, "lxml")
            due_date = assignment_soup.find_all("b")

            print(due_date)
            index += 1


if __name__ == "__main__":
    get_assignments_in_timespan(timedelta(1))
