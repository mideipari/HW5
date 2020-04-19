import random
import string
import time


from locust import HttpLocust, between, TaskSequence, seq_task

min_set_size = 1
max_set_size = 10
number_of_keys = 10
keys = []


def random_key():
    length = random.randint(min_set_size, max_set_size)
    value = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    keys.append(value)


class WebsiteTasks(TaskSequence):
    for i in range(number_of_keys):
        random_key()

    @seq_task(1)
    def put(self):
        for i in range(number_of_keys):
            self.client.put("http://localhost:8080/" + str(i) + "/" + keys[i])

    @seq_task(2)
    def get(self):
        key = random.randint(0, number_of_keys)
        self.client.get("http://localhost:8080/" + str(key))

    @seq_task(3)
    def delete(self):
        key = random.randint(0, number_of_keys)
        self.client.delete("http://localhost:8080/" + str(key))



class WebsiteUser(HttpLocust):
    task_set = WebsiteTasks
    wait_time = between(10, 15)
