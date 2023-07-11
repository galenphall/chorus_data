import pandas as pd

files = [
    'codebook/bills_codebook.xlsx',
    'codebook/clients_codebook.xlsx',
    'codebook/positions_codebook.xlsx',
    'codebook/block_assignments_codebook.xlsx',
]

markdown_str = """
<div style="text-align: center;">
<p>CHORUS: A new dataset of state interest group policy positions in the United States</p>


Galen Hall <br> 
University of Michigan <br>
galenh@umich.edu <br>
Corresponding author

Joshua Basseches <br>
Tulane University <br>
jbasseches@tulane.edu

Rebecca Bromley-Trujillo <br>
Christopher Newport University <br>
rebecca.bromleytrujillo@cnu.edu; 

Trevor Culhane <br> 
Brown University <br>
trevor_culhane@brown.edu <br>
</div>

# Codebook

## Data
The data used in this project is available online in the SPPQ Dataverse: https://dataverse.unc.edu/dataverse/sppq. To download it locally, run the `code/download.py` file.


"""

# Generate a markdown table for each file
for file in files:
    name = ' '.join(file.split('_')[:-1]).split('/')[-1].title()
    markdown_str += f"## {name}\n\n"

    df = pd.read_excel(file)
    df = df.drop(columns=['Unnamed: 0'])
    df = df.fillna('')

    description_col = next(c for c in df.columns if "Description" in c)
    df = df.rename(columns={description_col: 'Description'})

    # link to the corresponding section below for each variable
    varlinks = [f"[`{variable}`](#{name}{variable})" for variable in df.Variable.values]

    markdown_str += f"Columns: {', '.join(varlinks)}\n\n"

    for idx, row in df.iterrows():
        ## add a header for the variable, and make it an anchor
        markdown_str += f'### <a name="{name}{row.Variable}" id="{row.Variable}"></a>`{row.Variable}`\n\n'

        addl = next(c for c in row.index if "Additional" in c)

        # add a one-column table for the remainder of the row
        table = row.drop(["Variable", addl]).copy()
        table = table[table != '']
        table.index = [f"**{i}**" for i in table.index]
        table.name = ''
        table = table.to_frame().T
        markdown_str += table.to_markdown(index = False) + "\n\n"

        if row[addl] != '':
            markdown_str += f"**Additional information:** {row[addl]}\n\n"

    markdown_str += "\n\n"


markdown_str += """
## References

<p style="padding-left: 2em; text-indent: -2em;">
FollowTheMoney. “Home - FollowTheMoney.Org.” (https://www.followthemoney.org/). Data from FollowTheMoney is licensed under CC BY 4.0
</p>

<p style="padding-left: 2em; text-indent: -2em;">
Google Cloud. “Google Knowledge Graph Search API | Enterprise Knowledge Graph.” (https://cloud.google.com/enterprise-knowledge-graph/docs/search-api).
</p>

<p style="padding-left: 2em; text-indent: -2em;">
  LegiScan. “LegiScan | National Session Data Archives.” LegiScan. (https://legiscan.
com/datasets). Data from Legiscan (Legislative Datasets) by LegiScan LLC is licensed under CC BY 4.0
</p>

<p style="padding-left: 2em; text-indent: -2em;">
  National Conference of State Legislatures. “NCSL 50-State Searchable Bill Tracking Databases.” (https://www.ncsl.org/technology-and-communication/ncsl-50-state-searchable-bill-tracking-databases).
</p>

<p style="padding-left: 2em; text-indent: -2em;">
OpenSecrets. “OpenSecrets.” (https://www.opensecrets.org/). Data from OpenSecrets is licensed under CC BY 4.0
</p>
"""

with open('codebook/codebook_output.md', 'w') as f:
    f.write(markdown_str)