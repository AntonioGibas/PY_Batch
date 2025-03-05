# Testiranje konverzije datotečnog encodinga.
import codecs

def convert_to_ebcdic(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='ascii') as f:
            content = f.read()
        
        ebcdic_content = content.encode('cp037')
        
        with open(output_file, 'wb') as f:
            f.write(ebcdic_content)
        
        print(f"Datoteka uspjesno pretvorena: {output_file}")
    
    except Exception as e:
        print(f"Greska prilikom konverzije: {e}")

convert_to_ebcdic('/z/z26069/obrada1.txt', '/z/z26069/obrada1_ebcdic.txt')