"""Tool for batch appending data in Google Sheets."""

from collections.abc import Generator
from typing import Any
import json
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from .utils.google_service import get_sheets_service, handle_google_api_error


class BatchAppendTool(Tool):
    """Tool for appending data to multiple sheets/ranges in a Google Sheet."""
    
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        """Invoke the batch append operation.
        
        Args:
            tool_parameters: The parameters for the tool
                spreadsheet_id: The ID of the spreadsheet
                data: A list of objects, each containing 'range' and 'values' keys
                      (either as a JSON string or already parsed)
                value_input_option: How the input data should be interpreted
                insert_data_option: How the input data should be inserted.
                include_values_in_response: Whether to include the values in the response
                response_value_render_option: How the values in the response should be rendered
                response_date_time_render_option: How dates, times, and durations in the response should be rendered
                
        Yields:
            Either a success message with the append results or an error message
        """
        # Extract parameters
        spreadsheet_id = tool_parameters.get('spreadsheet_id')
        data_param = tool_parameters.get('data')
        value_input_option = tool_parameters.get('value_input_option', 'USER_ENTERED')
        insert_data_option = tool_parameters.get('insert_data_option', 'INSERT_ROWS')
        include_values_in_response = tool_parameters.get('include_values_in_response', False)
        response_value_render_option = tool_parameters.get('response_value_render_option')
        response_date_time_render_option = tool_parameters.get('response_date_time_render_option')
        
        if not spreadsheet_id:
            yield self.create_text_message("Missing required parameter: spreadsheet_id")
            return
            
        if not data_param:
            yield self.create_text_message("Missing required parameter: data")
            return
            
        try:
            # Parse data if it's a string
            if isinstance(data_param, str):
                try:
                    data = json.loads(data_param)
                except json.JSONDecodeError:
                    yield self.create_text_message("Invalid JSON format for data. Please provide a valid JSON array.")
                    return
            else:
                data = data_param
                
            # Validate data format
            if not isinstance(data, list):
                yield self.create_text_message("Data must be a list of objects, each with 'range' and 'values' keys")
                return
            
            # Get credentials from provider
            creds = self.runtime.credentials.get('credentials_json')
            creds_json = json.loads(creds)
            
            # Build service
            service = get_sheets_service(creds_json)
            
            # Get all existing sheet titles
            spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
            existing_sheets = {sheet['properties']['title'] for sheet in spreadsheet.get('sheets', [])}
            
            responses = []
            
            # Process the data items
            for item in data:
                if 'range' not in item or 'values' not in item:
                    yield self.create_text_message("Each data item must contain 'range' and 'values' keys")
                    return
                
                range_str = item['range']
                # extract sheet name from range
                if '!' in range_str:
                    sheet_name = range_str.split('!', 1)[0]
                else:
                    sheet_name = range_str
                
                # Remove single quotes if present (e.g. 'Sheet 1'!A1)
                if sheet_name.startswith("'") and sheet_name.endswith("'"):
                    sheet_name = sheet_name[1:-1]
                
                # Create sheet if it doesn't exist
                if sheet_name not in existing_sheets:
                    # Create the sheet
                    body = {
                        'requests': [
                            {
                                'addSheet': {
                                    'properties': {
                                        'title': sheet_name
                                    }
                                }
                            }
                        ]
                    }
                    service.spreadsheets().batchUpdate(
                        spreadsheetId=spreadsheet_id,
                        body=body
                    ).execute()
                    existing_sheets.add(sheet_name)
                    
                body = {'values': item['values']}
                
                # Note: The google client library method 'append' usually accepts kwargs for query parameters.
                # However, looking at the discovery document or method signature, 
                # we should pass them as arguments to append().
                # Let's re-construct the call to be safer and cleaner.
                
                kwargs = {
                    'spreadsheetId': spreadsheet_id,
                    'range': item['range'],
                    'valueInputOption': value_input_option,
                    'insertDataOption': insert_data_option,
                    'includeValuesInResponse': include_values_in_response,
                    'body': body
                }
                
                if response_value_render_option:
                    kwargs['responseValueRenderOption'] = response_value_render_option
                    
                if response_date_time_render_option:
                    kwargs['responseDateTimeRenderOption'] = response_date_time_render_option

                result = service.spreadsheets().values().append(**kwargs).execute()
                responses.append(result)
            
            # Return result
            yield self.create_json_message({"spreadsheetId": spreadsheet_id, "responses": responses})
            
        except Exception as e:
            error_message = handle_google_api_error(e)
            yield self.create_text_message(error_message)
