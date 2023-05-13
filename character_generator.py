from gen import optimizer as optimizer
import sane.constraints as sanitylib
from gen import charlang as charlib 
from gen import charinterp as charinterp
import src.loggen as loggen

from src.pdfgen import PDFGenerator
import argparse
import os 

def make_character(args):
    if not os.path.exists(args.output_dir):
        os.mkdir(args.output_dir)

    sane_constraints,user_constraints = [],[]
    if not args.disable_sane:
        sane_constraints = list(sanitylib.sane_character_constraints())

    if not args.chargen_guide is None:
        with open(args.chargen_guide, 'r') as fh:
            data = fh.read()
            user_constraints = list(charinterp.load(data))


    #constraints = list(charlib.random_character_constraints())
    for index,character in enumerate(optimizer.generate_character(count=args.count, novice=args.novice, \
                            experience=args.experience,constraints=(user_constraints+sane_constraints))):
        outfile_pdf = "%s%s-%d.pdf" % (args.output_dir, args.base_name, index)
        outfile_txt = "%s%s-%d.txt" % (args.output_dir, args.base_name, index)
        #optimizer.pretty_print_model(chgen,model)
        pdfgen = PDFGenerator()
        new_pdf = pdfgen.populate(args.template_pdf,character)
        pdfgen.flatten_pdf()
        pdfgen.save(outfile_pdf,new_pdf)
        print("---> writing %s" % outfile_pdf)
        loggen.write_character_log(outfile_txt,character)
        print("---> writing %s" % outfile_txt)

parser = argparse.ArgumentParser(
                    prog='secret project x character generator',
                    description='generate random characters')
parser.add_argument('-b','--base-name',help="base name of characters", type=str, default="char")
parser.add_argument('count',help="number of characters to randomly generate", type=int,default=1)
parser.add_argument('-n', '--novice',help="novice character, subject to session one constraints",
                    action='store_true')  
parser.add_argument('-x','--experience',help="amount of experience to start with [default=10]", type=int, default=10)
parser.add_argument('-t','--template-pdf',help="template PDF to populate.", default="pdfs/Character Sheet Vigilante - TEMPLATE.pdf")
parser.add_argument('-c','--chargen-guide',help="provide a file that guides character generation")
parser.add_argument('-s','--disable-sane', default=True, help="add constraints to ensure sane characters are generated")
parser.add_argument('-o','--output-dir', help="output directory", default="output/")

args = parser.parse_args()
make_character(args)