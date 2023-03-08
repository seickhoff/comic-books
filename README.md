![image](https://user-images.githubusercontent.com/2509012/223845161-31e04f52-7311-484a-8d47-2dd7ec92e446.png)


# Help Using the Online Comic Book Database

## Introduction

The Online Comic Book Database is a tool for maintaining and managing comic book collections. A knowledgeable collector designed it for his own personal use. The primary advantage of the Online Comic Book Database is that the data is not limited to your own PC. With the Online Comic Book Database, you can access your data from any computer with an Internet connection, regardless of the type of computer and its location.

### Comic Book Fields

There are twelve fields to every comic book record. Their names and data formats are listed below:

- Title
  - Use up to 50 alpha-numeric characters
  - Required field
- Publisher
  - Use up to 40 alpha-numeric characters
  - Required field
- Volume
  - Use an integer from 1 to 99
  - Required field
- Issue
  - Use up to 12 alpha-numeric characters
  - Required field
- Month
  - Use two-digit months from 01 to 12, or keep blank
  - Optional field
- Year
  - Use four-digit years from 0000 to 9999
  - Required field
- Quantity
  - Use an integer from 1 to 99
  - Required field
- Value
  - 0.01 to 99999.99
  - Must include the decimal point
  - Must include the leading zero for amounts less than 1.00 (i.e.: 0.25)
  - Required field
- Condition
  - Must use two capital letters
  - Required field
- Writer
  - Use up to 40 alpha-numeric characters
  - Enter as **Last Name, First Name**
  - Optional field
- Artist
  - Use up to 40 alpha-numeric characters
  - Enter as **Last Name, First Name**
  - Optional field
- Comments
  - Use up to 60 alpha-numeric characters
  - Optional field
 
### Login

Submit your Login and Password so the Online Comic Book Database knows which collection to work with.

![image](https://user-images.githubusercontent.com/2509012/223846214-0adba2c3-c3fa-4752-8e77-5dbe97dafa9f.png)

### Navigation Menu

Moving to different sections of the Online Comic Book Database is done with the Navigation Menu shown below.

- Help - Read the Help Pages
- Report - Create reports suitable for printing
- Maintenance - Record maintenance
- Backup - Export the data as pipe-delimited text

![image](https://user-images.githubusercontent.com/2509012/223846426-fe356874-8579-497c-854a-45ab75a9c085.png)

## Section 1: Report Generation

### Features

Report Generation contains the following features:

- No risk to data (view-only)
- Create reports suitable for printing
- Unrestricted searching and list ordering options
- Create custom or Overstreet-style reports
- Access the database from anywhere in the world
 
### Report Generation Form

The Report Generation Form is pictured in Figure 3. Use it to define what comics to include in reports. There are Text Input Boxes representing each field. Enter partial or exact phrases or numbers into the Text Boxes as search arguments. Pattern matching is not case sensitive.

![image](https://user-images.githubusercontent.com/2509012/223846657-7a6e6fc0-1d35-4405-9c01-f30da9bad31e.png)

### Searching Methods

Seven powerful methods are available for creating useful search definitions.

- **Partial Pattern**: Searches the field for any occurrence of the pattern. The pattern `man` will match **Batman**, **Maniac** and **Superman**.
- **Exact Pattern**: Searches the field for the exact occurrence of the pattern. Enclose your pattern in curly braces. The pattern `{spider}` will only match **Spider**, and will not match **Spiderman**.
- **Boundary Matching**: Searches for an occurrence of the pattern from the beginning or end of the field. Use a curly brace to indicate the beginning or end of the field. The pattern `{star` will match **Star Wars**, but will not match **Death Star**. Similarly, `man}` will match **Batman**, but will not match **Batman and Robin**.
- **Alternate Word Matching**: Searches for at least one occurrence of many patterns. Use the word or to list alternate matching patterns. The pattern `car or star` will match **Star Wars**, **Car Wars** and **Battlestar Galactica**. The pattern `(car or star)` wars will match **Star Wars** and **Car Wars**, but will not match **Battlestar Galactica**.
- **Alternate Character Matching**: Searches for at least one occurrence of many patterns. Enclose alternate characters in braces. The pattern `s[iou]n` will match **Berni Wrightson**, **Master of the Macabre**, **Red Sonja** and **Sin City: A Dame To Kill For**, but will not match **Search For Sanctuary**.
- **Wildcard Character Matching**: Searches for at least one occurrence of many patterns. Use the question mark to indicate any character. The pattern `s?n` will match **Berni Wrightson**, **Master of the Macabre**, **Red Sonja**, **Sin City: A Dame To Kill** For and **Search For Sanctuary**.
- **Wildcard Multi-Character Matching**: Searches for at least one occurrence of many patterns. Use an asterisk to indicate a multi-character wildcard. The pattern `s*n` will match **Spawn**, **Berni Wrightson**, **Master of the Macabre**, **Red Sonja**, **Sin City: A Dame To Kill For** and **Search For Sanctuary**.

### Any or All

- **Any**: Use the Radio Button labeled **Any** to report records if any field match is true.
- **All**: Use the Radio Button labeled **All** to report records if all field matches are true. Use **All** to create a report containing all records.

### Comic Fields to Print

- **Col**: Use the Checkboxes labeled **Col** to select the fields to include in the report. By default all fields are selected. At least one field must be selected. Generally, include just the fields you need in order to avoid making the report too large or cluttered.

### Sorting the Data

- **Wght**: Use the Scrolling List Boxes labeled **Wght** to define how the report will be sorted. Assign the lowest number to the highest sort priority field and assign the highest number to the lowest sort priority field. Normally, when selecting a field to include in a report, you will also assign a Sorting Weight. 
- **Asc/Dec**: Use the Radio Buttons labeled **Asc** and **Dec** to define the sorting direction. Select **Asc** for ascending order or **Dec** for descending order. The Sorting Direction is in effect only when a respective Wght has been assigned.

### Type of Report

- **Overstreet Style Y**: Use **Y** to create concise, price-guide style reports listing Title, Publisher, Volume, Issue and Value. All Col selections not used and therefor are ignored.

![image](https://user-images.githubusercontent.com/2509012/223847137-1dccbb14-b50d-4435-8076-07e1475f8f9b.png)

- **Overstreet Style N**: Customize the report field headers using **Col** selections. Distinct occurrences are reported and listed one record per line.

![image](https://user-images.githubusercontent.com/2509012/223847385-e4158349-4f2d-4c01-b9ea-23c470b66060.png)

### Search Examples

Use the following examples as guidelines to writing your own search definitions.

- Report for all comics in your collection:
  - Select **All**
  - Clear text from all Text Input Boxes (i.e.: Reset Form button)
- Find all comics in your collection worth between and including $1.00 and $3.99:
  - Select **Any** or **All** (same effect when searching one field)
  - Value Text Input Box: `{[1-3].??}`
- Find Comics in your collection with issues from 50-59 or 70-79:
  - Select **Any** or **All** (same effect when searching one field)
  - Issue Text Input Box: `{5?} or {7?}`
- Find Comics in your collection with issues from 50-59 or 70-79, and worth between $1.00 - $4.00, and drawn by John or Bill:
  - Select **All**
  - Issue Text Input Box: `{5?} or {7?}`
  - Value Text Input Box: `{[1-3].?? or {4.00`
  - Artist Text Input Box: `John or Bill`
- Find Comics in your collection with issues from 50-59 or 70-79, or worth between $1.00 - $4.00. or drawn by John or Bill:
  - Select **Any**
  - Issue Text Input Box:`{5?} or {7?}`
  - Value Text Input Box: `{[1-3].?? or {4.00`
  - Artist Text Input Box: `John or Bill`
 

## Section 2: Collection Maintenance

### Features

- Unrestricted Searching and Sorting Options
- Perform Group Modifications and Deletions
- Add a Comic or a Range of Comics

### Collection Maintenance Search Form

The collection maintenance Form is pictured below. It is nearly identical to the Report Generation Form. Use it to retrieve records you wish to change.

### Basic

Use the Radio Buttons labeled **Basic** and select **Yes** to use the Add Form with no Dropdown Menus. Select **No** to use the Add Form with Dropdown Menus. Selecting **Yes** can slow down system response time if your collection is large.

![image](https://user-images.githubusercontent.com/2509012/223847878-993ab7f9-ce28-4612-bd9e-856aa371dd29.png)

### Defining Search Definitions

See Report Generation search definitions.

### Matches

The following fifure displays a sample collection maintenance match list. The search definition is listed in the upper left corner and the records appear with all fields. The following actions can be performed.

- Modify Single Record
- Delete Single Record
- Modify Group
- Delete Group
 
![image](https://user-images.githubusercontent.com/2509012/223848278-0b963415-9157-45c1-be57-6d22c66d78c2.png)
 
### More

Matches are displayed 20 at a time. Use the More button to view the next set of records. Group Modifications and Deletions effect all of the matches, not just the records shown on the current page.

![image](https://user-images.githubusercontent.com/2509012/223848456-196810cf-acde-4a9a-96d0-f7c158a80dbb.png)

### Modify Single Record

Select the Radio Button of a specific comic book record and click on the Modify button. A retrieved record is shown next. The existing data is displayed on the left side Text Boxes and can be edited. Use the right side Dropdown Menus to conveniently select from a list of all existing data. Dropdown Menu selections override the text in the left side Text Boxes. Click the Submit button to perform the modification.

![image](https://user-images.githubusercontent.com/2509012/223848924-7b47d406-78ca-472d-b7fd-08b554c81e94.png)

![image](https://user-images.githubusercontent.com/2509012/223849005-1a156717-fa85-4e9f-9874-47f724a32bf4.png)

### Delete Single Record

Select the Radio Button of a specific comic book record and click on the Delete button.

### Add One Record

Select the Radio Button labeled **Add** One as shown in Figure 11. Enter data using the left side Text Boxes or the right side Dropdown Menus. Dropdown Menu selections override the text in the left side Text Boxes. The Artist, Writer and Comments are optional. The Text Boxes on the bottom row of the Add Form are not used. Press the Update button.

![image](https://user-images.githubusercontent.com/2509012/223849152-2e338319-9928-443d-b75d-ed1458a4dda6.png)

### Add Group Over a Range

Select the Radio Button labeled **Add Group**. Enter data using the left side Text Boxes or the right side Dropdown Menus if the Basic Radio Button is set to **No**. Dropdown Menu selections override the text in the left side Text Boxes. The Artist, Writer and Comments are optional. Next, fill in the Text Boxes labeled **Issue Start**, **Issue End**, **Month Start** and **Year Start**. Press the Update button. The issues and Date will automatically increment over the entire range.

### Modify the Entire Match List

Select the Radio Button labeled **Modify Group**. Enter data using the left side Text Boxes or the right side Dropdown Menus. Dropdown Menu selections override the text in the left side Text Boxes. Blank boxes are ignored. Press the Update button to apply the changes to the comic books in the match list.

Optionally, you can perform range updates to the match list by filling in the **Issue Start**, **Month Start** and **Year Start**. Be sure you have sorted the match list properly before updating.

### Delete the Entire Match List

Select the Radio Button labeled **Delete Group**. Press the Update button to delete all comic books in the match list.
