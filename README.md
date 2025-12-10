## google_sheets

**Author:** kamalei
**Version:** 0.0.2
**Type:** tool

### Description



This plugin provides a set of tools for integrating Google Sheets with Dify applications. It allows you to read and write data in Google Sheets directly from your Dify workflows and agents.

### Tools Included

-   **Batch Get**: Efficiently retrieve data from multiple ranges within a Google Sheet.
-   **Batch Update**: Efficiently update data in multiple ranges within a Google Sheet.
-   **Batch Append**: Append data to multiple sheets/ranges, automatically creating sheets if they don't exist.

### Setup

#### Prerequisites

-   A Google Cloud Platform account.
-   A Google Cloud project with the Google Sheets API enabled.
-   A service account with appropriate permissions for Google Sheets.

#### Creating a Service Account

1.  Go to the [Google Cloud Console](https://console.cloud.google.com/).
2.  Create a new project or select an existing one.
3.  Enable the Google Sheets API for your project.
4.  Create a service account:
    -   Go to "IAM & Admin" > "Service Accounts".
    -   Click "Create Service Account".
    -   Give it a name and description.
    -   Grant it appropriate roles (e.g., "Sheets Editor").
    -   Click "Create".
5.  Create a key for the service account:
    -   Click on the service account you just created.
    -   Go to the "Keys" tab.
    -   Click "Add Key" > "Create new key".
    -   Choose JSON format and click "Create".
    -   Save the downloaded JSON file securely.

#### Configuration in Dify

1.  In your Dify application, go to the Plugins section.
2.  Find and install the Google Sheets plugin.
3.  When configuring the plugin, you'll need to provide:
    -   `credentials_json`: The entire content of the service account JSON key file.

### Usage Examples

#### Batch Get

Use the Batch Get tool to retrieve data from multiple ranges.

```json
Input:
{
  "spreadsheet_id": "your_spreadsheet_id",
  "ranges": ["Sheet1!A1:C3", "Sheet2!B2:D4"]
}

Output:
{
    "spreadsheetId": "your_spreadsheet_id",
    "valueRanges": [
        {
            "range": "Sheet1!A1:C3",
            "values": [
                ["Header1", "Header2", "Header3"],
                ["Value1", "Value2", "Value3"],
                ["Value4", "Value5", "Value6"]
            ]
        },
        {
            "range": "Sheet2!B2:D4",
            "values": [
                ["HeaderA", "HeaderB", "HeaderC"],
                ["ValueA1", "ValueB1", "ValueC1"],
                ["ValueA2", "ValueB2", "ValueC2"]
            ]
        }
    ]
}
```

#### Batch Update
Use the 'Batch Update' tool to update multiple ranges in a sheet.
```json
Input:
{
"spreadsheet_id": "your_spreadsheet_id",
"data": [
    {
        "range": "Sheet1!A1:B2",
        "values": [
            ["NewHeader1", "NewHeader2"],
            ["NewValue1", "NewValue2"]
        ]
    },
     {
        "range": "Sheet2!C3:D4",
        "values": [
            ["Updated1", "Updated2"],
            ["Updated3", "Updated4"]
        ]
    }
]
}

Output:
{
    "spreadsheetId": "your_spreadsheet_id",
    "totalUpdatedRows": 4,
    "totalUpdatedColumns": 2,
    "totalUpdatedCells": 8,
    "responses": [
      {
        "updatedRange": "Sheet1!A1:B2"
      },
      {
        "updatedRange": "Sheet2!C3:D4"
      }
    ]

}
```

#### Batch Append
Use the 'Batch Append' tool to append data to multiple sheets. If a sheet listed in the range does not exist, it will be automatically created.

```json
Input:
{
  "spreadsheet_id": "your_spreadsheet_id",
  "data": [
    {
        "range": "Sheet1",
        "values": [
            ["NewRow1_Col1", "NewRow1_Col2"],
            ["NewRow2_Col1", "NewRow2_Col2"]
        ]
    },
    {
        "range": "NewSheet",
        "values": [
            ["Header1", "Header2"],
            ["Value1", "Value2"]
        ]
    }
  ]
}

Output:
{
    "spreadsheetId": "your_spreadsheet_id",
    "responses": [
      {
        "spreadsheetId": "your_spreadsheet_id",
        "updates": {
            "spreadsheetId": "your_spreadsheet_id",
            "updatedRange": "Sheet1!A10:B11",
            "updatedRows": 2,
            "updatedColumns": 2,
            "updatedCells": 4
        }
      },
      {
        "spreadsheetId": "your_spreadsheet_id",
        "updates": {
            "spreadsheetId": "your_spreadsheet_id",
            "updatedRange": "NewSheet!A1:B2",
            "updatedRows": 2,
            "updatedColumns": 2,
            "updatedCells": 4
        }
      }
    ]
}
```

### Permissions and Security

-   The tools operate with the permissions of the service account you configured.
-   To access user-specific sheets, you'll need to share those sheets with the service account's email address.
-   For shared drives, the service account needs to be added as a member of the shared drive.

### Troubleshooting

-   If you encounter issues:
    -   Verify that the Google Sheets API is enabled in your Google Cloud project.
    -   Check that the service account has the necessary permissions.
    -   Ensure the credentials JSON is correctly formatted and complete.
    -   For "Sheet not found" errors, verify that the sheet exists and is accessible to the service account.
    - Make sure the sheet name is correct.

### Support

For issues or feature requests, please contact [@omluc_ai](https://twitter.com/omluc_ai) on X.
