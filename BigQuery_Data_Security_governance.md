BigQuery Data Security
Overview
BigQuery Data Security is a collection of features that help organizations protect sensitive data and ensure that only authorized users can access the appropriate information.
Data security is not limited to allowing or denying access to a table. It provides multiple levels of protection, including:
•	IAM (Identity and Access Management)
•	Dataset and Table Permissions
•	Column-Level Security
•	Row-Level Security
•	Dynamic Data Masking
•	Encryption
•	Auditing and Monitoring
These features work together to ensure users see only the data they are authorized to access.
________________________________________
BigQuery Security Architecture
                        BigQuery Table
                              │
                              ▼
                     IAM Authentication
                              │
                              ▼
                  Can user access the table?
                              │
                 ┌────────────┴────────────┐
                 │                       			    │
               No                          		Yes
                 │                       			  │
        Access Denied           		 ▼
                                  		Row-Level Security
                                    			   │
                                          			  ▼
                               Filter unauthorized rows
                                           │
                                          ▼
                              Column-Level Security
                                           │
                                          ▼
                             Hide sensitive columns
                                           │
                                          ▼
                              Dynamic Data Masking
                                           │
                                          ▼
                         Show original or masked values
                                           │
                                          ▼
                               Return query result
________________________________________
1. IAM (Identity and Access Management)
What is IAM?
IAM determines whether a user can access a resource such as a project, dataset, or table.
It is the first layer of security in BigQuery.
Without IAM permission, a user cannot query a table.
________________________________________
Example
Dataset:
security_demo
Users
Owner
pavan202607@gmail.com
Developer
pavanreddy2697@gmail.com
Initially
Developer is not shared on the dataset.
Developer executes
SELECT *
FROM security_demo.employee;
Result
Access Denied
Reason
Developer does not have permission to access the dataset.
________________________________________
After granting
BigQuery Data Viewer
Developer executes
SELECT *
FROM security_demo.employee;
Now the query succeeds.
________________________________________
Purpose
IAM answers only one question:
Can the user access the table?
It does not decide which rows or columns the user can view.
________________________________________
2. Data Governance
What is Data Governance?
Data Governance is the process of managing data throughout its lifecycle.
It ensures:
•	Data ownership
•	Data quality
•	Data classification
•	Data lineage
•	Data security
•	Compliance
________________________________________
Example
Employee table contains
Employee Name
Salary
Email
SSN
Governance defines
-Owner
HR Team
-Classification
Confidential
-Contains PII
Yes
-Retention
7 Years
________________________________________
Google Cloud Services Used
•	BigQuery
•	Dataplex Universal Catalog
•	Policy Tags
•	Data Policies
•	Cloud Audit Logs
________________________________________
3. Column-Level Security
What is Column-Level Security?
Column-Level Security protects sensitive columns.
Instead of hiding the entire table, it hides only selected columns.
BigQuery uses
Policy Tags
to implement Column-Level Security.
________________________________________
Example
Employee Table
Name	Salary	SSN
John	90000	111-22-3333
Developer should not see SSN.
________________________________________
Steps Performed
Step 1
Created
Testing-Taxonomy
A Taxonomy is a collection of related Policy Tags used to organize and classify sensitive data within BigQuery.
________________________________________
Step 2
Created
Testing-Policy-Tag
A Policy Tag is a label assigned to a table column to classify it (for example, Confidential or PII) and enforce column-level security or dynamic data masking.
________________________________________
Step 3
Assigned Policy Tag to
ssn
column.
________________________________________
Step 4
Granted
Fine-Grained Reader
only to Owner.
Developer was not granted this permission.
________________________________________
Developer executes
SELECT *
FROM security_demo.employee;
Result
Access Denied

User has neither fine-grained reader nor masked get permission.
Fine-Grained Reader
A Fine-Grained Reader is an IAM permission that allows a user to view the original (unmasked) values of columns protected by Policy Tags.
Masked Reader
A Masked Reader is an IAM permission that allows a user to query protected columns but only view masked values according to the configured Data Masking policy.
________________________________________
Important
Policy Tags only classify the column.
They do not mask the data.
They require
•	Fine-Grained Reader
•	or Masked Reader permission
________________________________________
Policy Tag
A Policy Tag identifies sensitive columns.
Example
Testing-Taxonomy

      │

      └── Testing-Policy-Tag
Attached to
Employee.SSN
________________________________________
Fine-Grained Reader
If user has
Fine-Grained Reader
Result
Original Value
Example
111-22-3333
________________________________________
Without Fine-Grained Reader
Result
Access Denied
unless masking permission exists.
________________________________________
4. Dynamic Data Masking
What is Dynamic Data Masking?
Dynamic Data Masking allows users to query sensitive columns while viewing masked values instead of the original values.
The actual data remains unchanged in the table.
Only the displayed result is modified.
________________________________________
Example
Original Email
john@gmail.com
Developer sees
j***@gmail.com
Owner sees
john@gmail.com
Same query
Different output.
________________________________________
Data Policy
Dynamic masking is implemented using
Data Policy
A Data Policy is created on a Policy Tag.
Relationship
Column
↓
Policy Tag
↓
Data Policy
↓
Masking Rule
________________________________________
Available Masking Rules
Examples
Email Mask
john@gmail.com
↓
j***@gmail.com
________________________________________
Last Four Characters
111223333
↓
*****3333
________________________________________
Always Null
NULL
________________________________________
SHA256
Returns hashed value.
________________________________________
Default Masking Value
Returns default value.
________________________________________
Permissions
Scenario 1
Fine-Grained Reader
YES
Masked Reader
NO
Result
Original Value
________________________________________
Scenario 2
Fine-Grained Reader
NO
Masked Reader
YES
Result
Masked Value
________________________________________
Scenario 3
Fine-Grained Reader
NO
Masked Reader
NO
Result
Access Denied
________________________________________
Scenario 4
Fine-Grained Reader
YES
Masked Reader
YES
Result
Original Value
Fine-Grained Reader always takes precedence.
________________________________________
5. Row-Level Security
What is Row-Level Security?
Row-Level Security filters rows automatically based on the user.
Users execute the same query.
BigQuery automatically returns only authorized rows.
________________________________________
Example
Student Table
Student	State
Rahul	Telangana
Priya	Andhra Pradesh
Amit	Karnataka
Developer should see only Telangana students.
Created
CREATE ROW ACCESS POLICY telangana_policy
ON security_demo.student
GRANT TO ("user:pavanreddy2697@gmail.com")
FILTER USING(state='Telangana');
Developer executes
SELECT *
FROM security_demo.student;
Output
Student	State
Rahul	Telangana
No WHERE clause required.
BigQuery filters rows automatically.
________________________________________
View Row-Level Security in UI
Navigation
BigQuery
↓
Table
↓
Schema
↓
View Row Access Policies
________________________________________
Filter
state='Telangana'
Grantee
user:pavanreddy2697@gmail.com
________________________________________
Delete Row Access Policy
If multiple policies exist
DROP ROW ACCESS POLICY policy_name
ON table_name;
________________________________________
If it is the last policy
DROP ALL ROW ACCESS POLICIES
ON table_name;
________________________________________
Why DROP ALL?
Suppose only one policy exists.
Deleting it would expose all rows to everyone who already has table access.
To prevent accidental exposure, BigQuery requires
DROP ALL ROW ACCESS POLICIES
instead of
DROP ROW ACCESS POLICY
This acts as a safety confirmation.
________________________________________
Can IAM Override Row-Level Security?
No.
Once a Row Access Policy applies to a user, BigQuery enforces it.
Example
Developer has
BigQuery Data Viewer
Still
Only Telangana rows
are visible.
IAM cannot bypass Row-Level Security.
________________________________________
Who Can See All Rows?
Generally:
•	Project Owner
•	Dataset Owner
•	Table Owner
•	BigQuery administrators (administrative privileges)
If a Row Access Policy specifically applies to a user, it is enforced for that user.
________________________________________
Order of Security Evaluation
BigQuery evaluates security in the following order:
User
↓
IAM
↓
Can access table?
↓
Row-Level Security
↓
Column-Level Security
↓
Dynamic Data Masking
↓
Query Result
________________________________________
Difference Between Security Features
Feature	                Purpose                                          	Example
IAM	                    Allow/Deny access to dataset or table	Developer cannot query table
Column-Level Security	  Hide sensitive columns	                         Hide SSN column
Row-Level Security    	Hide rows	                                       Developer sees only Telangana students
Dynamic Data Masking	  Mask sensitive values                            Email displayed as j***@gmail.com
Data Governance	        Manage ownership, classification, lineage, compliance	Employee table classified as Confidential

## Advantages of BigQuery Data Security

* Protects sensitive data from unauthorized access.
* Provides multiple layers of security (IAM, Row-Level Security, Column-Level Security, Dynamic Data Masking).
* Helps meet security and compliance requirements.
* Supports the principle of least privilege by granting only the required access.
* Encrypts data at rest and in transit.
* Enables auditing and monitoring of data access.

## Advantages of Data Governance

* Clearly defines data ownership and accountability.
* Improves data quality and consistency.
* Helps classify sensitive and confidential data.
* Provides data lineage for tracking data flow.
* Simplifies regulatory compliance and auditing.
* Enables centralized management of enterprise data assets.

## Advantages of Dynamic Data Masking

* Protects sensitive information without modifying the original data.
* Allows users to query data while hiding confidential values.
* Reduces the risk of exposing Personally Identifiable Information (PII).
* Supports role-based access to sensitive data.
* Eliminates the need to create duplicate masked tables.
* Automatically applies masking based on user permissions.

## Advantages of Column-Level Security

* Restricts access to specific sensitive columns.
* Allows users to access the same table without exposing confidential fields.
* Provides fine-grained access control using Policy Tags.
* Reduces the need to create multiple versions of the same table.
* Helps organizations comply with privacy and security regulations.

## Advantages of Row-Level Security

* Restricts users to only the rows they are authorized to view.
* Enables user-specific data access without changing application queries.
* Eliminates the need to create separate tables for different users or departments.
* Improves data security by preventing unauthorized access to specific records.
* Simplifies access management through centralized Row Access Policies.
* Ensures the same query returns different results based on the user's permissions.
