from locust import HttpUser, task, between
import json
import random

# 1. Add slower than usual sometimes. Why?
# 2. What causes the crash? decoder? no status code. File "calculator_rest_service.py"


# 50 USERS

# 90th percentile ADD: 11
# 90th percentile SUBTRACT: 12
# 90th percentile MULTIPLY: 10
# 90th percentile DIVIDE: 11

# Requests/second: 16,5

# ---------------------------------------

# 200 USERS

# 90th percentile ADD: 20
# 90th percentile SUBTRACT: 18
# 90th percentile MULTIPLY: 19
# 90th percentile DIVIDE: 18

# Requests/second: 65

# ---------------------------------------


# 250 USERS worked for a minute until failures started

# ---------------------------------------

# 400 users, 49% failures, 133 RPS

#   File "C:\Users\ollec\AppData\Local\Programs\Python\Python311\Lib\json\__init__.py", line 346, in loads
#     return _default_decoder.decode(s)
#            ^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "C:\Users\ollec\AppData\Local\Programs\Python\Python311\Lib\json\decoder.py", line 337, in decode
#     obj, end = self.raw_decode(s, idx=_w(s, 0).end())
#                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "C:\Users\ollec\AppData\Local\Programs\Python\Python311\Lib\json\decoder.py", line 355, in raw_decode
#     raise JSONDecodeError("Expecting value", s, err.value) from None
# Expecting value: line 1 column 1 (char 0)


class CalculatorUser(HttpUser):
    wait_time = between(2, 4)

    def on_start(self):
        pass

    def check_response_status(self, response, expected_status):
        if response.status_code != expected_status:
            response.failure(
                f"Expected status code {expected_status} but got {response.status_code}"
            )

    @task
    def add(self):
        data_sets = [
            (1, 1, 2),
            (2, 3, 5),
            (5, 7, 12),
        ]

        selected_data = random.choice(data_sets)

        add = {
            "operation": "add",
            "operand1": selected_data[0],
            "operand2": selected_data[1],
        }
        with self.client.post(
            "/calculator", catch_response=True, name="add", json=add
        ) as response:
            self.check_response_status(response, 200)
            response_data = json.loads(response.text)
            if not response_data["result"] == selected_data[2]:
                response.failure(
                    f"Expected result to be {selected_data[2]} but was {response_data['result']}"
                )

    @task
    def subtract(self):
        data_sets = [
            (1, 1, 0),
            (3, 2, 1),
            (22, 6, 16),
        ]

        selected_data = random.choice(data_sets)

        sub = {
            "operation": "subtract",
            "operand1": selected_data[0],
            "operand2": selected_data[1],
        }
        with self.client.post(
            "/calculator", catch_response=True, name="subtract", json=sub
        ) as response:
            self.check_response_status(response, 200)
            response_data = json.loads(response.text)
            if not response_data["result"] == selected_data[2]:
                response.failure(
                    f"Expected result to be {selected_data[2]} but was {response_data['result']}"
                )

    @task
    def multiply(self):
        data_sets = [
            (1, 4, 4),
            (3, 2, 6),
            (10, 6, 60),
        ]

        selected_data = random.choice(data_sets)

        multiply = {
            "operation": "multiply",
            "operand1": selected_data[0],
            "operand2": selected_data[1],
        }
        with self.client.post(
            "/calculator", catch_response=True, name="multiply", json=multiply
        ) as response:
            self.check_response_status(response, 200)
            response_data = json.loads(response.text)
            if not response_data["result"] == selected_data[2]:
                response.failure(
                    f"Expected result to be {selected_data[2]} but was {response_data['result']}"
                )

    @task
    def divide(self):
        data_sets = [
            (8, 4, 2),
            (32, 4, 8),
            (256, 16, 16),
        ]

        selected_data = random.choice(data_sets)

        divide = {
            "operation": "divide",
            "operand1": selected_data[0],
            "operand2": selected_data[1],
        }
        with self.client.post(
            "/calculator", catch_response=True, name="divide", json=divide
        ) as response:
            self.check_response_status(response, 200)
            response_data = json.loads(response.text)
            if not response_data["result"] == selected_data[2]:
                response.failure(
                    f"Expected result to be {selected_data[2]} but was {response_data['result']}"
                )

    @task
    def add2(self):
        data_sets = [
            (15, 30, 45),
            (523, 3, 526),
            (312, 123, 435),
        ]

        selected_data = random.choice(data_sets)

        add = {
            "operation": "add",
            "operand1": selected_data[0],
            "operand2": selected_data[1],
        }
        with self.client.post(
            "/calculator", catch_response=True, name="add", json=add
        ) as response:
            self.check_response_status(response, 200)
            response_data = json.loads(response.text)
            if not response_data["result"] == selected_data[2]:
                response.failure(
                    f"Expected result to be {selected_data[2]} but was {response_data['result']}"
                )


if __name__ == "__main__":
    from locust import run_single_user

    CalculatorUser.host = "http://127.0.0.1:5000"
    run_single_user(CalculatorUser)
