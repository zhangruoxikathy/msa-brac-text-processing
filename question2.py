# PPHA 30538 Python2
# Fall 2023
# Homework 2

# Kathy Zhang
# zhangruoxikathy

# import packages
import re
import os
from pypdf import PdfReader

# %% Section 1 Functions defined

# %%% Sub-Section 1 Read pdf and perform cleaning

PATH = r'C:\\Users\\zhang\\OneDrive\\Documents\\GitHub'\
    r'\\homework-2-zhangruoxikathy-1'
os.chdir(PATH)
fname = '2005proposal.pdf'


def pdf_to_text(fname):
    """Load and parse the PDF document, also conduct a simple cleaning."""
    pdf = PdfReader(os.path.join(PATH, fname))
    text = []
    for page in pdf.pages[2:48]:
        page_text = page.extract_text()
        # remove footer and page number
        page_text = page_text.replace("This list does not include locations " +
                                      "where no changes in military or " +
                                      "civilian jobs are affected.", "")
        page_text = page_text.replace("Military figures include " +
                                      "student load changes.", "")
        page_text = page_text.replace("*Does not include the reduction of "
                                      "14,172 military positions a nd "
                                      "increase of 667 civilian positions "
                                      "from Germany, Korea, and Un "
                                      "distributed Actions.", "")
        page_text = re.sub(r'B-\d+', '', page_text)

        text.append(page_text)

    return '\n'.join(text)


def replace_patterns(new_text):
    """Substitute selected patterns for grouping."""

    def apply_re_subs(new_text, substitutions):
        """Replace incorrect patterns in a text with correct substitution."""
        for pattern, replacement in substitutions.items():
            new_text = re.sub(pattern, replacement, new_text)
        return new_text

    # create a dictionary with unwanted patterns and intended edited patterns
    subs = {
            r'0\(': r'0 (',
            r'\( (\d+) (\d+) \)': r'(\1\2)',
            r'\( (\d+) \)': r'(\1)',
            r' 0(\d) ': r' 0 \1 ',
            r'([\d,])\((\d) (\d+)\)([\dA-Z-])': r'\1\2\3 \4',
            r'\((0) (\d)\)': r'\1 \2 ',
            r'([A-Za-z]+)(\d)': r'\1 \2',
            r'(\d),(\d)': r'\1\2',
            r'\(([\d]+)\)': r'-\1'
            }

    new_text = apply_re_subs(new_text, subs)
    # remove extra spaces for easier grouping
    new_text = re.sub(' +', ' ', new_text)
    return new_text


def clean_text(lines):
    """Remove repetitive column names, header, replace incorrect patterns."""
    strings_remove = ["BRAC 2005 Closure and Realignment Impacts by Economic" +
                      " Area", "Economic Area ", "ActionInstallation Mil Civ" +
                      " Mil Civ Mil CivOut In Net Gain/(Loss) Net Mission ",
                      "ContractorTotal ", "DirectIndirect ", "ChangesTotal ",
                      "Job ", "ChangesEconomic ", "Area ", "Economic Area",
                      "Area Changes ", "EmploymentChanges as ", "Percent of ",
                      "Employment ", "Employment", ""]

    lines = [string for string in lines if string not in strings_remove]
    new_text = " ".join(lines)
    # remove extra spaces for easier grouping and cleaning
    new_text = re.sub(' +', ' ', new_text)
    new_text = replace_patterns(new_text)
    return new_text


# %%% Sub-Section 2 Perform matching and grouping

def form_matches_per_msa(new_text, lines):
    """Form a list of strings that each includes a msa's data."""
    pattern = (
        r'(([A-Za-z -]+, [A-Z-]+) (Metropolitan Statistical Area|'
        r'Micropolitan Statistical Area|Metropolitan Division|)[\s\S]+?)'
        r'(?=(?:[A-Za-z -]+, [A-Z]{2}))|$')
    matches = re.findall(pattern, new_text)
    matches = [tup[0].strip() for tup in matches if tup[0].strip() != ""]
    # matches = [x for x in matches if x != ""]
    # add back the last msa sicne it was not matched
    matches.append(" ".join(lines[-4:]))
    # clean up certain lines in the list
    matches[128] = matches[128] + ' ' + matches[129]
    del matches[129]
    matches[243] = replace_patterns(matches[243])
    matches[90] = replace_patterns(matches[90])
    return matches


def get_bases(matches):
    """Get each base of each msa with relavant data."""
    # get a list of msas and a list without msas to split bases
    pattern_msa = (r'([A-Za-z -]+, [A-Z-]+) (Metropolitan Statistical Area|' +
                   'Micropolitan Statistical Area|Metropolitan Division|)')
    re_results_msa = [re.search(pattern_msa, t) for t in matches]
    msa = [res.group(1)+' '+res.group(2) for res in re_results_msa if res]
    list_wo_msa = [str2.replace(str1, '', 1) for str1, str2 in
                   zip(msa, matches)]

    # create a list of lists for each msa, with each list contains lists for
    # each base in this msa and each base's data
    list_msa_base_data = []  # lists of lists of bases and data within each msa

    # Group bases and their data under each msa
    for list_ in list_wo_msa:
        pattern_base = (r'(\s+|)((([A-Za-z-/.,\s]+(126|))|I-270|)(# 2|)'
                        r'([A-Za-z-/.,\s]+|))\s([-\d,()]+) ([-\d,()]+) '
                        r'([-\d,()]+) ([-\d,()]+) ([-\d,()]+) ([-\d,()]+) '
                        r'(Realign|Gain|Close|Close/Realign) ([-\d,()]+) '
                        r'([-\d,()]+) ([-\d,()]+) ([-\d,()]+) ([-\d,()]+) '
                        r'([-\d,.-]+%)')

        # find all base and its data
        bases = re.findall(pattern_base, list_)
        bases = [list(tup) for tup in bases]
        list_msa_base_data.append(bases)

    # reformat to get the final list for each base wuth its msa and data
    final_list = []
    for msa_ in range(len(list_msa_base_data)):
        for base_ in list_msa_base_data[msa_]:
            # add quotes for each msa and base so that when converting them to
            # csv, comma within msa and base will not be used as seperators
            msa_edited = f'"{msa[msa_]}"'
            base_edited = f'"{base_[1]}"'
            # organize base data based on columns for each base
            msa_base = [msa_edited, base_edited, base_[-7], base_[-12],
                        base_[-10], base_[-13], base_[-11], base_[-9],
                        base_[-8], base_[-6], base_[-5], base_[-4], base_[-3],
                        base_[-2], base_[-1]]
            final_list.append(msa_base)

    return final_list


# %%% Sub-Section 3 Export to csv

def export_to_csv(final_list):
    """Convert the final list of bases to csv readable text."""
    final_text = [','.join(line) for line in final_list]
    # add header to the text as column names
    col_names = ('msa,base,action,mil_out,civ_out,mil_in,civ_in,mil_net,'
                 'civ_net,net_contractor,direct,indirect,'
                 'total_job_changes,ea_employment,'
                 'changes_as_percent_of_employment')
    final_text.insert(0, col_names)
    # now, each cell is seperated by comma and each row by \n
    doc = '\n'.join(final_text)
    with open('question2.csv', 'w') as ofile:
        ofile.write(doc)
    return doc


# %% Section 2 Use functions to generate output

# read the file and split it by line to a list to see if cleaning is needed
text = pdf_to_text(fname)
list_of_lines = text.strip().split(sep='\n')
# clean texts with deletion and regular expression
cleaned_text = clean_text(list_of_lines)
# find matches of each msa, remove msa from list, and then group bases under
# each msa, finally group together all the data in order for each base
matches_per_msa = form_matches_per_msa(cleaned_text, list_of_lines)
final_list_msa_base_data = get_bases(matches_per_msa)
# convert to csv by forming a csv readable string
final_doc_msa_base_data = export_to_csv(final_list_msa_base_data)
