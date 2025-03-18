import logging
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        # This function will be extended to handle file conversions
        # using the Markitdown library in the next TODO item
        return func.HttpResponse(
            "Azure Function is ready for Markitdown integration.",
            status_code=200
        )
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return func.HttpResponse(
            f"An error occurred: {str(e)}",
            status_code=500
        )
