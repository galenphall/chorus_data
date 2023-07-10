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

### Positions table
The `positions` table contains the policy positions of interest groups in each state. Each row represents a single position taken by an interest group in a single state. The `positions` table contains the following columns:


### Clients table
The `clients` table contains the interest groups in each state. Each row represents a single _recorded instance_ of an interest group. Interest groups appear under several different variants on their names within the CHORUS data; additionally, we attempted to link interest groups from our scraped data to entities registered in three other databases: Follow The Money, Open Secrets, and Google Knowledge Graph. Each of these variants is represented by a single row in the `clients` table. The `clients` table contains the following columns:


### Bills table
The `bills` table contains the bills in each state. Each row represents a single bill. Where possible, we merged data on the bills from LegiScan and NCSL. The `bills` table contains the following columns:


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





