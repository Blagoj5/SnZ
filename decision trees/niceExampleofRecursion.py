def test(a, count):
    count += 1
    if count == 3:
        print(a, count)
        return 1
    test(9, count)
    print(a, count)
    


if __name__ == "__main__":
    test(5, 0)