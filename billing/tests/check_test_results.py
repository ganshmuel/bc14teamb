#!/usr/bin/env python3



def main():
    test_file = open('test_results.txt')
    result = 'true'
    while True:
        line= test_file.readline()
        if not line:
            break  # EOF
        chunks = line.split(' ')
        if chunks[0] == 'RESULT:' and chunks[1] == 'Pass\n':
            continue
        elif chunks[0] == 'RESULT:' and chunks[1] != 'Pass\n':
            result = 'false'
        else:
            continue

    print(result)
    test_file.close()
    test_file = open('test_results.txt')
    test_name = ''
    test_result = ''
    while True:

        line = test_file.readline()
        if not line:
            break  # EOF
        spited_line = line
        chunks = spited_line.split(' ')
        if chunks[0] == 'TEST:':
            test_name = line
            continue
        if chunks[0] == 'RESULT:':
            test_result = line
            print(test_name + ' ' + test_result )
    test_file.close()
if __name__ == "__main__":
    main()