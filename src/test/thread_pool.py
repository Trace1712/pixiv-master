import time
import threading
import random
def test(value1, value2=None):
    print("%s threading is printed %s, %s"%(threading.current_thread().name, value1, value2))
    time.sleep(random.randint(5,10))
    return 'finished'

def test_result(future):
    print(future.result())

if __name__ == "__main__":
    from concurrent.futures import ThreadPoolExecutor
    threadPool = ThreadPoolExecutor(max_workers=4, thread_name_prefix="test")
    for i in range(0,10):
        future = threadPool.submit(test, i,i+1)
#         future.add_done_callback(test_result)
#         print(future.result())

    # threadPool.shutdown(wait=True)
    print('main finished')