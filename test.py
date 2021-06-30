import time
start = time.time()

j = 1
for i in range(100000):
    j += 1
done = time.time()
elapsed = done - start
print(elapsed)