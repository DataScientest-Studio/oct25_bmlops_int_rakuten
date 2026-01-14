import time
import subprocess
import streamlit as st
from datetime import datetime
from pathlib import Path

def live_command_demo(cmd, log_name, mode="a"):
    placeholder = st.empty()
    start_time = datetime.now()
    
    log_file = Path(f"{log_name}.log")
   

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

    while True:
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

    return exit_code


def clear_others(active_key):
    for key in ["presentation", "demo", "extra"]:
        if key != active_key and key in st.session_state:
            st.session_state[key] = None

