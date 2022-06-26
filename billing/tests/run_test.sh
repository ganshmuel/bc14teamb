#!/bin/bash
./billing/tests/checks.sh > ./billing/tests/test_results.txt
(python3 billing/tests/check_test_results.py) > ./billing/tests/test-log.txt