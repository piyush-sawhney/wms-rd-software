from rd_app.rd_master import process_rd_master
if __name__ == '__main__':
    option = input("Select an option.\n1. Run Master\n2. Re-Run Master\n3. Create Download and Upload schedules\n")
    if int(option) == 1:
        process_rd_master()
    elif int(option) == 2:
        process_rd_master(is_rerun=True)
