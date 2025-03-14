import os
import json

test_results = []  

def save_results(result_file_path):
    os.makedirs(os.path.dirname(result_file_path), exist_ok=True)  
    with open(result_file_path, "w", encoding="utf-8") as f:
        json.dump(test_results, f, indent=4, ensure_ascii=False)

def add_test_result(name, response, expected_status, expected_body=None):
    test_results.append({
        "TestCase": name,
        "Status": response.status_code,
        "Expected": expected_status,
        "Pass": response.status_code == expected_status,
        "Body": response.json() if response.status_code == 200 else response.text if expected_body is None else expected_body
    })
