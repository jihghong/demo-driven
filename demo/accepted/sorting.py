def bubble_sort(arr):
    arr = arr.copy()
    for i in range(len(arr)):
        for j in range(len(arr) - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def run_tests():
    print("Test 1: simple integers")
    print("Result:", bubble_sort([5, 2, 3]))

    print("Test 2: already sorted")
    print("Result:", bubble_sort([1, 2, 3]))

    print("Test 3: with duplicates")
    print("Result:", bubble_sort([2, 2, 1, 3]))

    print("Test 4: empty list")
    print("Result:", bubble_sort([]))


if __name__ == "__main__":
    run_tests()