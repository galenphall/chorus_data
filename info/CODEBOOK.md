
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


## Bills

Columns: [`legiscan_bill_id`](#Billslegiscan_bill_id), [`legiscan_bill`](#Billslegiscan_bill), [`legiscan_url`](#Billslegiscan_url), [`status_date`](#Billsstatus_date), [`status`](#Billsstatus), [`last_action_date`](#Billslast_action_date), [`last_action`](#Billslast_action), [`title`](#Billstitle), [`description`](#Billsdescription), [`year_start`](#Billsyear_start), [`year_end`](#Billsyear_end), [`prefile`](#Billsprefile), [`sine_die`](#Billssine_die), [`prior`](#Billsprior), [`session_title`](#Billssession_title), [`state`](#Billsstate), [`bill_chamber`](#Billsbill_chamber), [`bill_number`](#Billsbill_number), [`bill_suffix`](#Billsbill_suffix), [`sponsor_list`](#Billssponsor_list), [`description_ncsl`](#Billsdescription_ncsl), [`ncsl_summary`](#Billsncsl_summary), [`date_overlap_jaccard`](#Billsdate_overlap_jaccard), [`title_overlap_jaccard`](#Billstitle_overlap_jaccard), [`ncsl_topics`](#Billsncsl_topics), [`ncsl_databases`](#Billsncsl_databases), [`ncsl_metatopics`](#Billsncsl_metatopics), [`state_unified_bill_id`](#Billsstate_unified_bill_id)

### <a name="Billslegiscan_bill_id" id="legiscan_bill_id"></a>`legiscan_bill_id`

|   **Example** | **Description**          | **Type**   | **Source**   |
|--------------:|:-------------------------|:-----------|:-------------|
|        225543 | LegiScan bill identifier | integer    | LegiScan     |

### <a name="Billslegiscan_bill" id="legiscan_bill"></a>`legiscan_bill`

| **Example**   | **Description**                       | **Type**   | **Source**   |
|:--------------|:--------------------------------------|:-----------|:-------------|
| LR19CA        | Bill chamber and number from LegiScan | string     | LegiScan     |

### <a name="Billslegiscan_url" id="legiscan_url"></a>`legiscan_url`

| **Example**                              | **Description**                     | **Type**   | **Source**   |
|:-----------------------------------------|:------------------------------------|:-----------|:-------------|
| https://legiscan.com/NE/bill/LR19CA/2011 | The URL of the bill's LegiScan page | string     | LegiScan     |

### <a name="Billsstatus_date" id="status_date"></a>`status_date`

| **Example**   | **Description**      | **Type**   | **Source**   |
|:--------------|:---------------------|:-----------|:-------------|
| 2012-02-08    | Status date for bill | datetime   | LegiScan     |

### <a name="Billsstatus" id="status"></a>`status`

|   **Example** | **Description**       | **Type**   | **Source**   |
|--------------:|:----------------------|:-----------|:-------------|
|             3 | Status value for bill | integer    | LegiScan     |

### <a name="Billslast_action_date" id="last_action_date"></a>`last_action_date`

| **Example**   | **Description**     | **Type**   | **Source**   |
|:--------------|:--------------------|:-----------|:-------------|
| 2012-04-18    | Date of last action | datetime   | LegiScan     |

### <a name="Billslast_action" id="last_action"></a>`last_action`

| **Example**            | **Description**            | **Type**   | **Source**   |
|:-----------------------|:---------------------------|:-----------|:-------------|
| Indefinitely postponed | Description of last action | string     | LegiScan     |

### <a name="Billstitle" id="title"></a>`title`

| **Example**                                                                                                             | **Description**     | **Type**   | **Source**   |
|:------------------------------------------------------------------------------------------------------------------------|:--------------------|:-----------|:-------------|
| Constitutional amendment to provide that a civil officer is liable to impeachment for misdemeanors in pursuit of office | Short title of bill | string     | LegiScan     |

### <a name="Billsdescription" id="description"></a>`description`

| **Example**                                                                                                             | **Description**    | **Type**   | **Source**   |
|:------------------------------------------------------------------------------------------------------------------------|:-------------------|:-----------|:-------------|
| Constitutional amendment to provide that a civil officer is liable to impeachment for misdemeanors in pursuit of office | Long title of bill | string     | LegiScan     |

### <a name="Billsyear_start" id="year_start"></a>`year_start`

|   **Example** | **Description**                            | **Type**   | **Source**   |
|--------------:|:-------------------------------------------|:-----------|:-------------|
|          2011 | Starting year of the session from LegiScan | integer    | LegiScan     |

### <a name="Billsyear_end" id="year_end"></a>`year_end`

|   **Example** | **Description**                          | **Type**   | **Source**   |
|--------------:|:-----------------------------------------|:-----------|:-------------|
|          2012 | Ending year of the session from LegiScan | integer    | LegiScan     |

### <a name="Billsprefile" id="prefile"></a>`prefile`

|   **Example** | **Description**                                        | **Type**   | **Source**   |
|--------------:|:-------------------------------------------------------|:-----------|:-------------|
|             0 | Flag for session being in prefile (0, 1) from LegiScan | integer    | LegiScan     |

### <a name="Billssine_die" id="sine_die"></a>`sine_die`

|   **Example** | **Description**                                                | **Type**   | **Source**   |
|--------------:|:---------------------------------------------------------------|:-----------|:-------------|
|             1 | Flag for session being adjourned sine die (0, 1) from LegiScan | integer    | LegiScan     |

### <a name="Billsprior" id="prior"></a>`prior`

|   **Example** | **Description**                                                                | **Type**   | **Source**   |
|--------------:|:-------------------------------------------------------------------------------|:-----------|:-------------|
|             1 | Flag for session being archived out of production updates (0, 1) from LegiScan | integer    | LegiScan     |

### <a name="Billssession_title" id="session_title"></a>`session_title`

| **Example**               | **Description**                                                                 | **Type**   | **Source**   |
|:--------------------------|:--------------------------------------------------------------------------------|:-----------|:-------------|
| 2011-2012 Regular Session | Normalized session title with year(s) and Regular/Special Session from LegiScan | string     | LegiScan     |

### <a name="Billsstate" id="state"></a>`state`

| **Example**   | **Description**   | **Type**   | **Source**   |
|:--------------|:------------------|:-----------|:-------------|
| NE            | State acronym     | string     | CHORUS       |

### <a name="Billsbill_chamber" id="bill_chamber"></a>`bill_chamber`

| **Example**   | **Description**                | **Type**   | **Source**   |
|:--------------|:-------------------------------|:-----------|:-------------|
| LR            | The chamber/prefix of the bill | string     | CHORUS       |

### <a name="Billsbill_number" id="bill_number"></a>`bill_number`

|   **Example** | **Description**        | **Type**   | **Source**   |
|--------------:|:-----------------------|:-----------|:-------------|
|            19 | The number of the bill | integer    | CHORUS       |

### <a name="Billsbill_suffix" id="bill_suffix"></a>`bill_suffix`

| **Example**   | **Description**        | **Type**   | **Source**   |
|:--------------|:-----------------------|:-----------|:-------------|
| CA            | The suffix of the bill | string     | CHORUS       |

### <a name="Billssponsor_list" id="sponsor_list"></a>`sponsor_list`

| **Example**    | **Description**       | **Type**   | **Source**   |
|:---------------|:----------------------|:-----------|:-------------|
| ['Bill Avery'] | List of bill sponsors | string     | LegiScan     |

### <a name="Billsdescription_ncsl" id="description_ncsl"></a>`description_ncsl`

| **Example**                     | **Description**      | **Type**   | **Source**    |
|:--------------------------------|:---------------------|:-----------|:--------------|
| Election to Office Misdemeanors | Bill title from NCSL | string     | Statenet/NCSL |

### <a name="Billsncsl_summary" id="ncsl_summary"></a>`ncsl_summary`

| **Example**                                                                                                                                   | **Description**           | **Type**   | **Source**    |
|:----------------------------------------------------------------------------------------------------------------------------------------------|:--------------------------|:-----------|:--------------|
| Proposes a constitutional amendment to provide that misdemeanors related to election to office are grounds for impeachment of civil officers. | Summary of bill from NCSL | string     | Statenet/NCSL |

### <a name="Billsdate_overlap_jaccard" id="date_overlap_jaccard"></a>`date_overlap_jaccard`

|   **Example** | **Description**                                                                                           | **Type**   | **Source**   |
|--------------:|:----------------------------------------------------------------------------------------------------------|:-----------|:-------------|
|      0.896774 | A measure of how well the date range for this bill in LegiScan overlapped with the date range in StateNet | float64    | CHORUS       |

**Additional information:** These fields can be used to assess the likelihood that a given bill was incorrectly aligned between LegiScan and Statenet.

### <a name="Billstitle_overlap_jaccard" id="title_overlap_jaccard"></a>`title_overlap_jaccard`

|   **Example** | **Description**                                                                                 | **Type**   | **Source**   |
|--------------:|:------------------------------------------------------------------------------------------------|:-----------|:-------------|
|      0.521739 | A measure of how well the title for this bill in LegiScan overlapped with the title in StateNet | float64    | CHORUS       |

**Additional information:** These fields can be used to assess the likelihood that a given bill was incorrectly aligned between LegiScan and Statenet.

### <a name="Billsncsl_topics" id="ncsl_topics"></a>`ncsl_topics`

| **Example**                                                                                                                                                                             | **Description**                                                        | **Type**   | **Source**    |
|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------|:-----------|:--------------|
| ncsl_database__state_elections_legislation_database__ncsl_topic__candidates_qualifications_for_office; ncsl_database__state_elections_legislation_database__ncsl_topic__election_crimes | Topics that the bill addresses, based on matches with NCSL's databases | string     | Statenet/NCSL |

### <a name="Billsncsl_databases" id="ncsl_databases"></a>`ncsl_databases`

| **Example**                                         | **Description**                      | **Type**   | **Source**    |
|:----------------------------------------------------|:-------------------------------------|:-----------|:--------------|
| ncsl_database__state_elections_legislation_database | NCSL databases that include the bill | string     | Statenet/NCSL |

### <a name="Billsncsl_metatopics" id="ncsl_metatopics"></a>`ncsl_metatopics`

| **Example**                             | **Description**                        | **Type**   | **Source**    |
|:----------------------------------------|:---------------------------------------|:-----------|:--------------|
| ncsl_metatopic__elections_and_campaigns | NCSL metatopics which contain the bill | string     | Statenet/NCSL |

### <a name="Billsstate_unified_bill_id" id="state_unified_bill_id"></a>`state_unified_bill_id`

| **Example**           | **Description**          | **Type**   | **Source**   |
|:----------------------|:-------------------------|:-----------|:-------------|
| NE_LR_0000000019_2011 | Internal bill identifier | string     | CHORUS       |



## Clients

Columns: [`client_name`](#Clientsclient_name), [`state`](#Clientsstate), [`source`](#Clientssource), [`source_eid`](#Clientssource_eid), [`ftm_industry`](#Clientsftm_industry), [`state_client_id`](#Clientsstate_client_id), [`ftm_guessed`](#Clientsftm_guessed)

### <a name="Clientsclient_name" id="client_name"></a>`client_name`

| **Example**           | **Description**                                                    | **Type**   | **Source**                                                     |
|:----------------------|:-------------------------------------------------------------------|:-----------|:---------------------------------------------------------------|
| WISCONSIN ENVIRONMENT | The name of the client as it appeared in the original data source. | string     | CHORUS, FollowTheMoney, OpenSecrets, or Google Knowledge Graph |

**Additional information:** For CHORUS clients, this name matches the raw string parsed from the documents scraped from state legislatures, which may vary across different sources and over time for the same organization.

### <a name="Clientsstate" id="state"></a>`state`

| **Example**   | **Description**   | **Type**   | **Source**   |
|:--------------|:------------------|:-----------|:-------------|
| WI            | The US state.     | string     | CHORUS       |

### <a name="Clientssource" id="source"></a>`source`

| **Example**   | **Description**                                 | **Type**   | **Source**                                                     |
|:--------------|:------------------------------------------------|:-----------|:---------------------------------------------------------------|
| ftm           | The dataset from which this client was sourced. | string     | CHORUS, FollowTheMoney, OpenSecrets, or Google Knowledge Graph |

### <a name="Clientssource_eid" id="source_eid"></a>`source_eid`

| **Example**   | **Description**                                                                                                                                               | **Type**   | **Source**                                                     |
|:--------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------|:---------------------------------------------------------------|
| ftm_24761754  | The client's id in its dataset of origin. Since clients in CHORUS are assigned separate state_client_ids, this field is blank for names gathered from CHORUS. | string     | CHORUS, FollowTheMoney, OpenSecrets, or Google Knowledge Graph |

**Additional information:** Since clients in CHORUS are assigned separate state_client_ids, this field is blank for names gathered from CHORUS.

### <a name="Clientsftm_industry" id="ftm_industry"></a>`ftm_industry`

| **Example**              | **Description**                                                                                                                                                                                      | **Type**   | **Source**     |
|:-------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------|:---------------|
| PRO-ENVIRONMENTAL POLICY | The client's industry, coded using Follow The Money's categories. The determination of each industry was done either by Follow the Money directly, or using text analysis (see "ftm_guessed" field). | string     | FollowTheMoney |

**Additional information:** Note the ftm_guessed field.

### <a name="Clientsstate_client_id" id="state_client_id"></a>`state_client_id`

| **Example**   | **Description**            | **Type**   | **Source**   |
|:--------------|:---------------------------|:-----------|:-------------|
| WI_773        | The client's id in CHORUS. | string     | CHORUS       |

### <a name="Clientsftm_guessed" id="ftm_guessed"></a>`ftm_guessed`

| **Example**   | **Description**                                                                                                                                                                                       | **Type**   | **Source**   |
|:--------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------|:-------------|
| False         | If False, the industry categorization was done by Follow the Money. If True, the industry is a guess based on the name of the client, using a Naive Bayes classifier trained on the non-guessed data. | boolean    | CHORUS       |



## Positions

Columns: [`client_name`](#Positionsclient_name), [`lobbyist_rep_name`](#Positionslobbyist_rep_name), [`lobbyist_firm_name`](#Positionslobbyist_firm_name), [`position`](#Positionsposition), [`start_date`](#Positionsstart_date), [`end_date`](#Positionsend_date), [`year`](#Positionsyear), [`record_type`](#Positionsrecord_type), [`session`](#Positionssession), [`description`](#Positionsdescription), [`committee`](#Positionscommittee), [`state`](#Positionsstate), [`position_numeric`](#Positionsposition_numeric), [`docket_number`](#Positionsdocket_number), [`docket_prefix`](#Positionsdocket_prefix), [`legiscan_bill_id`](#Positionslegiscan_bill_id), [`state_unified_bill_id`](#Positionsstate_unified_bill_id), [`state_client_id`](#Positionsstate_client_id), [`ncsl_metatopics`](#Positionsncsl_metatopics), [`ncsl_topics`](#Positionsncsl_topics)

### <a name="Positionsclient_name" id="client_name"></a>`client_name`

| **Example**                 | **Description**                                                    | **Type**   | **Source**   |
|:----------------------------|:-------------------------------------------------------------------|:-----------|:-------------|
| Direct Energy Services, LLC | The name recorded by the client (interest group) for this position | string     | CHORUS       |

### <a name="Positionslobbyist_rep_name" id="lobbyist_rep_name"></a>`lobbyist_rep_name`

| **Example**     | **Description**                                                          | **Type**   | **Source**   |
|:----------------|:-------------------------------------------------------------------------|:-----------|:-------------|
| Paul T. Donovan | The name of the lobbyist recording this position on behalf of the client | string     | CHORUS       |

### <a name="Positionslobbyist_firm_name" id="lobbyist_firm_name"></a>`lobbyist_firm_name`

| **Example**                    | **Description**                          | **Type**   | **Source**   |
|:-------------------------------|:-----------------------------------------|:-----------|:-------------|
| Kearney, Donovan & McGee, P.C. | The name of the lobbyist's employer firm | string     | CHORUS       |

### <a name="Positionsposition" id="position"></a>`position`

| **Example**   | **Description**                                                      | **Type**   | **Source**   |
|:--------------|:---------------------------------------------------------------------|:-----------|:-------------|
| NEUTRAL       | The string position, i.e. what was originally written on the record. | string     | CHORUS       |

### <a name="Positionsstart_date" id="start_date"></a>`start_date`

| **Example**               | **Description**                                    | **Type**   | **Source**   |
|:--------------------------|:---------------------------------------------------|:-----------|:-------------|
| 2011-01-01 00:00:00+00:00 | The first date on which the position was reported. | datetime   | CHORUS       |

### <a name="Positionsend_date" id="end_date"></a>`end_date`

| **Example**               | **Description**                                                                                      | **Type**   | **Source**   |
|:--------------------------|:-----------------------------------------------------------------------------------------------------|:-----------|:-------------|
| 2011-06-30 00:00:00+00:00 | The last date on which the position was reported, or the end of the reporting period, if applicable. | datetime   | CHORUS       |

**Additional information:** Not all positions have end_dates, and in general end_dates are taken from the end of the applicable reporting period, so they should not be seen as strict bounds on the position. It may be best practice to assume a given position holds until either (a) the text of the bill changes from its value at the `start_date` or (b) the client records a new position on that bill.

### <a name="Positionsyear" id="year"></a>`year`

|   **Example** | **Description**                              | **Type**   | **Source**   |
|--------------:|:---------------------------------------------|:-----------|:-------------|
|          2011 | The year in which the position was reported. | integer    | CHORUS       |

### <a name="Positionsrecord_type" id="record_type"></a>`record_type`

| **Example**   | **Description**                                                                                                                                                   | **Type**   | **Source**   | **Possible Values**     |
|:--------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------|:-------------|:------------------------|
| lobbying      | The type of disclosure record from which the position was collected: "lobbying" for lobbying disclosures and "testimony" for all forms of public hearing records. | string     | CHORUS       | "lobbying", "testimony" |

### <a name="Positionssession" id="session"></a>`session`

|   **Example** | **Description**                            | **Type**   | **Source**   |
|--------------:|:-------------------------------------------|:-----------|:-------------|
|           187 | The session as reported by the legislature | string     | CHORUS       |

### <a name="Positionsdescription" id="description"></a>`description`

| **Example**                     | **Description**                                                         | **Type**   | **Source**   |
|:--------------------------------|:------------------------------------------------------------------------|:-----------|:-------------|
| HB37, HB223, [omitted], SD2009. | A general-purpose field for descriptive notes attached to the position. | string     | CHORUS       |

**Additional information:** In this example, the positions given to us by Massachusetts included a description column containing the plaintext, comma-delimited lists of bills for each position (support/oppose/neutral) from each client, from which we extracted one row per unique bill.

### <a name="Positionscommittee" id="committee"></a>`committee`

| **Example**                             | **Description**                                                | **Type**   | **Source**   |
|:----------------------------------------|:---------------------------------------------------------------|:-----------|:-------------|
| Telecommunications Utilities and Energy | The committee in which the position was stated, if applicable. | string     | CHORUS       |

### <a name="Positionsstate" id="state"></a>`state`

| **Example**   | **Description**   | **Type**   | **Source**   | **Possible Values**                                                                            |
|:--------------|:------------------|:-----------|:-------------|:-----------------------------------------------------------------------------------------------|
| MA            | The US state.     | string     | CHORUS       | "MA", "MO", "NJ", "NE", "MD", "IL", "TX", "OH", "KS", "FL", "AZ", "CO", "IA", "WI", "MO", "SD" |

### <a name="Positionsposition_numeric" id="position_numeric"></a>`position_numeric`

|   **Example** | **Description**                                                                                                                                                 | **Type**   | **Source**   | **Possible Values**   |
|--------------:|:----------------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------|:-------------|:----------------------|
|             0 | A numeric representation of the position which maps "oppose" and variants thereof to -1, "support" to +1, and "neutral" and all other ambiguous positions to 0. | integer    | CHORUS       | -1, 0, 1              |

### <a name="Positionsdocket_number" id="docket_number"></a>`docket_number`

|   **Example** | **Description**                                                                                                                                                                          | **Type**   | **Source**   |
|--------------:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------|:-------------|
|          2009 | The docket number of the prefiled bill, which we can sometimes use to map to final bill numbers when, as in this case, the position was stated before bills were assigned final numbers. | integer    | CHORUS       |

### <a name="Positionsdocket_prefix" id="docket_prefix"></a>`docket_prefix`

| **Example**   | **Description**                             | **Type**   | **Source**   |
|:--------------|:--------------------------------------------|:-----------|:-------------|
| SD            | The chamber in which the bill was prefiled. | string     | CHORUS       |

### <a name="Positionslegiscan_bill_id" id="legiscan_bill_id"></a>`legiscan_bill_id`

|   **Example** | **Description**                              | **Type**   | **Source**   |
|--------------:|:---------------------------------------------|:-----------|:-------------|
|      12345678 | The ID in the LegiScan database, if possible | integer    | LegiScan     |

### <a name="Positionsstate_unified_bill_id" id="state_unified_bill_id"></a>`state_unified_bill_id`

| **Example**          | **Description**                                 | **Type**   | **Source**   |
|:---------------------|:------------------------------------------------|:-----------|:-------------|
| MA_S_0000001958_2011 | The unified identifier used to reference bills. | string     | CHORUS       |

**Additional information:** Format is [state]_[chamber]_[10-digit bill number]_[session]

### <a name="Positionsstate_client_id" id="state_client_id"></a>`state_client_id`

| **Example**   | **Description**                  | **Type**   | **Source**   |
|:--------------|:---------------------------------|:-----------|:-------------|
| MA_548        | The id used to identify clients. | string     | CHORUS       |

### <a name="Positionsncsl_metatopics" id="ncsl_metatopics"></a>`ncsl_metatopics`

| **Example**            | **Description**                                | **Type**   | **Source**    |
|:-----------------------|:-----------------------------------------------|:-----------|:--------------|
| ncsl_metatopic__energy | Metatopics for this bill in the NCSL databases | string     | StateNet/NCSL |

**Additional information:** If plural, appears as comma-delimited values

### <a name="Positionsncsl_topics" id="ncsl_topics"></a>`ncsl_topics`

| **Example**                                                                                                                                                                | **Description**                            | **Type**   | **Source**    |
|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-------------------------------------------|:-----------|:--------------|
| ncsl_database__energy_legislation_tracking_database__ncsl_topic__renewable_energy; ncsl_database__energy_legislation_tracking_database__ncsl_topic__renewable_energy_solar | Topics for this bill in the NCSL databases | string     | StateNet/NCSL |

**Additional information:** If plural, appears as comma-delimited values



## Block Assignments

Columns: [`entity_id`](#Block Assignmentsentity_id), [`0`](#Block Assignments0), [`1`](#Block Assignments1), [`2`](#Block Assignments2), [`3`](#Block Assignments3), [`4`](#Block Assignments4), [`5`](#Block Assignments5), [`6`](#Block Assignments6), [`state`](#Block Assignmentsstate), [`record_type`](#Block Assignmentsrecord_type)

### <a name="Block Assignmentsentity_id" id="entity_id"></a>`entity_id`

| **Example**                   | **Description**                                                                                                     | **Type**   | **Source**   |
|:------------------------------|:--------------------------------------------------------------------------------------------------------------------|:-----------|:-------------|
| MA_1, or MA_H_0000000001_2020 | The state_client_id or state_unified_bill_id corresponding to the node in the HBSBM graph with this block structure | string     | CHORUS       |

### <a name="Block Assignments0" id="0"></a>`0`

| **Example**      | **Description**                                                                                                                                                                                                                                                                                           | **Type**   | **Source**   |
|:-----------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------|:-------------|
| MA_lobbying_3283 | The lowest-level block assignment (i.e. most granular). With increasing levels above this one the blocks become larger and less granular. The index of the highest-level block varies in different states as the HBSBMs equilibrate to different depths depending on the amount and richness of the data. | string     | CHORUS       |

**Additional information:** With increasing levels above this one the blocks become larger and less granular. The index of the highest-level block varies in different states as the HBSBMs equilibrate to different depths depending on the amount and richness of the data.

### <a name="Block Assignments1" id="1"></a>`1`

| **Example**     | **Type**   | **Source**   |
|:----------------|:-----------|:-------------|
| MA_lobbying_150 | string     | CHORUS       |

### <a name="Block Assignments2" id="2"></a>`2`

| **Example**   | **Type**   | **Source**   |
|:--------------|:-----------|:-------------|
| MA_lobbying_0 | string     | CHORUS       |

### <a name="Block Assignments3" id="3"></a>`3`

| **Example**    | **Type**   | **Source**   |
|:---------------|:-----------|:-------------|
| MA_lobbying_12 | string     | CHORUS       |

### <a name="Block Assignments4" id="4"></a>`4`

| **Example**   | **Type**   | **Source**   |
|:--------------|:-----------|:-------------|
| MA_lobbying_3 | string     | CHORUS       |

### <a name="Block Assignments5" id="5"></a>`5`

| **Example**   | **Type**   | **Source**   |
|:--------------|:-----------|:-------------|
| MA_lobbying_3 | string     | CHORUS       |

### <a name="Block Assignments6" id="6"></a>`6`

| **Example**   | **Type**   | **Source**   |
|:--------------|:-----------|:-------------|
| MA_lobbying_2 | string     | CHORUS       |

### <a name="Block Assignmentsstate" id="state"></a>`state`

| **Example**   | **Description**   | **Type**   | **Source**   |
|:--------------|:------------------|:-----------|:-------------|
| MA            | The US state.     | string     | CHORUS       |

### <a name="Block Assignmentsrecord_type" id="record_type"></a>`record_type`

| **Example**   | **Description**                                                                                                                                                   | **Type**   | **Source**   |
|:--------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------|:-------------|
| lobbying      | The type of disclosure record from which the position was collected: "lobbying" for lobbying disclosures and "testimony" for all forms of public hearing records. | string     | CHORUS       |




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
