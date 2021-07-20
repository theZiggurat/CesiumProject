HEIGHTMAP_WIDTH = 512

def main():

    print("Reading data files...")
    pre = open("assets/pre.data", "rb").read()
    post = open("assets/post.data", "rb").read()

    while True:

        args = [x.strip() for x in input('Enter pixel coordinates: ').split(',')]

        if len(args) != 2:
            print("Please enter two numbers seperated by comma")
            continue

        x = int(args[0])
        y = int(args[1])

        if x > HEIGHTMAP_WIDTH or y > HEIGHTMAP_WIDTH:
            print("X and Y values must be below {}".format(HEIGHTMAP_WIDTH))
            continue

        quit = input("Quit? (y, n): ").strip().lower()
        if quit == 'y':
            break



if __name__ == "__main__":
    main()