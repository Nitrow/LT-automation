from vacuClassModule import VacuClass


def main():


    picoCam = VacuClass()
    frame = picoCam.takeImage()

    picoCam.findCapColor(frame)


if __name__ == '__main__':
    main()

