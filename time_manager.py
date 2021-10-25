# This program shows weekly time allocations of tasks
import time

def read_file(filename):
    with open(filename) as f:
        lines = f.readlines()

    return lines

def write_to_file(filename, hdr_line, task_num, duration, lines, len_titles):
    file_object = open(filename, 'w')
    L = [hdr_line]

    times = list(map(float, lines[1].split()))
    additions = [0] * len_titles
    additions[task_num] = duration / 60 # we mostly work in minutes   

    new_times = [x + y for x, y in zip(times, additions)]

    new_line = ''
    for i in new_times:
        new_line = new_line + str(i) + ' '
    L.append(new_line)
    
    file_object.writelines(L)
    file_object.close()

def reset_all_times(filename, hdr_line, lines):
    file_object = open(filename, 'w')
    L = [hdr_line]

    times = list(map(float, lines[1].split()))
    resetted_times = [x * 0 for x in times]

    new_line = ''
    for i in resetted_times:
        new_line = new_line + str(i) + ' '
    
    L.append(new_line)
    
    file_object.writelines(L)
    file_object.close()

def show_records(lines, titles):
    count = 0
    times = list(map(float, lines[1].split()))
    for i in range(len(titles)):
        print("%s\t: %5.2f hrs\t<->\t%7.2f min" % (titles[i], times[i]/60, times[i]))

def choose_task(titles):
    print("Choose a task:\n")
    for i in range(len(titles)):
        print(i, "-", titles[i])
    print(i + 1, "- Just show me the current records!")
    print(i + 2, "- Instead, add a duration manually!")
    print(i + 3, "- RESET\n")
    task_num = int(input("Enter task number: "))

    return task_num

def show_updated_records(filename, lines):
    print()
    lines = read_file(filename)
    hdr_line = lines[0]
    titles = hdr_line.split()
    titles[-1] = (titles[-1].split())[0]
    show_records(lines, titles)

if __name__ == "__main__":
    # This is the file where task names and time data is stored.
    filename = 'time_data.txt'
    lines = read_file(filename)
    # get first (title) line
    hdr_line = lines[0]
    
    titles = hdr_line.split()
    # remove \n
    titles[-1] = (titles[-1].split())[0]

    # Choosing task
    task_num = choose_task(titles)

    repeat = True
    while repeat:
        if task_num == len(titles):
            show_records(lines, titles)
            
        elif task_num == len(titles) + 1:
            task_num    = int(input("Which task? (number): "))
            time_lapsed = float(input("Enter duration in minutes: "))
            # convert minute to seconds
            time_lapsed *= 60 
            write_to_file(filename, hdr_line, task_num, time_lapsed, lines, len(titles))

            show_updated_records(filename, lines)

        elif task_num == len(titles) + 2:
            reset_all_times(filename, hdr_line, lines)
            print("Resetting completed, have a nice week!")
            
        else:
            # Start recording (STOPWATCH)
            # Stopwatch
            start_time = time.time()
            input("Press Enter to stop stopwatch")
            end_time = time.time()

            time_lapsed = end_time - start_time

            print(time_lapsed, "in seconds")
            print(time_lapsed/60, "in minutes")

            write_to_file(filename, hdr_line, task_num, time_lapsed, lines, len(titles))

            show_updated_records(filename, lines)

        check = input("\nDo you want to do another task? (type y for yes): ")
        if check == 'y':
            task_num = choose_task(titles)
        else:
            repeat = False  

