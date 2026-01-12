import time
import subprocess
import streamlit as st
from datetime import datetime
from pathlib import Path

def live_command_demo(cmd, log_name, mode="a"): # , live=True):
    placeholder = st.empty()
    start_time = datetime.now()
    # if mode == "new":
    #     edit_mode = "a"
    # elif mode == "write":
    #     edit_mode = "w"
    # elif mode == "new":
    log_file = Path(f"{log_name}.log")
    #     edit_mode = ""

    with open(log_file, mode, buffering=1) as log:
        # log.write("")
        log.write("\n" + "=" * 80 + "\n")
        log.write(f"[START] {start_time.isoformat()} | CMD: {' '.join(cmd)}\n")
        log.write("=" * 80 + "\n")
        log.flush()

        process = subprocess.Popen(
            cmd,
            stdout=log, 
            stderr=subprocess.STDOUT,
            text=True
            )

    # if live:
    while True:
#         for _ in range(60):  # Demo-Zeitfenster
        if log_file.exists():
            placeholder.code(log_file.read_text(), 
                            language="text")
        else:
            placeholder.info("Waiting for log output...")
        
        exit_code = process.poll()

        if exit_code is not None:
            with open(log_file, mode, buffering=1) as log:
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()

                # --- END MARKER ---
                log.write("-" * 80 + "\n")
                log.write(
                    f"[END] {end_time.isoformat()} | "
                    f"EXIT CODE: {exit_code} | "
                    f"DURATION: {duration:.1f}s\n"
                )
                log.write("-" * 80 + "\n")
                log.flush()

                placeholder.code(log_file.read_text(), 
                            language="text")
                            
            break

        time.sleep(1)


    # if error_mark:
    #     lines = log_file.read_text().splitlines()
    #     errors = [l for l in lines if "ERROR" in l or "FAILED" in l]
    #     if errors:
    #         st.code("\n".join(errors), language="text")

    return exit_code



def clear_others(active_key):
    for key in ["presentation", "demo", "extra"]:
        if key != active_key and key in st.session_state:
            st.session_state[key] = None

