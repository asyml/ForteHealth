"""
This file defines some HTML templates
"""


def number_of_results(total_hits: int, duration: float) -> str:
    """HTML scripts to display number of results and duration."""
    return f"""
        <div style="color:grey;font-size:95%;">
            {total_hits} results ({duration:.2f} seconds)
        </div><br>
    """


def search_result(highlights: str) -> str:
    """HTML scripts to display search results."""
    return f"""
        <div style="font-size:100%; white-space: pre-line;">
        {highlights}
        </div>
    """
