import subprocess
import sys
import codecs

uss_file = "/z/z26069/obrada1.txt"
ebcdic_file = "/z/z26069/obrada1_ebcdic_temp.txt"
dataset = "Z26069.USSPY.OUTPUT"

try:
    # Brisanje postojeceg dataseta
    delete_cmd = f"DELETE '{dataset}' PURGE"
    subprocess.run(["tso", delete_cmd], check=False)

    # Alokacija novog dataseta
    allocate_cmd = f"ALLOCATE DA('{dataset}') NEW SPACE(1,1) TRACKS LRECL(80) RECFM(F B) DSORG(PS)"
    subprocess.run(["tso", allocate_cmd], check=True)

    # Pokretanje prvog i drugog programa
    prog1 = subprocess.run(["/z/z26069/code1.py"], capture_output=True, text=True)
    prog2 = subprocess.run(["/z/z26069/code2.py"], capture_output=True, text=True)

    output = prog1.stdout + "\n" + prog2.stdout

    if prog1.returncode == 0 and prog2.returncode == 0:
        output += "\nSUCCESS\n"
    else:
        output += "\nFAILURE\n"

    # Pisanje outputa u ASCII datoteku
    with open(uss_file, "w") as f:
        f.write(output)
    
    # Rucna konverzija u EBCDIC (IBM-037)
    with open(uss_file, 'r', encoding='ascii') as input_file:
        content = input_file.read()
    
    # Kodiranje u EBCDIC
    ebcdic_content = content.encode('cp037')
    
    # Cuvanje EBCDIC verzije
    with open(ebcdic_file, 'wb') as output_file:
        output_file.write(ebcdic_content)

    # Prijenos EBCDIC datoteke u dataset
    oget_cmd = f"OGET '{ebcdic_file}' 'Z26069.USSPY.OUTPUT'"
    subprocess.run(["tso", oget_cmd], check=True)

except Exception as e:
    print(f"Doslo je do greske: {e}")
    print(f"Tip greske: {type(e)}")
    import traceback
    traceback.print_exc()