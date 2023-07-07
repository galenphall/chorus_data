# Codebook

## Data
The data used in this project is available online in the SPPQ Dataverse: https://dataverse.unc.edu/dataverse/sppq. To download it locally, run the `code/download.py` file.

### Positions table
The `positions` table contains the policy positions of interest groups in each state. Each row represents a single position taken by an interest group in a single state. The columns are as follows:

- `state`: The state in which the position was taken.
- `year`: The year in which the position was taken.
- `state_client_uuid`: A unique identifier for the interest group that took the position.
- `client_name`: The name of the interest group that took the position.
- `lobbyist_rep_name`: The name of the lobbyist who represented the interest group.
- `lobbyist_firm_name`: The name of the firm that employed the lobbyist.
- `state_unified_bill_id`: A unique identifier for the bill on which the position was taken.
- `bill_number`: The number of the bill on which the position was taken.
- `bill_chamber`: The chamber in which the bill was introduced.
- `bill_title`: The title of the bill on which the position was taken.