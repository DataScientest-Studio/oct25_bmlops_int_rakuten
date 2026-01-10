import time
import subprocess

def live_command_demo(cmd, log_file): # , live=True):
    placeholder = st.empty()
    
    with open(log_file, "w") as log:
        
        process = subprocess.Popen(
            cmd,
            # ["make", "api_docker"],
            stdout=log, # open("build_apis.log", "w"),
            stderr=subprocess.STDOUT,
            text=True
    )

    # if live:
    while True:
#         for _ in range(60):  # Demo-Zeitfenster
        if log_file.exists():
            placeholder.code(log_file.read_text(), language="text")
        else:
            placeholder.info("Waiting for log output...")
        exit_code = process.poll()

        if exit_code is not None:
            break

        time.sleep(1)

    # if error_mark:
    #     lines = log_file.read_text().splitlines()
    #     errors = [l for l in lines if "ERROR" in l or "FAILED" in l]
    #     if errors:
    #         st.code("\n".join(errors), language="text")

    return exit_code