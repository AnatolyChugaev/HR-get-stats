import math
from datetime import datetime
import requests

start_date = "2022-04-01T00:00:00+0000"
date_format = '%Y-%m-%dT%H:%M:%S+0000'
start_date_timestamp = datetime.strptime(start_date, date_format).timestamp()

# access_token = "uncomment and write your access token here"
tasks = {}
off = 0
while True:
    off += 100
    params = dict(
        limit='100',
        offset=str(off)
    )
    r = requests.get("https://www.hackerrank.com/x/api/v3/tests/1145944/candidates",
                     headers={"Authorization": "Bearer " + access_token},
                     params=params)
    print("code = " + str(r.status_code))
    data = r.json()["data"]

    for user in data:
        if user["status"] == -1:
            continue
        attempt_timestamp = datetime.strptime(user["attempt_starttime"], date_format).timestamp()
        if attempt_timestamp < start_date_timestamp:
            continue
        for task in user["questions"]:
            if task not in tasks:
                tasks[task] = []
            tasks[task].append((user["questions"][task], user["ats_state"]))
    if len(data) < 100:
        break
    # break

print(len(tasks))
for t in tasks:
    print(len(tasks[t]))

tasks_max_score = {}

for question in tasks:
    r = requests.get("https://www.hackerrank.com/x/api/v3/questions/" + question,
                     headers={"Authorization": "Bearer " + access_token})
    data = r.json()
    tasks_max_score[question] = (data["max_score"], data["name"])

print(tasks_max_score)

fully_solution_stats = {}

for task_id in tasks:
    all_cnt = len(tasks[task_id])
    full_cnt = 0
    pass_cnt = 0
    for res in tasks[task_id]:
        if res[0] == tasks_max_score[task_id][0]:
            full_cnt += 1
        elif res[1] == 19:
            pass_cnt += 1

    fully_solution_stats[tasks_max_score[task_id][1]] = (full_cnt, all_cnt, pass_cnt)

s = 0
for t in fully_solution_stats:
    s += fully_solution_stats[t][1]
    print(t + " " + str(math.trunc(fully_solution_stats[t][0] / fully_solution_stats[t][1] * 100)) + "% all = "
          + str(fully_solution_stats[t][1]) + " "
          + str(math.trunc(fully_solution_stats[t][2] / fully_solution_stats[t][1] * 100)) + "%")

print("all tasks were solved: " + str(s))
