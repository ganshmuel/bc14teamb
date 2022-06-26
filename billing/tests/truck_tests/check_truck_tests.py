#------------- Compare output to expected output ----------
def main():
    test_file = open('billing/tests/truck_tests/tests_results.txt')
    while True:
        line1 = test_file.readline()
        if not line1:
            break  # EOF
        expected_result = test_file.readline()
        result = line1.split(' ')
        if result == 'Success' and expected_result == '400':
            print('400')
            return 1
        elif result == 'Failure' and expected_result == '200':
            print('400')
            return 1
        else:
            print('200')
            return 0


if __name__ == "__main__":
    main()