from zoautil_py import datasets
import subprocess
import time
import os

uss_file = "/z/z26069/obrada1.txt"
dataset = "Z26069.ZOAU.NEW1"

try:
    try:
        datasets.delete(f"{dataset}")
    except Exception as e:
        print(f"Greska pri brisanju membera: {e}")

    datasets.create(
        "Z26069.ZOAU.NEW1",
        dataset_type="SEQ", 
        primary_space='1KB', 
        block_size=0,
        record_format='FB',
        record_lenght=100 
    )

    prog1 = subprocess.run(["/z/z26069/code1.py"], capture_output=True, text=True)
    prog2 = subprocess.run(["/z/z26069/code2.py"], capture_output=True, text=True)

    current_date_time = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())

    output = prog1.stdout + "\n" + prog2.stdout + "\n" + current_date_time

    if prog1.returncode == 0 and prog2.returncode == 0:
        output += "\nSUCCESS"
    else:
        output += "\nFAILURE"

    datasets.write(f"{dataset}", content=output)
    print(current_date_time)

except Exception as e:
    print(f"Doslo je do greske: {e}")
    import traceback
    traceback.print_exc()