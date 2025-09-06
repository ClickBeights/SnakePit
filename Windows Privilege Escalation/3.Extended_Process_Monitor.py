import os
import sys
import win32api
import win32con
import win32security
import wmi

# The extended part is responsible for printing out interesting windows privileges of printed processes.
def get_process_privileges(pid):
    try:
        # Use process ID to obtain a handle on the target process
        hproc = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION, False, pid)
        # Open the process token.
        htok = win32security.OpenProcessToken(hproc, win32con.TOKEN_QUERY)
        # Request process information for that token.
        privs = win32security.GetTokenInformation(htok, win32security.TokenPrivileges)
        privileges = ''
        for priv_id, flags in privs:
            # Show only enabled privileges using the (win32security.TokenPrivileges) function.
            if flags == win32security.SE_PRIVILEGE_ENABLED | win32security.SE_PRIVILEGE_ENABLED_BY_DEFAULT:
                # Return the enabled privileges from the tuple returned by the previous function (Human Readable Name).
                privileges += f'{win32security.LookupPrivilegeName(None, priv_id)}|'
    except Exception:
        # Modified from 'N/A' to the following to get proper output and log this information.
        privileges = get_process_privileges(pid)

    return privileges

def log_to_file(message):
    with open('process_monitor_log.csv', 'a') as fd:
        fd.write(f'{message}\r\n')

def monitor():
    log_to_file('CommandLine, Time, Executable, Parent PID, PID, User, Privileges')
    c = wmi.WMI()
    process_watcher = c.Win32_Process.watch_for('creation')
    while True:
        try:
            new_process = process_watcher()
            cmdline = new_process.CommandLine
            create_date = new_process.CreationDate
            executable = new_process.ExecutablePath
            parent_pid = new_process.ParentProcessId
            pid = new_process.ProcessId
            proc_owner = new_process.GetOwner()

            privileges = get_process_privileges(pid)
            process_log_message = (
                f'{cmdline} , {create_date} , {executable},'
                f'{parent_pid} , {pid} , {proc_owner} , {privileges}'
            )
            print(process_log_message)
            print()
            log_to_file(process_log_message)
        except Exception:
            pass

if __name__ == '__main__':
    monitor()
