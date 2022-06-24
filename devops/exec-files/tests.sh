
TEST_1="curl localhost:8081"
TEST_2="curl localhost:8081"
TEST_3="curl localhost:8081"

my_arr=("$TEST_1","$TEST_3","$TEST_3")

echo ${"${my_arr}"} 
