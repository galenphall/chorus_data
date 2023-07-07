# Codebook

## Data
The data used in this project is available online in the SPPQ Dataverse: https://dataverse.unc.edu/dataverse/sppq. To download it locally, run the `code/download.py` file.

### Positions table
The `positions` table contains the policy positions of interest groups in each state. Each row represents a single position taken by an interest group in a single state. The columns are as follows:

positions
- **bill_number**: The bill number of the bill on which the interest group took a position.
- **bill_chamber**: The chamber in which the bill was introduced.
- **bill_version**: The version of the bill on which the interest group took a position, if applicable.
- **client_name**: The name of the interest group.
- **lobbyist_rep_name**: The name of the lobbyist who represented the interest group.
- **lobbyist_firm_name**: The name of the firm that employed the lobbyist.
- **position**: The string representation of the position taken by the interest group, which is recorded differently in each state.
- **start_date**: The date on which the interest group took the position.
- **end_date**: The date on which the interest group ended the position, if applicable.
- **client_parent_name**: The name of the parent organization of the interest group, if applicable.
- **year**: The year in which the position was taken.
- **record_type**: The type of record in which the position was recorded. This is used to distinguish between positions recorded in `lobbying` versus `testimony`.
- **session**: The session in which the position was taken.
- **description**: The description of the position, if applicable.
- **committee**: The committee to which the bill was referred, if applicable.
- **doclink**: The link to the original document in which the position was recorded.
- **state**: The state in which the position was taken.
- **unified_session**: The unified session in which the position was taken, used for merging across datasets.
- **unified_prefix**: The unified prefix of the bill on which the position was taken, used for merging across datasets.
- **position_numeric**: The numeric representation of the position taken by the interest group: 1 for support, -1 for oppose, and 0 for neutral.
- **docket_number**: The docket number of the bill on which the position was taken, if applicable.
- **docket_prefix**: The docket prefix of the bill on which the position was taken, if applicable.
- **unified_docket**: The unified docket of the bill on which the position was taken, if applicable.
- **legiscan_bill_id**: The Legiscan id of the bill on which the position was taken, if applicable.
- **client_uuid**: The unique identifier of the interest group, used for merging across datasets.
- **unified_bill_number**: The unified bill number of the bill on which the position was taken, used for merging across datasets.
- **bill_id**: The original id given to bill on which the position was taken.
- **unified_bill_id**: The unified bill id of the bill on which the position was taken, used for merging across datasets.
- **state_unified_bill_id**: The unified bill id of the bill on which the position was taken, used for merging across datasets. This combines the state and unified bill id.
- **state_client_uuid**: The unique identifier of the interest group, used for merging across datasets. This combines the state and client uuid.
- **ncsl_metatopics**: The metatopics of the bill on which the position was taken, according to NCSL, if applicable.
- **ncsl_topics**: The topics of the bill on which the position was taken, according to NCSL, if applicable.
- **ftm_final**: The final industry of the interest group according to FollowTheMoney, using Naive Bayes if necessary.
- **ftm_confirmed**: The final industry of the interest group according to FollowTheMoney, confirmed by a human coder, if applicable.

### Clients table
- **client_name**: The name of the interest group.
- **state**: The state in which the interest group is registered.
- **client_index**: The index of the interest group (not used)
- **source**: The source of the interest group (indicates whether it comes from external sources such as FTM or from the state's lobbying database)
- **source_eid**: the id in the source database
- **client_uuid**: a unique identifier for the interest group, which may link registrations from different sources and states
- **ftm_industry**: the industry of the interest group according to FollowTheMoney
- **ftm_industry_merged**: the industry of the interest group according to FollowTheMoney, merged across uuids
- **ftm_best_guess**: the best guess for the industry of the interest group according to FollowTheMoney, using Naive Bayes
- **ftm_final**: the final industry of the interest group according to FollowTheMoney, using Naive Bayes if necessary
- **state_client_uuid**: the unique identifier for the interest group appended to the state, to distinguish between interest groups with the same uuid in different states



### Bills table
legiscan_bill_id:
legiscan_bill: 
change_hash: 
legiscan_url: 
status_date: 
status: 
last_action_date: 
last_action: 
title: 
description: 
session_id: 
state_id: 
year_start: 
year_end: 
prefile: 
sine_die: 
prior: 
special: 
session_tag: 
session_title: 
session_name: 
state: 
bill_chamber: 
bill_number: 
bill_suffix: 
unified_session: 
state_chamber: 
unified_prefix: 
first_legiscan_progress_date: 
last_legiscan_progress_date: 
first_legiscan_history_date: 
last_legiscan_history_date: 
sponsor_list: 
description_ncsl: 
ncsl_summary: 
history: 
ncsl_link: 
date_overlap_jaccard: 
title_overlap_jaccard: 
ncsl_topics: 
ncsl_databases: 
ncsl_metatopics: 
unified_bill_number: 
unified_bill_id: 
bill_id: 
state_unified_bill_id: 