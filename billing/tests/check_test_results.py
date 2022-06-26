#------------- Compare output to expected output ----------
def main():
    test_file = open('test_results.txt')
    result = 'true'
    while True:
        line= test_file.readline()
        if not line:
            break  # EOF
        chunks = line.split(' ')
        if chunks[0] == 'RESULT:'and chunks[1] == 'Pass':
            continue
        else:
            result = 'false'

    print(result)
    test_file.close()
    test_file = open('test_results.txt')
    while True:
        test_name = ''
        test_result = ''
        line = test_file.readline()
        if not line:
            break  # EOF
        chunks = line.split(' ')
        if chunks[0] == 'TEST:':
            test_name = line
            continue
        if chunks[0] == 'RESULT:':
            test_result = line
            print(test_name + ' ' + test_result )

if __name__ == "__main__":
    main()