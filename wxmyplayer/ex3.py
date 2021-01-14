import keyboard
def main():
    b1 = True
    while b1:
        print("A")
    if keyboard.is_pressed("q"):
        b1 =False
        print("gone")

if __name__ == "__main__":
    main()